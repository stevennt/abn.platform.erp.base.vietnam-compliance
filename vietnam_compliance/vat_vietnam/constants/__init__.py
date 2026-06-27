import re

from erpnext.stock.get_item_details import sales_doctypes

TIMEZONE = "Asia/Ho_Chi_Minh"

ABBREVIATIONS = {"VAT", "GTGT", "MST", "HDDT", "CQT", "GDT"}

VAT_ACCOUNT_FIELDS = (
    "vat_account",
)

VAT_RATES = (0, 5, 8, 10)

VAT_PARTY_TYPES = ("Customer", "Supplier", "Company")

INVOICE_TYPES = {
    "Có mã CQT": "CODED",
    "Không mã CQT": "UNCODED",
}

INVOICE_TYPE_CHOICES = "\n".join(INVOICE_TYPES)

INVOICE_FORM_TEMPLATES = {
    "01GTKT0/001": "Hóa đơn giá trị gia tăng (có mã)",
    "01GTKT0/002": "Hóa đơn giá trị gia tăng (không mã)",
    "02GTTT0/001": "Hóa đơn bán hàng (có mã)",
    "02GTTT0/002": "Hóa đơn bán hàng (không mã)",
}

EINVOICE_STATUSES = {
    "Pending": "Chờ gửi",
    "Submitted": "Đã gửi CQT",
    "Coded": "CQT cấp mã",
    "Generated": "Đã có mã",
    "Failed": "Lỗi",
    "Cancelled": "Đã hủy",
    "ManuallyGenerated": "Tạo thủ công",
    "PendingCancellation": "Chờ hủy",
    "NotApplicable": "Không áp dụng",
}

EINVOICE_STATUS_CHOICES = (
    "\nChờ gửi\nĐã gửi CQT\nCQT cấp mã\nĐã có mã\nLỗi\nĐã hủy\nTạo thủ công\nChờ hủy\nKhông áp dụng"
)

CANCEL_REASON_CODES = {
    "Sai thông tin": "1",
    "Hủy đơn hàng": "2",
    "Sai sót nghiệp vụ": "3",
    "Khác": "4",
}

ADJUSTMENT_TYPES = {
    "Điều chỉnh": "ADJUSTMENT",
    "Thay thế": "REPLACEMENT",
    "Hủy": "CANCELLATION",
}

ACTION_MAP = {"A": "Accepted", "R": "Rejected", "P": "Pending", "N": "No Action"}

STATUS_CODE_MAP = {
    "P": "Processed",
    "PE": "Processed with Errors",
    "ER": "Error",
    "IP": "In Progress",
}

MST_FORMAT = re.compile(r"^\d{10}(\d{3})?$")

SALES_DOCTYPES = tuple(sales_doctypes)

PROVINCES = {
    "An Giang": "89",
    "Bà Rịa - Vũng Tàu": "77",
    "Bạc Liêu": "99",
    "Bắc Kạn": "06",
    "Bắc Giang": "24",
    "Bắc Ninh": "27",
    "Bến Tre": "83",
    "Bình Dương": "74",
    "Bình Định": "52",
    "Bình Phước": "70",
    "Bình Thuận": "80",
    "Cà Mau": "98",
    "Cao Bằng": "04",
    "Cần Thơ": "92",
    "Đà Nẵng": "48",
    "Đắk Lắk": "66",
    "Đắk Nông": "67",
    "Điện Biên": "11",
    "Đồng Nai": "75",
    "Đồng Tháp": "87",
    "Gia Lai": "64",
    "Hà Giang": "02",
    "Hà Nam": "35",
    "Hà Nội": "01",
    "Hà Tĩnh": "48",
    "Hải Dương": "34",
    "Hải Phòng": "31",
    "Hậu Giang": "95",
    "Hòa Bình": "23",
    "Hồ Chí Minh": "79",
    "Hưng Yên": "33",
    "Khánh Hòa": "56",
    "Kiên Giang": "91",
    "Kon Tum": "62",
    "Lai Châu": "12",
    "Lạng Sơn": "20",
    "Lào Cai": "10",
    "Lâm Đồng": "68",
    "Long An": "80",
    "Nam Định": "36",
    "Nghệ An": "40",
    "Ninh Bình": "37",
    "Ninh Thuận": "58",
    "Phú Thọ": "25",
    "Phú Yên": "54",
    "Quảng Bình": "44",
    "Quảng Nam": "49",
    "Quảng Ngãi": "51",
    "Quảng Ninh": "22",
    "Quảng Trị": "45",
    "Sóc Trăng": "94",
    "Sơn La": "14",
    "Tây Ninh": "72",
    "Thái Bình": "36",
    "Thái Nguyên": "19",
    "Thanh Hóa": "38",
    "Thừa Thiên Huế": "46",
    "Tiền Giang": "82",
    "Trà Vinh": "84",
    "Tuyên Quang": "08",
    "Vĩnh Long": "86",
    "Vĩnh Phúc": "26",
    "Yên Bái": "15",
    "Nước ngoài": "99",
}

PROVINCE_CHOICES = "\n".join(f"{code} - {name}" for name, code in PROVINCES.items())

PORT_CODES = {}

EXPORT_TYPES = ("NOT_EXPORT",)

CURRENCY_CODES = {"VND": "704"}

SERVICE_VAT_PREFIX = "00000"

VALID_VAT_LENGTHS = [10, 13]

GDT_API_URL = "https://hoadondientu.gdt.gov.vn"

GDT_SANDBOX_URL = "https://hoadondientutest.gdt.gov.vn"
BUG_REPORT_URL = "https://github.com/stevennt/abn.platform.erp.base.vietnam-compliance/issues"

GST_UOMS = {}
GST_ACCOUNT_FIELDS = ("vat_account",)
GST_PARTY_TYPES = VAT_PARTY_TYPES
TAXABLE_GST_TREATMENTS = ("Taxable", "Zero-Rated")
SALES_DOCTYPES = tuple(sales_doctypes)
SUBCONTRACTING_DOCTYPES = ()
GST_RCM_TAX_TYPES = ()
GST_REFUND_TAX_TYPES = ()
GST_TAX_TYPES = ("vat",)
TAX_TYPES = ("vat",)
STATE_NUMBERS = PROVINCES
