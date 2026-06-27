import frappe
from frappe import _


def generate_e_invoice(docname):
    """Generate and submit a single e-invoice to GDT."""
    try:
        doc = frappe.get_doc("Sales Invoice", docname)
    except frappe.DoesNotExistError:
        return

    try:
        from vietnam_compliance.vat_vietnam.xml_generator import generate_e_invoice_xml
        from vietnam_compliance.vat_vietnam.signing import get_signing_provider
        from vietnam_compliance.vat_vietnam.api_classes.gdt.e_invoice import GDTEInvoiceAPI

        xml_data = generate_e_invoice_xml(doc)
        signer = get_signing_provider()
        signed_xml = signer.sign_xml(xml_data)

        api = GDTEInvoiceAPI.create()
        api.setup(doc)
        response = api.submit_invoice(signed_xml)

        if response.get("success"):
            doc.db_set("custom_transaction_id", response.get("transaction_id"))
            doc.db_set("custom_einvoice_status", response.get("status", "CQT cấp mã"))
            doc.db_set("custom_gdt_submitted_on", frappe.utils.now())

            _create_einvoice_log(doc.name, response)
        else:
            doc.db_set("custom_einvoice_status", "Lỗi")
            frappe.log_error(
                f"GDT submission failed: {response.get('message', '')}",
                "E-Invoice Generation"
            )

    except Exception as e:
        doc.db_set("custom_einvoice_status", "Lỗi")
        frappe.log_error(frappe.get_traceback(), "E-Invoice Generation Error")


def generate_e_invoices(docnames):
    """Bulk e-invoice generation."""
    for name in docnames:
        generate_e_invoice(name)


def cancel_e_invoice(docname, reason=""):
    """Cancel an e-invoice on GDT."""
    try:
        doc = frappe.get_doc("Sales Invoice", docname)
    except frappe.DoesNotExistError:
        return

    try:
        from vietnam_compliance.vat_vietnam.api_classes.gdt.e_invoice import GDTEInvoiceAPI

        api = GDTEInvoiceAPI.create()
        api.setup(doc)
        response = api.cancel_invoice(doc.get("custom_transaction_id"), reason)

        if response.get("success"):
            doc.db_set("custom_einvoice_status", "Đã hủy")
            _update_einvoice_log(docname, {"einvoice_status": "Đã hủy", "is_cancelled": 1})
        else:
            frappe.log_error(
                f"GDT cancel failed: {response.get('message', '')}",
                "E-Invoice Cancellation"
            )

    except Exception as e:
        frappe.log_error(frappe.get_traceback(), "E-Invoice Cancellation Error")


def check_e_invoice_status(docname):
    """Check e-invoice status from GDT."""
    try:
        doc = frappe.get_doc("Sales Invoice", docname)
    except frappe.DoesNotExistError:
        return {"status": "Unknown"}

    txn_id = doc.get("custom_transaction_id")
    if not txn_id:
        return {"status": doc.get("custom_einvoice_status", "Chưa gửi")}

    try:
        from vietnam_compliance.vat_vietnam.api_classes.gdt.e_invoice import GDTEInvoiceAPI

        api = GDTEInvoiceAPI.create()
        api.setup(doc)
        return api.get_invoice_status(txn_id)
    except Exception:
        return {"status": doc.get("custom_einvoice_status", "Không xác định")}


def retry_e_invoice_generation():
    """Retry failed e-invoice submissions."""
    failed_logs = frappe.get_all(
        "EInvoice Log",
        filters={"einvoice_status": "Lỗi"},
        fields=["reference_name"],
        limit=50,
    )

    for log in failed_logs:
        generate_e_invoice(log.reference_name)


def _create_einvoice_log(docname, response):
    if frappe.db.exists("EInvoice Log", {"reference_name": docname}):
        _update_einvoice_log(docname, response)
        return

    frappe.get_doc({
        "doctype": "EInvoice Log",
        "transaction_id": response.get("transaction_id"),
        "reference_doctype": "Sales Invoice",
        "reference_name": docname,
        "einvoice_status": response.get("status", "CQT cấp mã"),
        "is_generated_in_sandbox_mode": response.get("sandbox", 0),
    }).insert(ignore_permissions=True)


def _update_einvoice_log(docname, updates):
    log_name = frappe.db.get_value("EInvoice Log", {"reference_name": docname}, "name")
    if log_name:
        log = frappe.get_doc("EInvoice Log", log_name)
        log.update(updates)
        log.save(ignore_permissions=True)
