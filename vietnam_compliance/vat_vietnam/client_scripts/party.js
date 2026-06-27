function update_mst_in_other_documents(doctype) {
    frappe.ui.form.on(doctype, {
        after_save(frm) {
            const { docs_with_previous_mst, previous_mst } = frappe.last_response || {};
            if (!docs_with_previous_mst) return;

            const { mst } = frm.doc;
            let message = __(
                "Bạn đang dùng MST <strong>{0}</strong> trong các chứng từ sau:<br>",
                [previous_mst]
            );

            for (const [doctype, docnames] of Object.entries(docs_with_previous_mst)) {
                message += `<br><strong>${__(doctype)}</strong>:<br>`;
                docnames.forEach((docname) => {
                    message += `${frappe.utils.get_form_link(doctype, docname, true)}<br>`;
                });
            }
            message += `<br>Bạn có muốn cập nhật MST mới?<br><br><strong>MST:</strong> ${mst || "&lt;trống&gt;"}`;

            frappe.confirm(message, function () {
                frappe.call({
                    method: "vietnam_compliance.vat_vietnam.overrides.party.update_docs_with_previous_mst",
                    args: {
                        mst: mst || "",
                        docs_with_previous_mst,
                    },
                });
            });
        },
    });
}

function validate_mst_input(doc, cdt, cdn) {
    const d = locals[cdt][cdn];
    if (d.mst && !/^\d{10}(\d{3})?$/.test(d.mst)) {
        frappe.msgprint(__("Mã số thuế không hợp lệ. Phải có 10 hoặc 13 chữ số."));
        frappe.validated = false;
    }
}

update_mst_in_other_documents("Customer");
update_mst_in_other_documents("Supplier");
update_mst_in_other_documents("Company");
