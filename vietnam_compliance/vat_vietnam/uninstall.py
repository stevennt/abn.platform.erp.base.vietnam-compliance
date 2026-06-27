import frappe

from vietnam_compliance.vat_vietnam.constants.custom_fields import CUSTOM_FIELDS
from vietnam_compliance.vat_vietnam.setup.property_setters import get_property_setters
from vietnam_compliance.utils.custom_fields import delete_custom_fields


def before_uninstall():
    delete_custom_fields(CUSTOM_FIELDS)
    delete_property_setters()


def delete_property_setters():
    field_map = {
        "doctype": "doc_type",
        "fieldname": "field_name",
    }

    property_setters = get_property_setters(include_defaults=True)

    for property_setter in property_setters:
        for key, fieldname in field_map.items():
            if key in property_setter:
                property_setter[fieldname] = property_setter.pop(key)

        frappe.db.delete("Property Setter", property_setter)
