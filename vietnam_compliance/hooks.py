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

before_tests = None

boot_session = "vietnam_compliance.boot.set_bootinfo"

app_include_js = "vietnam_compliance.bundle.js"

doctype_js = {
    "Sales Invoice": [
        "vat_vietnam/client_scripts/sales_invoice.js",
        "vat_vietnam/client_scripts/e_invoice_actions.js",
    ],
    "Purchase Invoice": [],
    "Customer": [],
    "Supplier": [],
    "Company": [],
    "Item": [],
    "Item Tax Template": [],
    "Address": [],
    "Tax Category": [],
    "Payment Entry": [],
}

doctype_list_js = {}

doc_events = {
    "Sales Invoice": {
        "onload": "vietnam_compliance.vat_vietnam.overrides.sales_invoice.onload",
        "validate": "vietnam_compliance.vat_vietnam.overrides.sales_invoice.validate",
        "on_submit": "vietnam_compliance.vat_vietnam.overrides.sales_invoice.on_submit",
        "before_cancel": "vietnam_compliance.vat_vietnam.overrides.sales_invoice.before_cancel",
        "on_update_after_submit": "vietnam_compliance.vat_vietnam.overrides.sales_invoice.on_update_after_submit",
    },
    "Accounts Settings": {
        "validate": None,
    },
}

override_doctype_dashboards = {
    "Sales Invoice": "vietnam_compliance.vat_vietnam.overrides.sales_invoice.get_dashboard_data",
}

company_data_to_be_ignored = []
ignore_links_on_delete = ["EInvoiceLog"]

audit_trail_doctypes = [
    "Accounts Settings",
    "Sales Invoice",
]

scheduler_events = {
    "cron": {
        "*/5 * * * *": [
            "vietnam_compliance.vat_vietnam.utils.e_invoice.retry_e_invoice_generation",
        ],
    }
}

require_type_annotated_api_methods = True
