app_name = "vietnam_compliance"
app_title = "Vietnam Compliance"
app_publisher = "ABN Platform"
app_description = "Vietnam e-invoice compliance app for ERPNext — hóa đơn điện tử theo Nghị định 123/2020/NĐ-CP và Thông tư 78/2021/TT-BTC"
app_icon = "octicon octicon-file-directory"
app_color = "red"
app_email = "hello@abnplatform.com"
app_license = "GNU General Public License (v3)"
required_apps = ["frappe/erpnext"]
app_home = "/desk/vat-vietnam"

add_to_apps_screen = [
    {
        "name": app_name,
        "logo": "/assets/vietnam_compliance/images/vietnam-compliance.svg",
        "title": app_title,
        "route": app_home,
        "has_permission": "vietnam_compliance.check_app_permission",
    }
]

before_install = "vietnam_compliance.patches.check_version_compatibility.execute"
after_install = "vietnam_compliance.install.after_install"
before_uninstall = "vietnam_compliance.uninstall.before_uninstall"

after_app_install = "vietnam_compliance.install.after_app_install"
before_app_uninstall = "vietnam_compliance.uninstall.before_app_uninstall"

before_migrate = "vietnam_compliance.patches.check_version_compatibility.execute"
after_migrate = "vietnam_compliance.audit_trail.setup.after_migrate"

before_tests = "vietnam_compliance.tests.before_tests"

boot_session = "vietnam_compliance.boot.set_bootinfo"

app_include_js = "vietnam_compliance.bundle.js"

doctype_js = {
    "Address": [
        "vat_vietnam/client_scripts/party.js",
        "vat_vietnam/client_scripts/address.js",
    ],
    "Company": [
        "vat_vietnam/client_scripts/party.js",
        "vat_vietnam/client_scripts/company.js",
    ],
    "Customer": [
        "vat_vietnam/client_scripts/party.js",
        "vat_vietnam/client_scripts/customer.js",
    ],
    "Item": "vat_vietnam/client_scripts/item.js",
    "Item Tax Template": "vat_vietnam/client_scripts/item_tax_template.js",
    "Payment Entry": "vat_vietnam/client_scripts/payment_entry.js",
    "Purchase Invoice": [
        "vat_vietnam/client_scripts/purchase_invoice.js",
    ],
    "Sales Invoice": [
        "vat_vietnam/client_scripts/e_invoice_actions.js",
        "vat_vietnam/client_scripts/sales_invoice.js",
    ],
    "Tax Category": "vat_vietnam/client_scripts/tax_category.js",
    "Accounts Settings": "audit_trail/client_scripts/accounts_settings.js",
    "Customize Form": "audit_trail/client_scripts/customize_form.js",
}

doctype_list_js = {
    "Sales Invoice": [
        "vat_vietnam/client_scripts/sales_invoice_list.js",
    ]
}

