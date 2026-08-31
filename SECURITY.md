# Security Policy

## Supported Versions

Only the latest stable release and the current development branch receive security updates. Older versions are not supported.

| Version           | Supported          |
| ----------------- | ------------------ |
| Latest release    | :white_check_mark: |
| main branch       | :white_check_mark: |
| < latest release  | :x:                |

## Merge security enforcement

For pull requests to `main`, the required security/dependency context is `scan-pr / osv-scan`. It is produced by `.github/workflows/osv-scanner.yml`; the reusable OSV PR workflow fails when a new vulnerability is detected.

The active `Protect main` ruleset also requires `python`, uses strict latest-base status-check enforcement and requires relevant review threads to be resolved before merge.

CodeQL is not configured as a required check or Code Scanning merge-protection rule in the currently verified ruleset, so no CodeQL severity threshold is an active merge gate. Trivy is not configured as a verified merge gate and has no active threshold.

CodeRabbit and Copilot Code Review are advisory/best-effort review services, not required status checks. Their unavailability alone does not block merge. If either service posts a relevant finding, the finding must still be evaluated and any relevant review thread resolved before merge.

## Reporting a Vulnerability

If you discover a security vulnerability in pastebinit, please report it responsibly.

**Please do not open a public GitHub issue.** Instead, report it privately through GitHub's Security Advisory system:

1. Go to the **Security** tab in this repository
2. Click **Report a vulnerability**
3. Fill out the advisory form with as much detail as possible

Alternatively, you can use GitHub's private vulnerability reporting feature if enabled.

### What to expect

- **Acknowledgment:** You will receive an initial response within 5 business days confirming receipt of your report.
- **Updates:** We aim to provide status updates at least every 2 weeks as we investigate and work on a fix.
- **Decision:** If the vulnerability is accepted, we will develop and release a fix, then coordinate public disclosure. You will be credited as the reporter unless you prefer to remain anonymous.
- **Declined:** If the report is declined, we will explain why and may suggest alternative steps.

We greatly appreciate responsible disclosure and the effort you put into keeping pastebinit secure.
