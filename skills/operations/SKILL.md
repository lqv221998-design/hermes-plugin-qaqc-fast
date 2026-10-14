---
name: operations
description: Use when operating QAQC. Verify project, discipline and effects.
version: 0.2.0-rc.3
license: MIT
platforms: [windows]
metadata:
  hermes:
    tags: [qaqc, browser, hybrid]
    related_skills: [qaqc-site-map, qaqc-business-map]
---
# QAQC Fast — operating contract
Missing local runtime/libraries: load setup, read [PREREQUISITES.md](../../PREREQUISITES.md) and [recipient prompt](../../PROMPT-HERMES.md). Native PM and actual import/version proof; server template/ACL denial is not a local dependency fault.

Use `qaqc_fast_session` only. Do not call raw `chrome_qaqc`, DMS tools, a second browser driver, JavaScript or account APIs to bypass this executor. Scoped Computer Use runs through the executor, not fallback after refusal. This intent policy is not an OS sandbox or backend ACL. Load `qaqc-fast:setup` for prerequisite gates.

## Resolve the work
Default context_policy=auto uses the recipient's own browser login and QAQC backend ACL. No typed account/project binding is required. Observe current page context, keep it stable during an operation, never copy author cookies/permissions/settings. Old expected_user_display_name is ignored in auto mode; optional manual policy is only a legacy assertion. Display names are not unique principals or access grants.

Read bundled references/module-guide.md; author global skills are optional. Current project is observed from selected page header, never URL IDs. If user selects a specific target, expected_project is an optional assertion and mismatch stops. No author project/account is a default.

## Tool flow
Start with tasks, capabilities and local prepare; auto mode requires no name input. Prerequisite block does not establish route/ACL failure. Three legacy recipes are not all actions; reading workflow is not granting transitions.

open_page accepts exact QAQC URL, mode new/reuse and operation_id, without typed names in auto mode. Separate grants/host approval remain. New is background and uniquely identified; reuse verifies source context. No launcher/profile copy/arbitrary domains. Root is bootstrap only, not business verification. open_page_status reconciles same session/attempt without replay. Context/URL verified is not data readiness or permission expansion.

1. `capabilities` returns supported actions/modules without browser access.
2. `pages` discovers supported QAQC page IDs and separate bootstrap_pages for the exact root. It does **not** open Chrome, verify project or authenticate. Never assume page 1. Multiple pages require selecting the relevant observed source.
3. inspect needs page_id; project is observed from header. expected_project is optional explicit target assertion, not card/URL inference.
4. `open_module` or `read_list` needs these fields + `module`: `work_acceptance`, `photos`, `quality_risks`. One executor call batches a bounded live-menu walk; after every click it rechecks source/project. A destination requires the live route and exact business heading. No arbitrary UID/URL/label input is accepted.
5. Public `read_list` and `read_view` persist all observed current-page rows/text/links to a hashed artifact; no 100/250/100 slicing. Native snapshot file budget 8 MiB fails closed, never silently clips. Non-semantic DOM stays unstructured, not invented records. Readiness requires stable snapshots plus explicit data/completion/empty/counter and no busy/loading/contradiction; false is pending, not a zero-record proof. Exclude only iframe subtree, keeping later top-page siblings. Current page is not whole inventory, SharePoint link not workbook content.

## Completion and pending states
- Accept only stated verification; `ok:true,status:read_verified` with readiness false is still partial. Pages/capabilities success is not completed business work.
- Report observed time/source/project, coverage, filters and remaining gaps. `inventory_complete` and `full_document_read` remain false.
- Supply expected_discipline when required. Only selected/checked/pressed=true on a matching control verifies XÂY DỰNG/CƠ ĐIỆN; labels alone do not. If unavailable/mismatched, stop rather than force true. Legacy inspect is only header observation; use new read_view/read_list for discipline/readiness.
- `pending_login`: ask the human to log in in the dedicated Chrome or use host vault tools where they can target that page. Never accept/type/store passwords or 2FA through this plugin.
- `permission_denied`, `project_mismatch`, `project_header_unverified`, `navigation_missing_or_dom_drift`, `destination_not_verified`: stop; do not retry/fallback into another project/browser/account.
- pending_user_binding only applies to opt-in manual policy. In auto, user/project drift or unverified header stops the current operation without asking for a persistent name binding. Never use author account or bypass ACL.
- Host block/failure/truncation: no plugin retry. Check native connector/approval and fresh UI before an explicit new request. Do not infer success from the click or timeout.

