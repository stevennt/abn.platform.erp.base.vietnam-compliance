# Multi-Site Setup — Vietnam Compliance

## Overview

Vietnam Compliance supports multi-tenant e-invoicing across multiple Frappe sites. Each client company gets its own Frappe site (separate database) with independent MST, GDT credentials, and digital certificate.

This follows the same architecture pattern as India Compliance's multi-site setup.

## Global Configuration

Set shared GDT API settings across all sites using bench global config:

```sh
# Set common GDT API URL for all sites
bench set-config -g gdt_api_url "https://hoadondientu.gdt.gov.vn"

# Enable sandbox mode globally
bench set-config -g gdt_sandbox_mode 1

# Set sandbox URL
bench set-config -g gdt_sandbox_url "https://hoadondientutest.gdt.gov.vn"
```

## Per-Company Configuration

Each Company doctype stores its own:
- **MST** (Mã số thuế): 10 or 13 digit tax code
- **Digital Certificate Reference**: USB Token ID or HSM key ID
- **GDT Username/Password**: Portal login credentials (stored encrypted)
- **Invoice Form Numbers**: Allowed form numbers (01GTKT0/001, etc.)
- **Default Invoice Type**: Có mã CQT or Không mã CQT

Credentials are stored in Frappe's encrypted Password fields and are never exposed in plaintext.

## Installation per Site

```sh
# Get the app
bench get-app https://github.com/stevennt/abn.platform.erp.base.vietnam-compliance.git

# Install on a site
bench --site client-site.example.com install-app vietnam_compliance

# Migrate
bench --site client-site.example.com migrate
```

## SaaS Deployment

For a multi-tenant SaaS platform (like MISA/BKAV/FPT e-invoice):

1. **One Frappe site per client company** — maximum data isolation
2. Shared Frappe bench with N sites (each ~200MB RAM per site)
3. Global config for shared infrastructure settings
4. Per-site GDT credentials via Company doctype
5. Separate MariaDB database per site (Frappe default)

## Security Notes

- GDT passwords stored in Frappe encrypted Password fields
- Digital certificate keys NEVER stored in the database
- Signing services (VNPT/Viettel/BKAV) accessed via API, not local key material
- Production deployment requires SSL/TLS for all GDT API communication

## Verification

After installation, verify:
1. Tax Department Config appears in Frappe Desk
2. Company form shows MST + GDT credential fields
3. Sales Invoice shows e-invoice section with VN fields
4. VAT Vietnam workspace is accessible
