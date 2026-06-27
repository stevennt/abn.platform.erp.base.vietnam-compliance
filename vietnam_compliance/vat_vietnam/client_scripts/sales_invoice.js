const DOCTYPE = "Sales Invoice";

frappe.ui.form.on(DOCTYPE, {
    setup(frm) {
        frm.set_query("adjusted_invoice", (doc) => {
            return {
                filters: {
                    name: ["!=", doc.name],
                    docstatus: 1,
                    custom_einvoice_status: ["in", ["CQT cấp mã", "Đã có mã"]],
                },
            };
        });
    },

    before_submit(frm) {
        frm.doc._submitted_from_ui = 1;
    },

    refresh(frm) {
        if (frm.is_new()) return;
        _add_einvoice_actions(frm);
        _show_einvoice_status(frm);
    },

    after_save(frm) {
        if (frm.doc.docstatus === 1 && frm.doc.custom_einvoice_status === "Chờ gửi") {
            _show_generate_dialog(frm);
        }
    },
});

function _add_einvoice_actions(frm) {
    if (!frm.doc.__islocal && frm.doc.docstatus === 1) {
        const status = frm.doc.custom_einvoice_status;

        if (!status || status === "Chờ gửi" || status === "Lỗi") {
            frm.add_custom_button(__("Gửi CQT"), () => _submit_to_gdt(frm), __("HĐĐT"));
        }

        if (status && !["Đã hủy", "Chờ hủy"].includes(status)) {
            frm.add_custom_button(__("Hủy HĐ"), () => _cancel_einvoice(frm), __("HĐĐT"));
        }

        if (status) {
            frm.add_custom_button(__("Kiểm tra trạng thái"), () => _check_status(frm), __("HĐĐT"));
        }
    }

    if (frm.is_new()) {
        _set_default_einvoice_settings(frm);
    }
}

function _submit_to_gdt(frm) {
    frappe.confirm(
        __("Xác nhận gửi hóa đơn lên Cổng Dịch vụ Thuế?"),
        () => {
            frappe.call({
                method: "vietnam_compliance.vat_vietnam.api_classes.gdt.e_invoice.enqueue_bulk_e_invoice_generation",
                args: { docnames: [frm.doc.name] },
                callback: () => {
                    frappe.show_alert({ message: __("Đã gửi yêu cầu phát hành HĐĐT"), indicator: "green" });
                    frm.refresh();
                },
            });
        }
    );
}

function _cancel_einvoice(frm) {
    frappe.prompt(
        [
            {
                fieldname: "reason",
                fieldtype: "Select",
                label: __("Lý do hủy"),
                options: ["Sai thông tin", "Hủy đơn hàng", "Sai sót nghiệp vụ", "Khác"],
                reqd: 1,
            },
        ],
        (values) => {
            frappe.call({
                method: "vietnam_compliance.vat_vietnam.utils.e_invoice.cancel_e_invoice",
                args: { docname: frm.doc.name, reason: values.reason },
                callback: () => {
                    frappe.show_alert({ message: __("Đã yêu cầu hủy HĐĐT"), indicator: "orange" });
                    frm.refresh();
                },
            });
        },
        __("Hủy hóa đơn điện tử"),
        __("Xác nhận")
    );
}

function _check_status(frm) {
    frappe.call({
        method: "vietnam_compliance.vat_vietnam.utils.e_invoice.check_e_invoice_status",
        args: { docname: frm.doc.name },
        callback: (r) => {
            if (r.message) {
                frappe.show_alert({
                    message: __("Trạng thái: {0}", [r.message.status || __("Không xác định")]),
                    indicator: r.message.status === "CQT cấp mã" ? "green" : "blue",
                });
                frm.refresh();
            }
        },
    });
}

function _show_einvoice_status(frm) {
    const status = frm.doc.custom_einvoice_status;
    if (!status) return;

    const colors = {
        "Chờ gửi": "orange",
        "Đã gửi CQT": "blue",
        "CQT cấp mã": "green",
        "Đã có mã": "green",
        "Lỗi": "red",
        "Đã hủy": "gray",
        "Chờ hủy": "orange",
    };

    const color = colors[status] || "gray";
    frm.dashboard.add_indicator(__(status), color);
}

function _set_default_einvoice_settings(frm) {
    frappe.db.get_single_value("Tax Department Config", "enable_e_invoice").then((enabled) => {
        if (enabled) {
            frappe.model.set_value(frm.doc.doctype, frm.doc.name, "custom_einvoice_status", "Chờ gửi");
        }
    });
}

function _show_generate_dialog(frm) {
    frappe.confirm(
        __("Bạn có muốn tự động gửi HĐĐT lên CQT không?"),
        () => _submit_to_gdt(frm)
    );
}
