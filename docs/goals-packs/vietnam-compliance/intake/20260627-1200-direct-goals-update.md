# Direct Goals Update Intake Log

- **Timestamp:** 2026-06-27 12:00 UTC
- **Prompt:** PR-GP-Direct-Goals-File-From-Repo-And-Instructions
- **Direct Update Mode:** initialize-or-update
- **Auto Accept Suggested:** no
- **Continue Execution After Update:** no

## Preflight

- **cwd:** /Users/thanhson/Workspace/abn.platform.erp.base.vietnam-compliance
- **git branch:** main
- **git status:** clean, up to date with origin/main
- **WORK_THOUGHTS_ISSUE:** https://github.com/stevennt/abn.platform.erp.base.vietnam-compliance/issues/2

## Context

- **Ecosystem Context Used:** N/A — this is a standalone Frappe app (Python/JS) that runs inside ERPNext v16 with its own MariaDB. Does NOT use Axum API server, abn.postgresql, OneID, or OneWorkflow.
- **Source Issue:** https://github.com/stevennt/abn.platform.erp.base/issues/9 — full codebase analysis
- **Plan:** PLAN.md at repo root — 5-phase conversion roadmap
- **Source Repo (India Compliance):** https://github.com/resilient-tech/india-compliance (4,893 commits, 257 releases)

## Repo Research Summary

### Evidence Found

| Item | Evidence |
|------|----------|
| India Compliance source | 372 .py files, ~70K Python LOC, ~16K JS LOC, 24 custom doctypes |
| Hook architecture | `india_compliance/hooks.py`: 647 lines, overrides ~30 ERPNext doctypes via doc_events |
| Custom fields | `gst_india/constants/custom_fields.py`: 1,802 lines, patches Sales Invoice, Company, Party, etc. |
| API integration | `gst_india/api_classes/nic/e_invoice.py`: NIC portal integration for India e-Invoice |
| e-Invoice flow | `gst_india/utils/e_invoice.py`: 1,023 lines — IRN generation, cancellation, retry |
| Workspace | `gst_india/workspace/gst_india/`: Frappe Desk workspace dashboard |
| Reports | `gst_india/report/`: 15+ GST reports |
| Scheduler | Cron jobs for auto-generate, retry, reconciliation (every 5 min, daily) |
| Multi-tenant | `docs/developer-guide/multi-site-setup`: global API secret via `bench set-config -g` |
| PLAN.md | 326 lines — delete/rewrite/keep mapping, 5 implementation phases |
| No existing goals file | `docs/goals-packs/` does not exist yet |

### Modules to DELETE (India-only)

- e-Waybill (entire module, no VN equivalent)
- GST Returns GSTR-1/3B
- Purchase Reconciliation 2A/2B
- ITC Classification / Ineligible ITC
- Reverse Charge (RCM)
- TDS/TCS (Income Tax India)
- HSN Code system
- Bill of Entry
- PAN doctype
- State-wise e-Waybill threshold

### Modules to REWRITE

- `india_compliance/gst_india/` → `vietnam_compliance/vat_vietnam/`
- `GSTSettings` → `TaxDepartmentConfig`
- `GSTIN` → `MST`
- `EInvoiceAPI` (NIC) → `GDTEInvoiceAPI` (TCT Vietnam)
- `e_invoice.py` → same name, entirely different XML/API logic

### Modules to KEEP (architectural patterns)

- `hooks.py` pattern
- `install.py`/`uninstall.py`/`setup/` flow
- `custom_fields.py` approach
- `api_classes/base.py`
- `exceptions.py`
- `boot.py`
- Client scripts pattern
- Override pattern (doc_events)
- Scheduler cron pattern
- Multi-site global config pattern
- Workspace/Desk UI pattern

### What ERPNext Provides (no changes needed)

- Sales Invoice, Purchase Invoice, Customer, Supplier, Company doctypes
- Tax engine (GTGT 0%, 5%, 8%, 10%)
- Print Format (Jinja + HTML)
- Multi-company / Multi-site
- Naming Series
- Address
- Dashboard/report system
- Frappe cron/scheduler
- Webhook/API framework

### What Must Be Built New

1. GDT portal API client
2. Vietnam XML schema generator (Thông tư 78)
3. Digital signature integration (ký số)
4. Mẫu số + Ký hiệu management
5. QR code for tra cứu
6. Hóa đơn điều chỉnh/thay thế workflow
7. Báo cáo tình hình sử dụng HĐĐT
8. Province/tax authority codes (63 provinces)

