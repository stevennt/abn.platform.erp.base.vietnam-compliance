import frappe
from frappe import _
from frappe.utils import flt


def onload(doc, method=None):
    if doc.get("custom_transaction_id"):
        try:
            tax_config = frappe.get_cached_doc("Tax Department Config")
            if tax_config.enable_e_invoice:
                doc.set_onload("e_invoice_info", _get_e_invoice_info_from_log(doc))
        except Exception:
            pass


def validate(doc, method=None):
    _validate_mst(doc)
    _validate_form_number_and_series(doc)
    _set_einvoice_status_on_validate(doc)


def on_submit(doc, method=None):
    if not getattr(doc, "_submitted_from_ui", None):
        return

    try:
        tax_config = frappe.get_cached_doc("Tax Department Config")
    except Exception:
        return

    if not tax_config.enable_e_invoice:
        return

    if not doc.get("custom_einvoice_status") or doc.get("custom_einvoice_status") == "Chờ gửi":
        doc.db_set("custom_einvoice_status", "Chờ gửi")

    if tax_config.auto_generate_e_invoice:
        frappe.enqueue(
            "vietnam_compliance.vat_vietnam.utils.e_invoice.generate_e_invoice",
            enqueue_after_commit=True,
            queue="short",
            docname=doc.name,
        )


def before_cancel(doc, method=None):
    if not doc.get("custom_einvoice_status"):
        return

    statuses_requiring_cancel = ("Đã gửi CQT", "CQT cấp mã", "Đã có mã")
    if doc.get("custom_einvoice_status") in statuses_requiring_cancel:
        try:
            tax_config = frappe.get_cached_doc("Tax Department Config")
            if tax_config.auto_cancel_e_invoice:
                frappe.enqueue(
                    "vietnam_compliance.vat_vietnam.utils.e_invoice.cancel_e_invoice",
                    enqueue_after_commit=True,
                    queue="short",
                    docname=doc.name,
                )
        except Exception:
            pass


def on_update_after_submit(doc, method=None):
    pass


def get_dashboard_data(data):
    data.setdefault("transactions", []).insert(
        2,
        {
            "label": _("GDT Logs"),
            "items": ["EInvoice Log"],
        },
    )
    return data


def _validate_mst(doc):
    company_mst = frappe.db.get_value("Company", doc.company, "custom_mst")
    if not company_mst:
        frappe.msgprint(
            _("Company {0} chưa khai báo MST. Vui lòng cập nhật trong hồ sơ Công ty.").format(doc.company),
            indicator="yellow",
        )


def _validate_form_number_and_series(doc):
    if doc.get("custom_einvoice_status") == "Không áp dụng":
        return


def _set_einvoice_status_on_validate(doc):
    if doc.docstatus == 2:
        if doc.get("custom_transaction_id"):
            doc.custom_einvoice_status = "Chờ hủy"
        return

    if not doc.get("custom_einvoice_status"):
        tax_config = frappe.get_cached_doc("Tax Department Config")
        if tax_config.enable_e_invoice:
            doc.custom_einvoice_status = "Chờ gửi"


def _get_e_invoice_info_from_log(doc):
    logs = frappe.get_all(
        "EInvoice Log",
        filters={"reference_name": doc.name},
        fields=["transaction_id", "einvoice_status", "acknowledged_on", "is_cancelled"],
        order_by="creation desc",
        limit=1,
    )
    return logs[0] if logs else {}