doc_events = {
    "Address": {
        "validate": [
            "vietnam_compliance.vat_vietnam.overrides.address.validate",
        ],
        "on_update": [
            "vietnam_compliance.vat_vietnam.overrides.address.update_party_tax_info",
        ],
    },
    "Company": {
        "on_update": [
            "vietnam_compliance.vat_vietnam.overrides.company.make_company_fixtures",
        ],
        "validate": "vietnam_compliance.vat_vietnam.overrides.party.validate_party",
    },
    "Customer": {
        "validate": "vietnam_compliance.vat_vietnam.overrides.party.validate_party",
        "after_insert": "vietnam_compliance.vat_vietnam.overrides.party.create_primary_address",
    },
    "GL Entry": {
        "validate": "vietnam_compliance.vat_vietnam.overrides.gl_entry.validate",
    },
    "Item": {
        "validate": "vietnam_compliance.vat_vietnam.overrides.item.validate",
    },
    "Item Tax Template": {
        "validate": "vietnam_compliance.vat_vietnam.overrides.item_tax_template.validate",
    },
    "Payment Entry": {
        "onload": "vietnam_compliance.vat_vietnam.overrides.payment_entry.onload",
        "validate": "vietnam_compliance.vat_vietnam.overrides.payment_entry.validate",
        "on_submit": "vietnam_compliance.vat_vietnam.overrides.payment_entry.on_submit",
        "before_cancel": "vietnam_compliance.vat_vietnam.overrides.payment_entry.before_cancel",
    },
    "Purchase Invoice": {
        "onload": [
            "vietnam_compliance.vat_vietnam.overrides.purchase_invoice.onload",
            "vietnam_compliance.vat_vietnam.overrides.transaction.onload",
        ],
        "before_validate": [
            "vietnam_compliance.vat_vietnam.overrides.transaction.before_validate_transaction",
        ],
        "validate": "vietnam_compliance.vat_vietnam.overrides.purchase_invoice.validate",
        "before_save": "vietnam_compliance.vat_vietnam.overrides.transaction.update_valuation_rate",
        "before_submit": "vietnam_compliance.vat_vietnam.overrides.transaction.update_valuation_rate",
        "after_mapping": "vietnam_compliance.vat_vietnam.overrides.transaction.after_mapping",
        "on_cancel": "vietnam_compliance.vat_vietnam.overrides.purchase_invoice.on_cancel",
    },
    "Sales Invoice": {
        "onload": [
            "vietnam_compliance.vat_vietnam.overrides.sales_invoice.onload",
            "vietnam_compliance.vat_vietnam.overrides.transaction.onload",
        ],
        "before_print": "vietnam_compliance.vat_vietnam.overrides.transaction.before_print",
        "before_validate": "vietnam_compliance.vat_vietnam.overrides.transaction.before_validate_transaction",
        "validate": "vietnam_compliance.vat_vietnam.overrides.sales_invoice.validate",
        "on_submit": "vietnam_compliance.vat_vietnam.overrides.sales_invoice.on_submit",
        "before_update_after_submit": "vietnam_compliance.vat_vietnam.overrides.transaction.sync_address_dependent_fields_on_submit",
        "on_update_after_submit": "vietnam_compliance.vat_vietnam.overrides.sales_invoice.on_update_after_submit",
        "before_cancel": [
            "vietnam_compliance.vat_vietnam.overrides.sales_invoice.before_cancel"
        ],
        "after_mapping": "vietnam_compliance.vat_vietnam.overrides.transaction.after_mapping",
    },
    "Accounts Settings": {
        "validate": "vietnam_compliance.audit_trail.overrides.accounts_settings.validate"
    },
    "Property Setter": {
        "validate": "vietnam_compliance.audit_trail.overrides.property_setter.validate",
        "on_trash": "vietnam_compliance.audit_trail.overrides.property_setter.on_trash",
    },
    "Version": {
        "validate": "vietnam_compliance.audit_trail.overrides.version.validate",
        "on_trash": "vietnam_compliance.audit_trail.overrides.version.on_trash",
    },
}

regional_overrides = {
    "Vietnam": {
        "erpnext.accounts.party.get_regional_address_details": (
            "vietnam_compliance.vat_vietnam.overrides.transaction.update_party_details"
        ),
    }
}

jinja = {
    "methods": [
        "vietnam_compliance.vat_vietnam.utils.get_state",
        "vietnam_compliance.vat_vietnam.utils.jinja.get_e_invoice_qr_code",
    ],
}

override_doctype_dashboards = {
    "Sales Invoice": "vietnam_compliance.vat_vietnam.overrides.sales_invoice.get_dashboard_data",
}

override_doctype_class = {
    "Customize Form": "vietnam_compliance.audit_trail.overrides.customize_form.CustomizeForm",
}

company_data_to_be_ignored = []
ignore_links_on_delete = ["EInvoiceLog"]

accounting_dimension_doctypes = []

audit_trail_doctypes = [
    "Accounts Settings",
    "Journal Entry",
    "Payment Entry",
    "Purchase Invoice",
    "Sales Invoice",
]

scheduler_events = {
    "cron": {
        "*/5 * * * *": [
            "vietnam_compliance.vat_vietnam.utils.e_invoice.retry_e_invoice_generation",
        ],
    }
}

override_whitelisted_methods = {
    "erpnext.accounts.doctype.payment_entry.payment_entry.get_outstanding_reference_documents": (
        "vietnam_compliance.vat_vietnam.overrides.payment_entry.get_outstanding_reference_documents"
    )
}

require_type_annotated_api_methods = True
