from lxml import etree


def generate_e_invoice_xml(sales_invoice_doc):
    """Generate Vietnam e-invoice XML per Circular 78/2021/TT-BTC schema.

    Args:
        sales_invoice_doc: Frappe Sales Invoice document

    Returns:
        str: XML string ready for signing
    """
    nsmap = {
        None: "http://hoadondientu.gdt.gov.vn",
        "xsi": "http://www.w3.org/2001/XMLSchema-instance",
    }

    root = etree.Element("HoaDon", nsmap=nsmap)
    root.set(
        "{http://www.w3.org/2001/XMLSchema-instance}schemaLocation",
        "http://hoadondientu.gdt.gov.vn hoadon.xsd",
    )

    _add_header(root, sales_invoice_doc)
    _add_seller_info(root, sales_invoice_doc)
    _add_buyer_info(root, sales_invoice_doc)
    _add_items(root, sales_invoice_doc)
    _add_totals(root, sales_invoice_doc)

    return etree.tostring(root, encoding="unicode", pretty_print=True)


def _add_header(root, doc):
    dlhdon = etree.SubElement(root, "DLHDon")
    etree.SubElement(dlhdon, "MauSo").text = doc.get("custom_invoice_form_number", "")
    etree.SubElement(dlhdon, "KyHieu").text = doc.get("custom_invoice_series", "")
    etree.SubElement(dlhdon, "So").text = doc.name or ""
    etree.SubElement(dlhdon, "Ngay").text = str(doc.posting_date) if doc.posting_date else ""
    etree.SubElement(dlhdon, "LoaiHD").text = doc.get("custom_einvoice_type", "Có mã CQT")


def _add_seller_info(root, doc):
    nb = etree.SubElement(root, "NB")
    company = doc.company
    etree.SubElement(nb, "Ten").text = doc.company_name or ""
    etree.SubElement(nb, "MST").text = doc.get("company_mst", "")
    etree.SubElement(nb, "DiaChi").text = doc.company_address_display or ""


def _add_buyer_info(root, doc):
    nm = etree.SubElement(root, "NM")
    etree.SubElement(nm, "Ten").text = doc.customer_name or ""
    customer_mst = doc.get("customer_mst", "")
    if customer_mst:
        etree.SubElement(nm, "MST").text = customer_mst
    etree.SubElement(nm, "DiaChi").text = doc.customer_address or ""


def _add_items(root, doc):
    ds = etree.SubElement(root, "DSHHDVu")
    for item in doc.items:
        hhdv = etree.SubElement(ds, "HHDVu")
        etree.SubElement(hhdv, "Ten").text = item.item_name or ""
        etree.SubElement(hhdv, "DVT").text = item.uom or ""
        etree.SubElement(hhdv, "SL").text = str(item.qty or 1)
        etree.SubElement(hhdv, "DGia").text = str(item.rate or 0)
        etree.SubElement(hhdv, "Tien").text = str(item.amount or 0)
        etree.SubElement(hhdv, "TSuat").text = str(_get_tax_rate(item))


def _add_totals(root, doc):
    etree.SubElement(root, "TongTien").text = str(doc.total or 0)
    etree.SubElement(root, "TongTienThue").text = str(doc.total_taxes_and_charges or 0)
    etree.SubElement(root, "TongTienThanhToan").text = str(doc.grand_total or 0)
    etree.SubElement(root, "TienBangChu").text = doc.in_words or ""


def _get_tax_rate(item):
    return getattr(item, "vat_rate", 0) or 0


def generate_qr_code_data(doc):
    data = {
        "mst": doc.get("company_mst", ""),
        "so": doc.name,
        "ngay": str(doc.posting_date),
        "tong": str(doc.grand_total),
    }
    return "|".join(f"{k}={v}" for k, v in data.items())
