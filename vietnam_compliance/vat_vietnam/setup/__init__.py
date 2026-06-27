import frappe

from vietnam_compliance.vat_vietnam.constants.custom_fields import CUSTOM_FIELDS
from vietnam_compliance.vat_vietnam.setup.property_setters import get_property_setters
from vietnam_compliance.utils.custom_fields import get_custom_fields_creator

_create_custom_fields = get_custom_fields_creator("VAT Vietnam")


def after_install():
    create_custom_fields()
    create_property_setters(include_defaults=True)
    set_default_vat_settings()


def create_custom_fields():
    _create_custom_fields(CUSTOM_FIELDS, ignore_validate=True)

    installed_apps = frappe.get_installed_apps()

    if "hrms" in installed_apps:
        pass  # HRMS custom fields

    if "education" in installed_apps:
        pass  # Education custom fields

    if "healthcare" in installed_apps:
        pass  # Healthcare custom fields


def create_education_custom_fields():
    pass


def create_healthcare_custom_fields():
    pass


def create_hrms_custom_fields():
    pass


def create_property_setters(*, include_defaults=False):
    for property_setter in get_property_setters(include_defaults=include_defaults):
        frappe.make_property_setter(
            property_setter,
            validate_fields_for_doctype=False,
            is_system_generated=property_setter.get("is_system_generated", True),
        )


def set_default_vat_settings():
    if frappe.db.exists("Tax Department Config"):
        return

    frappe.get_doc({
        "doctype": "Tax Department Config",
        "enable_e_invoice": 0,
        "sandbox_mode": 1,
        "auto_generate_e_invoice": 0,
        "auto_cancel_e_invoice": 0,
    }).insert(ignore_permissions=True)


def setup_wizard_complete():
    from vietnam_compliance.vat_vietnam.constants.custom_fields import (
        CUSTOM_FIELDS,
    )
    _create_custom_fields(CUSTOM_FIELDS, ignore_validate=True)

EDUCATION_CUSTOM_FIELDS = {}
HEALTHCARE_CUSTOM_FIELDS = {}
HRMS_CUSTOM_FIELDS = {}
ITEM_VARIANT_FIELDNAMES = frozenset()
def get_all_custom_fields():
    return CUSTOM_FIELDS
