# Copyright (c) 2023, Resilient Tech and contributors
# For license information, please see license.txt
import frappe
from frappe import _
from frappe.model.document import Document
from frappe.utils import date_diff, format_date, get_datetime

from vietnam_compliance.vat_vietnam.utils import is_api_enabled, validate_mst_check_digit
from vietnam_compliance.vat_vietnam.utils.mst_info import (
    fetch_mst_status,
    fetch_transporter_id_status,
)

MST_STATUS = {
    "ACT": "Active",
    "CNL": "Cancelled",
    "INA": "Inactive",
    "PRO": "Provisional",
    "SUS": "Suspended",
}

MST_BLOCK_STATUS = {"U": 0, "B": 1}


class MST(Document):
    def before_save(self):
        self.status = MST_STATUS.get(self.status, self.status)
        self.is_blocked = MST_BLOCK_STATUS.get(self.is_blocked, 0)
        self.last_updated_on = get_datetime()

        if not self.cancelled_date and self.status == "Cancelled":
            self.cancelled_date = self.registration_date

    @frappe.whitelist()
    def update_mst_status(self):
        """
        Permission check not required as MST details are public and user has access to doc.
        """
        # hard refresh will always use public API
        create_or_update_mst_status(self.mst, throw=True, doc=self)

    @frappe.whitelist()
    def update_transporter_id_status(self):
        """
        Permission check not required as MST details are public and user has access to doc.
        """
        create_or_update_mst_status(self.mst, is_transporter_id=True, doc=self)


def get_gstr_1_filed_upto(mst):
    if not mst:
        return

    return frappe.db.get_value("MST", mst, "gstr_1_filed_upto")


def create_or_update_mst_status(
    mst=None,
    response=None,
    callback=None,
    doc=None,
    is_transporter_id=False,
    throw=False,
):
    if frappe.flags.in_import:
        return

    doctype = "MST"

    if not response:
        if is_transporter_id:
            response = fetch_transporter_id_status(mst, doc=doc, throw=throw)
        else:
            response = fetch_mst_status(mst=mst, doc=doc, throw=throw)

        if not response:
            return

    if frappe.db.exists(doctype, response.get("mst")):
        mst_doc = frappe.get_doc(doctype, response.pop("mst"))
    else:
        mst_doc = frappe.new_doc(doctype)

    mst_doc.update(response)
    mst_doc.save(ignore_permissions=True)

    transaction_date = None

    if doc:
        transaction_date = doc.get("transaction_date") or doc.get("posting_date")

    if callback:
        callback(mst_doc, transaction_date)

    return mst_doc


### MST Status Validation ###


def get_and_validate_mst_status(mst, doc):
    """
    Get and validate MST status.
    Enqueues fetching MST status if required and hence best suited for Backend use.
    """
    if not mst:
        return

    transaction_date = doc.get("transaction_date") or doc.get("posting_date")

    if not is_status_refresh_required(mst, transaction_date):
        if not frappe.db.exists("MST", mst):
            return

        mst_doc = frappe.get_doc("MST", mst)

        validate_mst_status(
            mst_doc,
            transaction_date=transaction_date,
            throw=True,
        )

    else:
        now = get_datetime()

        # Don't delay the response if API is required
        frappe.enqueue(
            create_or_update_mst_status,
            enqueue_after_commit=True,
            queue="short",
            mst=mst,
            doc=doc,
            callback=validate_mst_status,
            job_id=f"create_or_update_mst_status_{mst}_{now.date()}_{now.hour}",
        )


@frappe.whitelist()
def get_mst_status(mst: str, doc: str | dict | frappe._dict | None = None, force_update: bool = False):
    """
    Get MST status. Responds immediately, and best suited for Frontend use.
    Permission check not required as MST details are public where MST is known.
    """
    if not mst:
        return

    if doc and isinstance(doc, str):
        doc = frappe.parse_json(doc)

    if not doc:
        doc = frappe._dict()

    transaction_date = doc.get("transaction_date") or doc.get("posting_date")

    if not force_update and not is_status_refresh_required(
        mst, transaction_date, doc.get("docstatus") or 0
    ):
        if not frappe.db.exists("MST", mst):
            return

        return frappe.get_doc("MST", mst)

    return create_or_update_mst_status(mst, doc=doc, throw=force_update)


