# ICM 1.2 release candidate — sanitized validation evidence

Package under test: public commit `3b435de` (version 1.2). Scope: #1, #2 and #3. This is draft release-candidate evidence, not release approval or complete ICM certification.

## Automated checks

- Existing audit regression script passed.
- 20 additional synthetic unittest cases passed, including table/bullet inputs, title/subheading traversal, routing columns, path bases, anchors, optional/future working inputs, input prose, shims, alternate paths/gates, libraries, history, unsupported constructs, symlinks, exit modes and no-cache/idempotence behavior.
- Skill metadata validator passed; the public pack audit has no structural failures or warnings. Unresolved external/dynamic routing is explicitly reported.

## Isolated consumer pilots

Two independent baseline/candidate pairs were prepared from owner-supplied archives. Backup coverage was accepted. Only lightweight isolation and scoped context/package checks were performed; originals remained read-only. Complete candidate packages were staged only in candidate copies, with hash parity on relevant installation surfaces. Baseline installed version was 1.1. No applications, hooks, deployments, product updates or external account workflows were executed.

| Archetype | Baseline audit | Final candidate audit after synthetic maintenance | Behavioral result |
| --- | --- | --- | --- |
| Engineering consumer with foreign workflow ownership | Exit 0; one reference-area warning | Exit 0; 5 ok, 5 info, no warnings/failures; 98 local targets checked, 3 unresolved | Actual fresh-context orientation/resumption succeeded. One fictitious document plus one router row; existing status/history ownership preserved. |
| Topic-selected numbered roster with record lifecycle | Exit 0; 9 ok, 1 info | Exit 0; 9 ok, 97 info, no warnings/failures; 140 local targets checked, 95 unresolved | Actual fresh-context contract selection succeeded. Flat/scoped routing and one-hop profile resolution exercised as structural simulations. Three fictitious files in one new record; no real write-back. |

Both final auditors were rerun twice with byte-identical output. Scoped baseline context was unchanged; candidate context differences matched the allowed synthetic tasks. Lightweight original Git status and relevant file checks were unchanged. Candidate installation parity was confirmed across five tested surfaces. Fresh navigation used the same version 1.2 guidance throughout; final parser replacements received mechanical reruns, not new fresh navigation sessions.

The roster pilot is **qualified compatibility evidence**, not a clean procedural pass: an incidental private-file read and an interrupted overly broad hashing attempt occurred in its disposable candidate. No private facts entered fixtures, reports or this repository, and no full manifest was produced. Details stay in local reports. The overall pilot issue remains open for review of this exception.

## Findings and limits

The pilots exposed title/subheading input traversal and explanatory-path false positives; both were repaired with synthetic regressions before final reruns. Improved coverage reports dynamic, conditional and prose-scoped references honestly instead of silently counting them as validated. Unresolved counts are not resolved dependencies. No heuristic pass establishes semantic correctness, current review approval, private fact freshness or execution readiness. Existing stale engineering routing/status snippets were reported locally and left untouched.

Profile/index write-back, real record execution, live applications, external consumers and migrations remain intentionally untested. These results authorize no rollout. Review #1–#3 and the draft PR; a subsequent explicit decision is needed before merge/release and one-consumer-at-a-time updates using the owner's existing recovery arrangements.
