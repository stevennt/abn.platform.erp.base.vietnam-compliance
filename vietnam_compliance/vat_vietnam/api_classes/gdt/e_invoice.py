import frappe
from frappe import _

from vietnam_compliance.vat_vietnam.api_classes.base import BaseAPI


class GDTEInvoiceAPI(BaseAPI):
    API_NAME = "GDT e-Invoice"

    @classmethod
    def create(cls, *args, **kwargs):
        if cls != GDTEInvoiceAPI:
            return cls(*args, **kwargs)
        return GDTEInvoiceAPI(*args, **kwargs)

    def setup(self, doc=None, *, company_mst=None):
        self.validate_enable_api()
        self.company_mst = company_mst

        if doc:
            self.company_mst = doc.get("company_mst") or frappe.db.get_value(
                "Company", doc.company, "custom_mst"
            )

        gdt_config = frappe.get_cached_doc("Tax Department Config")
        self.sandbox_mode = gdt_config.get("sandbox_mode", False)
        self.gdt_api_url = gdt_config.get("gdt_api_url", "https://hoadondientu.gdt.gov.vn")

        if self.sandbox_mode:
            self.gdt_api_url = gdt_config.get(
                "gdt_sandbox_url", "https://hoadondientutest.gdt.gov.vn"
            )

    def validate_enable_api(self):
        gdt_config = frappe.get_cached_doc("Tax Department Config")
        if not gdt_config.get("enable_e_invoice"):
            frappe.throw(_("E-Invoice is not enabled in Tax Department Config"))

    def authenticate(self):
        pass

    def submit_invoice(self, signed_xml):
        if self.sandbox_mode:
            return self._mock_submit_response()
        raise NotImplementedError(_("Real GDT API integration pending sandbox credentials"))

    def get_invoice_status(self, transaction_id):
        if self.sandbox_mode:
            return self._mock_status_response(transaction_id)
        raise NotImplementedError(_("Real GDT API integration pending sandbox credentials"))

    def cancel_invoice(self, transaction_id, reason=""):
        if self.sandbox_mode:
            return self._mock_cancel_response(transaction_id)
        raise NotImplementedError(_("Real GDT API integration pending sandbox credentials"))

    def _mock_submit_response(self):
        mock_transaction_id = frappe.generate_hash(length=20)
        return {
            "success": True,
            "transaction_id": mock_transaction_id,
            "status": "CQT cấp mã",
            "message": "Mock: Hóa đơn đã được tiếp nhận",
            "signed_xml": None,
        }

    def _mock_status_response(self, transaction_id):
        return {
            "success": True,
            "transaction_id": transaction_id,
            "status": "CQT cấp mã",
            "message": "Mock: Tra cứu thành công",
        }

    def _mock_cancel_response(self, transaction_id):
        return {
            "success": True,
            "transaction_id": transaction_id,
            "status": "Đã hủy",
            "message": "Mock: Hóa đơn đã được hủy",
        }


@frappe.whitelist()
def enqueue_bulk_e_invoice_generation(docnames):
    frappe.has_permission("Sales Invoice", "submit", throw=True)

    gdt_config = frappe.get_cached_doc("Tax Department Config")
    if not gdt_config.get("enable_e_invoice"):
        frappe.throw(_("Please enable e-Invoicing in Tax Department Config first"))

    docnames = frappe.parse_json(docnames) if docnames.startswith("[") else [docnames]
    frappe.enqueue(
        "vietnam_compliance.vat_vietnam.utils.e_invoice.generate_e_invoices",
        queue="short",
        docnames=docnames,
    )