def validate_mst_status(mst_doc, transaction_date=None, throw=False):
    if not (mst_doc and transaction_date):
        return

    def _throw(message):
        if throw:
            frappe.throw(message)

        else:
            frappe.log_error(
                title=_("Invalid Party MST"),
                message=message,
            )

    registration_date = mst_doc.registration_date
    cancelled_date = mst_doc.cancelled_date

    if not registration_date:
        return _throw(
            _(
                "Registration date not found for party MST {0}. Please make sure MST is registered."
            ).format(mst_doc.mst)
        )

    if date_diff(transaction_date, registration_date) < 0:
        return _throw(
            _(
                "Party MST {1} is registered on {0}. Please make sure that document date is on or after {0}."
            ).format(format_date(registration_date), mst_doc.mst)
        )

    if mst_doc.status == "Cancelled" and date_diff(transaction_date, cancelled_date) >= 0:
        return _throw(
            _(
                "Party MST {1} is cancelled on {0}. Please make sure that document date is before {0}."
            ).format(format_date(cancelled_date), mst_doc.mst)
        )

    if mst_doc.status not in ("Active", "Cancelled"):
        return _throw(_("Status of Party MST {1} is {0}").format(mst_doc.status, mst_doc.mst))


def is_status_refresh_required(mst, transaction_date, docstatus=0):
    settings = frappe.get_cached_doc("GST Settings")

    if not settings.validate_mst_status or not is_api_enabled(settings) or settings.sandbox_mode:
        return False

    # # not from draft transactions
    if not transaction_date or docstatus > 0:
        return False

    doc = frappe.db.get_value("MST", mst, ["last_updated_on", "status"], as_dict=True)

    if not doc:
        return True

    if doc.status not in ("Active", "Cancelled"):
        return True

    days_since_last_update = date_diff(get_datetime(), doc.get("last_updated_on"))
    return days_since_last_update >= settings.mst_status_refresh_interval


### GST Transporter ID Validation ###


@frappe.whitelist()
def validate_gst_transporter_id(transporter_id: str, doc: str | dict | frappe._dict | None = None):
    """
    Validates GST Transporter ID and warns user if transporter_id is not Active.
    Just suggestive and not enforced.

    Only for Frontend use.

    Args:
        transporter_id (str): GST Transporter ID
    """
    if not transporter_id:
        return

    if doc and isinstance(doc, str):
        doc = frappe.parse_json(doc)

    mst = None

    settings = frappe.get_cached_doc("GST Settings")
    if not settings.validate_mst_status or not is_api_enabled(settings) or settings.sandbox_mode:
        return

    # Check if MST doc exists
    if frappe.db.exists("MST", transporter_id):
        mst = frappe.get_doc("MST", transporter_id)

    # Check if transporter_id starts with 88 or is not valid MST and use Transporter ID API
    elif transporter_id[:2] == "88" or has_mst_check_digit_failed(transporter_id):
        mst = create_or_update_mst_status(
            transporter_id,
            doc=doc,
            is_transporter_id=True,
        )

    # Use MST API
    else:
        mst = create_or_update_mst_status(transporter_id, doc=doc)

    if not mst:
        return

    # If MST status is not Active and transporter_id_status is None, use Transporter ID API
    if mst.status != "Active" and not mst.transporter_id_status:
        mst = create_or_update_mst_status(
            transporter_id,
            doc=doc,
            is_transporter_id=True,
        )

    # Return if MST or transporter_id_status is Active
    if mst.status == "Active" or mst.transporter_id_status == "Active":
        return

    frappe.msgprint(
        _("GST Transporter ID {0} seems to be Invalid").format(transporter_id),
        indicator="orange",
    )


def has_mst_check_digit_failed(mst):
    try:
        validate_mst_check_digit(mst)

    except frappe.ValidationError:
        return True

    return False