## Expanded RC flows and limits
`navigate` uses bounded observed menu_path/destination_heading. `set_context` verifies from_project then exact target/discipline. `query` fills observed fields and reads values back before search; dates must be supported by live UI. `read_all` requires key_column/next_label, per-page artifacts, duplicate conflict checks, terminal pager and total reconciliation; only then inventory_complete. `open_record` uses exact identity/observed link and validates requested tabs. No guessed URL/UID/API or unverified virtualized rows. Risk checklist is not defects; 0/0 does not prove no defect.

`read_document`: selected local file/hash, XLSX all sheets/rows/formulas or PDF all text layers. No formula calculation; scan/empty gaps explicit, full_document_read=false. DOCX/CSV/ZIP content reader not implemented. Local name is not SharePoint source/revision; remote_source_link_verified=false. `ocr_document` needs explicit local MinerU binding/operation_id; no fallback/retry. `analyze_image` uses host vision. Outputs unreviewed/non-normative; not company rules or automatically loaded into Cognee.

Writes need host approval, explicit write_project TEST and only new QAQC-PLUGIN-TEST records owned by plugin. write_record/create/edit verifies fields/identity/status after successful uncached reload. upload_attachment verifies selected file and persisted link, not remote bytes. delete_record reconciles absence in exact return list after reload/all pages. transition_record send/approve/reject/close needs separate grant; creation rights do not grant workflow. Keep workflow_transitions=[] when only create/edit/upload/delete authorized. Journal operation_id before side effects; do not mint a new ID to replay uncertainty. checkpoint does not auto-resume/reset.

begin_transfer stores pending before one trigger at selected new destination; verify_transfer checks new stable complete format/hash. Click/print prompt is not file completion. No replay on missing/partial/uncertain. Native dialog/print and live role acceptance need their own evidence.

native_capture exact pid/window after source verification; review image active URL/window/account/project/control, because AX can include inactive tabs. native_step same session/project/user and owned-record or verified transfer, reviewed SHA and one-use token; fresh same-window image/elements must match immediately before input. Driver confirmed is not business persisted. Native refresh with handoff_token can capture the owned modal without DOM fallback, only same scope/target and bounded cached source. MCP refusal/context drift invalidates handoff. Input expires after 90s, refresh source after 300s must be reverified. Foreground has separate approval; no focus steal, auto retry, secrets/permission/payment/2FA input.

diagnose only probes selected loopback port, not business/login. restore_browser needs explicit grant and exact owner executable/profile/port, no profile copying or connector switch. benchmark uses equal two-fresh-snapshot samples, p50/p95/min/max/readiness/output hashes. It excludes preflight/model/chat and has no baseline by default: not end-to-end acceptance. Need caller/model/UI timings, equivalent baseline and output reconciliation before claiming faster/stable site-wide.

## Runtime ownership
The active profile grants only `chrome_qaqc` to this plugin. Native include is list_pages/take_snapshot/click/wait_for/fill_form/upload_file/navigate_page, plus new_page only when the recipient grants new-tab use. DMS remains unchanged. Runtime artifacts/state stay private, outside install tree. Keep endpoints, paths, cookies and live records out of portable packages; recipient owns browser/account. RC fixtures/Doctor do not prove all roles/full site or live TEST acceptance.
Trust/allowlist consent from one operator applies only to that operator's local profile, never to all recipients. Each installation must make its own grant. Do not share one credential-bearing Chrome connection between people; use isolated OS/Hermes/browser profiles. This desktop plugin does not authenticate users of a shared multi-user service or elevate/copy QAQC roles.

Install/enable is not proof the present chat reloaded tools. Open a new chat after activation; verify skill discovery, capabilities, pages and an actual inspect before using it. Do not profile-wide reload/restart DMS solely to activate QAQC.
