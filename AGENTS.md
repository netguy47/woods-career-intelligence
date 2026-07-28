# JobSpy PBS Scorer Assurance Instructions

This project contains a governed PBS Scorer Assurance package. Read this file and `.agents/skills/pbs-scorer-assurance/SKILL.md` before changing assurance artifacts.

## Protected policy

- Do not change `recommendation_policy.md`, PBS weights, PBS thresholds, ground-truth labels, or `professional_identity_model.json` without explicit user approval.
- Preserve and verify SHA-256 hashes for protected files before and after remediation.
- Builder-generated evidence is not independent evidence. Label each separately in reports and handoffs.

## Operational restrictions

- Do not conduct live job searches or start the 30-job trial without explicit authorization.
- Use only fixtures, recorded outputs, and deterministic local tests during assurance work.
- Restore or update `pbs_assurance_state.json` before changing implementation or test artifacts.
- Stop at a gate decision and record the exact next authorized action.

## Required assurance gates

- Keep calibration and holdout fixtures separate and report before/after results per case.
- Test score boundaries at 49.99, 50, 64.99, and 65, plus `eligibility_disposition=None`.
- Check adversarial inputs, report integrity, package inventory/checksums, and protected-file safeguards.
- Use standardized handoffs listing files, evidence provenance, tests, uncertainties, gate, and next action.
- Human approval is required before progression to a controlled trial or any protected-policy change.
