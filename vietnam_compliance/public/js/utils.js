frappe.provide("vietnam_compliance");
const VN = vietnam_compliance;

VN.MST_REGEX = /^\d{10}(\d{3})?$/;

VN.validate_mst = function (mst) {
    if (!mst) return __("Mã số thuế không được để trống");
    if (!VN.MST_REGEX.test(mst)) return __("Mã số thuế phải có 10 hoặc 13 chữ số");
    return null;
};

VN.get_e_invoice_status_color = function (status) {
    const colors = {
        "Chờ gửi": "orange",
        "Đã gửi CQT": "blue",
        "CQT cấp mã": "green",
        "Đã có mã": "green",
        "Lỗi": "red",
        "Đã hủy": "gray",
        "Chờ hủy": "orange",
        "Không áp dụng": "gray",
    };
    return colors[status] || "gray";
};
