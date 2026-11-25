# Maintainer activation checklist

This public checklist contains no secrets or private operational details. An authorized owner should complete these steps before treating the repository as an operational public trust surface.

1. Publish the contents at the root of the public `Azvelahq/.github` repository on `main`. Confirm the organization profile renders correctly.
2. Enable Issues and private vulnerability reporting for this repository. Test the private reporting entry point from a non-maintainer account without submitting real sensitive information. Establish a monitored private channel and a responsible person for triage. Until verified, do not advertise the channel as operational. Enable private reporting separately in relevant public projects.
3. Review the contact-only issue form and ensure requests are monitored. Establish a private moderation route. Replace this fallback with a confirmed corporate contact when available.
4. Confirm that the initial CODEOWNERS account has explicit write access. Replace it with an authorized team once that team exists and has access.
5. On this public repository, enable repository-level branch rules as available: block force pushes/deletion, require pull requests and independent review when there are enough reviewers, require passing CI after its first successful run. Document any bootstrap exception. Organization rulesets and private-repository protections may need a paid plan.
6. Confirm organization 2FA, token restrictions, Actions policy and full commit SHA pinning in Settings. Disable unnecessary third-party access. Review audit events. Do not publish audit records here.
7. Run the included validation workflow and inspect its result. Check all templates in GitHub's UI. Install workflow templates only in projects that have the documented Make targets; do not treat a green documentation check as product security assurance.
8. Confirm Dependabot settings and available free security features; review updates before merging. Keep artifacts and credentials out of this repository.
9. Confirm rights to publish the supplied branding and approve the public policy language. Do not imply registered trademark or legal corporate status without confirmation. Add an explicit license only after rights and terms are decided.

## Local checks

Run `python3 scripts/validate_public_repo.py` from the root. The checker verifies a limited set of structural invariants, links to local files, template pairings and pinned action references; it is not a full GitHub schema validator or security scanner.

References: [community defaults](https://docs.github.com/en/communities/setting-up-your-project-for-healthy-contributions/creating-a-default-community-health-file), [workflow templates](https://docs.github.com/en/actions/how-tos/reuse-automations/create-workflow-templates), [private reporting](https://docs.github.com/en/code-security/how-tos/report-and-fix-vulnerabilities/configure-vulnerability-reporting/configure-for-a-repository).
