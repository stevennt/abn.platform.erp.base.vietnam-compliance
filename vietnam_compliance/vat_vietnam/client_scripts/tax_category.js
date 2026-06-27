frappe.ui.form.on("Tax Category", {
    refresh: set_field_states,
    gst_state(frm) {
        if (frm.doc.gst_state && frm.doc.is_vietnam_compliance_default) {
            frm.set_value("is_vietnam_compliance_default", 0);
        }
        set_field_states(frm);
    },
    is_vietnam_compliance_default(frm) {
        if (frm.doc.is_vietnam_compliance_default && frm.doc.gst_state) {
            frm.set_value("gst_state", "");
        }
        set_field_states(frm);
    },
});

function set_field_states(frm) {
    frm.set_df_property("is_vietnam_compliance_default", "read_only", Boolean(frm.doc.gst_state));
    frm.set_df_property("gst_state", "read_only", Boolean(frm.doc.is_vietnam_compliance_default));
}
