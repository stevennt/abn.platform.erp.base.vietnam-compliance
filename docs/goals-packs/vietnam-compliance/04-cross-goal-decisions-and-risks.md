# Vietnam Compliance — Cross-Goal Decisions and Risks

Last updated: 2026-06-27 12:00

## Architecture Decisions

### AD-001: Add-on to ERPNext, not standalone
- **Decision:** Vietnam Compliance is a Frappe app add-on to ERPNext v16, following India Compliance pattern.
- **Rationale:** ERPNext already provides Sales Invoice, Purchase Invoice, Customer, Company, Tax engine, Print Format, Multi-company, Scheduler. Building standalone would duplicate all of this.
- **Evidence:** PLAN.md Section 0 — 80% of what we need exists in ERPNext.
- **Impact:** All goals target Frappe hooks (doc_events, custom fields, overrides). No standalone API server, no separate database.

### AD-002: Delete India code, don't comment out
- **Decision:** India-only modules are deleted entirely, not commented out or archived in-place.
- **Rationale:** Commented-out code becomes dead weight and confusion. The India source remains available in the original repo and git history.
- **Evidence:** PLAN.md DELETE list — ~15 modules to remove.

### AD-003: Mock-first for GDT API and digital signature
- **Decision:** GDT API client and digital signature use mock/sandbox implementations initially. Real integration deferred until GDT documentation and sandbox credentials available.
- **Rationale:** Development can proceed without blocking on external dependencies. Mock responses allow end-to-end testing of the override and UI flow.
- **Risk:** Real GDT API contract may differ from assumptions. Adjust when sandbox access obtained.

### AD-004: One Frappe site per client for SaaS
- **Decision:** Multi-tenant SaaS deployment uses one Frappe site per client company (separate MariaDB databases).
- **Rationale:** Maximum data isolation, independent backup/restore, separate GDT credentials per site. Follows India Compliance multi-site pattern.
- **Alternative Considered:** Multi-company within single site — lighter but weaker isolation.
- **Evidence:** India Compliance docs/developer-guide/multi-site-setup.

### AD-005: Frappe app is standalone from ABN ecosystem
- **Decision:** This Frappe app does NOT use Axum API server, abn.postgresql, OneID Auth, or OneWorkflow.
- **Rationale:** Frappe/ERPNext provides its own API layer (Frappe REST API), database (MariaDB), authentication (Frappe Login), and workflow (Frappe Workflow). The app lives entirely within the Frappe ecosystem.
- **Evidence:** `india_compliance/hooks.py` — required_apps = ["frappe/erpnext"] only. No Axum/PostgreSQL dependencies.

## Risks

### R-001: GDT API documentation unavailable
- **Severity:** High
- **Mitigation:** Start with mock implementation. Research community/unofficial API docs. Contact GDT for official documentation.
- **Affected Goals:** GP-GOAL-008, GP-GOAL-010, GP-GOAL-015

### R-002: GDT sandbox credentials unavailable
- **Severity:** Medium
- **Mitigation:** Use fake/mock credentials in sandbox mode. Real integration testing blocked until credentials obtained.
- **Affected Goals:** GP-GOAL-008, GP-SUGGESTED-002

### R-003: XML schema may have changed since Circular 78
- **Severity:** Medium
- **Mitigation:** Verify against latest GDT XSD when available. Schema versioning in constants. Keep XML generator modular.
- **Affected Goals:** GP-GOAL-009

### R-004: Digital signing provider selection undecided
- **Severity:** Low (for Phase 1-2)
- **Mitigation:** Pluggable SigningProvider interface. Mock implementation for development. Integrate real provider (VNPT/Viettel/BKAV) when selected.
- **Affected Goals:** GP-GOAL-012

### R-005: ERPNext v16 field layout differences
- **Severity:** Low
- **Mitigation:** Custom field insert_after references may need adjustment. Verify against ERPNext v16 Sales Invoice layout when bench available.
- **Affected Goals:** GP-GOAL-006, GP-GOAL-007

### R-006: Legal certification as T-VAN
- **Severity:** Note (pre-launch)
- **Mitigation:** Operating as T-VAN (tổ chức cung cấp dịch vụ HĐĐT) may require registration with GDT. Not a code issue but a business/compliance prerequisite for production SaaS.
- **Affected Goals:** GP-GOAL-018

## Dependency Map

```
GP-GOAL-001 (scaffold)
  ├── GP-GOAL-002 (constants)
  ├── GP-GOAL-003 (TaxDepartmentConfig)
  ├── GP-GOAL-004 (MST)
  ├── GP-GOAL-005 (EInvoiceLog) ──────────────────┐
  ├── GP-GOAL-006 (SI custom fields) ──┐           │
  └── GP-GOAL-007 (party custom fields) │           │
                                        │           │
  Phase 2 ─────────────────────────────┼───────────┤
                                        │           │
  GP-GOAL-008 (GDT API) ←──┐           │           │
  GP-GOAL-009 (XML gen) ──┐│           │           │
  GP-GOAL-010 (SI overrides)─┼─────────┼───────────┘
  GP-GOAL-011 (SI client) ──┼│         │
  GP-GOAL-012 (signing) ───┼┘         │
  GP-GOAL-013 (print fmt) ─┘          │
  GP-GOAL-014 (workspace) ────────────┘
                                       
  Phase 3 ─────────────────────────────
                                       
  GP-GOAL-015 (scheduler) ←── depends on 008, 010
  GP-GOAL-016 (usage report) ────── depends on 005, 006
  GP-GOAL-017 (listing reports) ─── depends on 005, 006, 007
  GP-GOAL-018 (multi-tenant) ────── depends on 003, 004, 007
```

## Contradictions

None identified in initial goals creation.

## Ecosystem Ownership Boundaries

- **Vietnam Compliance repo:** All Frappe app code (doctypes, overrides, client scripts, reports, workspace, print formats, utils, API clients, constants, install/uninstall scripts)
- **NOT applicable:** Axum API server, abn.postgresql, OneID, OneWorkflow — this app is self-contained within Frappe ecosystem
