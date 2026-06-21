# Security Policy

## Supported Versions

Because the Reddit Neographical Unicode Registry (RNUR) operates as a live data matrix standard, security updates, validation fixes, and architecture patch deployments are applied exclusively to the main production branch. We do not maintain legacy branch support cycles.

| Version | Supported          |
| ------- | ------------------ |
| Main    | :white_check_mark: |
| < Main  | :x:                |

---

## What Constitutes a Security Vulnerability in RNUR?

Unlike traditional software frameworks, RNUR is an infrastructure database registry. In our ecosystem, security threats specifically target the integrity, accessibility, and reliability of our allocation tables. 

We classify the following as security vulnerabilities:
1. **Validation Engine Bypasses:** Flaws within `tools/validator.py` or the remote `.github/workflows/registry_check.yml` framework that allow unauthorized, hidden, or malformed code point allocations to merge without triggering errors.
2. **Denial of Service (Matrix Pollution):** Exploits or formatting tricks within incoming CSV proposals designed to trigger memory exhaustion, unhandled exceptions, or rendering crashes in standard font engineering software parsing our registry.
3. **Upstream Data Hijacking:** Malicious spoofing or unauthorized modification of historical and provisional leases (e.g., altering fields belonging to other authors or community groups).

---

## Reporting a Vulnerability

**Please do not open a public GitHub Issue for a severe security vulnerability or exploitation vector.** Opening a public issue alerts potential bad actors before a defensive patch can be engineered.

Instead, please report security vulnerabilities using the following discrete pipeline:

1. **Draft a Private Report:** Document the exact step-by-step reproduction method, the files affected (e.g., `data/set1_master.csv`, `tools/validator.py`), and the potential impact on downstream font builders or conlangers.
2. **Submit Directly:** Open a secure private advisory via the repository's **Security** tab to transmit your finding directly to the project maintainer in a private workspace.

### Our Response Timeline
* **Acknowledgment:** You will receive an initial response acknowledging receipt of your report within **48 hours**.
* **Status Updates:** The maintainer will keep you updated privately as the vulnerability is triaged, reproduced, and patched.
* **Coordinated Disclosure:** Once a pull request resolving the issue is safely merged into `main`, full credit will be awarded to the reporting researcher in our release logs (unless anonymity is requested).

---

## Automated Security Enforcements

To protect the registry against structural manipulation, our repository employs rigorous automated boundary protections:
* **CI/CD Lockdowns:** The `.github/workflows/registry_check.yml` workflow runs automatically on every commit and pull request. It strictly enforces registry specification compliance, rendering unauthorized allocation overlaps impossible to merge.
* **Dependency Auditing:** Standard GitHub Dependabot alerts are active to monitor our underlying automation dependencies (such as the Python runtime environment) for security patches.

Thank you for helping keep the structural roadmap of digital neography secure and stable!