### Technical Foundation Assessment

- The repo already has a Frappe app structure (india_compliance/ with hooks.py, public/, templates/, setup/ etc.)
- PMO/platform setup: NOT applicable — this is an existing Frappe app, not a Flutter/Next.js/etc. project
- Need to rename app from india_compliance to vietnam_compliance
- Need to update hooks.py metadata, remove required_apps dependency

### Ecosystem Reuse Decisions

- Axum API: NOT needed — Frappe provides its own API layer
- abn.postgresql: NOT needed — Frappe uses MariaDB internally
- OneID Auth: NOT needed — Frappe has its own auth
- OneWorkflow: NOT needed — Frappe has document workflow
- This is a fully self-contained Frappe app

### # Direct Goals Update Intake Log (continued)

## Candidate Goals Classification

From PLAN.md + Issue #9, mapped to goals:

| Candidate | Classification | Source |
|-----------|---------------|--------|
| P0: Scaffold vietnam_compliance app (rename, strip India code, update metadata) | NEW | user (PLAN.md Phase 1) |
| P0: Vietnam constants (provinces, tax rates, invoice types) | NEW | user (PLAN.md Phase 1) |
| P0: TaxDepartmentConfig doctype (replaces GST Settings) | NEW | user (PLAN.md Phase 2) |
| P0: MST doctype (replaces GSTIN) | NEW | user (PLAN.md Phase 2) |
| P0: EInvoiceLog doctype (rewrite statuses) | NEW | user (PLAN.md Phase 2) |
| P0: Custom fields on Sales Invoice (einvoice_status, transaction_id, form_number, series, etc.) | NEW | user (PLAN.md Phase 2) |
| P0: Custom fields on Company (MST, digital cert, GDT credentials) | NEW | user (PLAN.md Phase 2) |
| P1: GDT API client (authentication, submit, status, cancel) | NEW | user (PLAN.md Phase 3) |
| P1: Vietnam XML e-invoice schema generator | NEW | user (PLAN.md Phase 3) |
| P1: Digital signature integration (mock first, real later) | NEW | user (PLAN.md Phase 3) |
| P1: Sales Invoice client scripts (e-invoice actions, status UI) | NEW | user (PLAN.md Phase 4) |
| P1: Vietnam e-invoice print format (Thông tư 78 template) | NEW | user (PLAN.md Phase 4) |
| P1: VAT Vietnam workspace (dashboard) | NEW | user (PLAN.md Phase 4) |
| P1: Invoice adjustment/replacement workflow | NEW | user (PLAN.md Phase 4) |
| P2: Báo cáo tình hình sử dụng HĐĐT | NEW | user (PLAN.md Phase 5) |
| P2: Bảng kê hóa đơn bán ra / mua vào | NEW | user (PLAN.md Phase 5) |
| P2: Scheduler jobs (auto-retry, auto-generate, cert expiry) | NEW | user (PLAN.md Phase 5) |
| P2: Multi-tenant setup docs (global config pattern) | NEW | user (PLAN.md Phase 5) |
| SUGGESTED: Automated tests for e-invoice flow | SUGGESTED | agent |
| SUGGESTED: GDT sandbox mode for integration testing | SUGGESTED | agent |
| SUGGESTED: API usage dashboard for multi-tenant operators | SUGGESTED | agent |

## Uncertainty

- GDT API documentation availability (may need to work with unofficial/community docs)
- GDT sandbox environment access
- Digital signing provider selection (VNPT vs Viettel vs BKAV)
- Exact XML schema version per latest Circular updates

## Source File References

- `/Users/thanhson/Workspace/abn.platform.erp.base.vietnam-compliance/PLAN.md`
- `/Users/thanhson/Workspace/abn.platform.erp.base.vietnam-compliance/india_compliance/hooks.py`
- `/Users/thanhson/Workspace/abn.platform.erp.base.vietnam-compliance/india_compliance/gst_india/constants/custom_fields.py`
- `/Users/thanhson/Workspace/abn.platform.erp.base.vietnam-compliance/india_compliance/gst_india/utils/e_invoice.py`
- `/Users/thanhson/Workspace/abn.platform.erp.base.vietnam-compliance/india_compliance/gst_india/setup/__init__.py`
- `https://github.com/stevennt/abn.platform.erp.base/issues/9`

## What Was Not Inspected

- Full deep read of all 372 .py files (sampled key architectural files)
- Individual report implementations (inspected file list, not contents)
- Print format HTML templates
- Client-side JS scripts in detail
- Test files (only 2 exist)
