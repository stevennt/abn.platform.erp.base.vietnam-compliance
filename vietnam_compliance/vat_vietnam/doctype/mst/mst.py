import frappe
from frappe.model.document import Document
from frappe import _
import re


class MST(Document):
    def validate(self):
        self.validate_mst_format()

    def validate_mst_format(self):
        mst = self.mst
        if not mst:
            return

        mst_clean = re.sub(r"[^\d]", "", mst)
        if not mst_clean:
            frappe.throw(_("MST must contain 10 or 13 digits"))

        if len(mst_clean) not in (10, 13):
            frappe.throw(_("MST must be exactly 10 or 13 digits. Got {0} digits: {1}").format(len(mst_clean), mst_clean))

        self.mst = mst_clean
