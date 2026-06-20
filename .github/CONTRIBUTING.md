# Contributing to RNUR

Thank you for taking the time to contribute to the **Reddit Neographical Unicode Registry (RNUR)**!

RNUR is an open-source, community-driven framework engineered to establish a centralized, collision-free allocation matrix across a 16-plane Unicode structure. By maintaining organized mapping standards within the Private Use Areas (PUA), this project ensures that font engineers, typographers, and conlangers can safely develop and digitally preserve custom writing systems without overlapping memory slots or breaking font metrics.

Please review these guidelines to understand our project layout, automated validation workflows, and open-source submission rules.

---

## 📂 Repository Architecture

When proposing modifications, your pull requests must target the exact directory framework defined below:

* **`.github/`**: Houses our automation workflows and issue entry points.
  * `ISSUE_TEMPLATE/bug_report.yml`: For reporting flaws in tools or specs.
  * `ISSUE_TEMPLATE/script_proposal.yml`: The mandatory starting form for requesting new code point blocks.
  * `workflows/registry_check.yml`: Our automated validation pipeline.
* **`S1/Roadmap/`**: The core tracking documentation for high-level block layouts.
  * `bmp_pua_roadmap.md`: Tracks Basic Multilingual Plane PUA allocations.
  * `spua-a_roadmap.md`: Tracks Supplementary Private Use Area-A allocations.
  * `spua-b_roadmap.md`: Tracks Supplementary Private Use Area-B allocations.
* **`UNIDATA/`**: Stores baseline reference matrices, including `Blocks.txt`, to cross-reference allocation boundaries against standard specifications.
* **`assets/`**: Houses repository media and branding files, including the official project identity (`rnur_logo.png`).
* **`core/`**: Houses `SPECIFICATION.md`, the official technical standard governing data constraints and formatting rules for the registry.
* **`data/`**: The definitive data tables for the project:
  * `set1_master.csv`: The primary, verified database tracking finalized allocations.
  * `set2_sandbox.csv`: The staging environment for experimental, pending, or unverified script layouts.
* **`tools/`**: Contains Python scripts and verification utilities used to process data tables and analyze font-mapping metrics.
  * `validator.py`: The core validation script responsible for parsing `.csv` files, checking matrix bounds, and identifying code point collisions.

---

## 🛠️ Step-by-Step Contribution Pipeline

### 1. Requesting a Script Allocation Block
To claim an unassigned block of code points for a new writing system, do not modify the master tables directly. Instead, follow this onboarding sequence:
1. Cross-reference `data/set1_master.csv` and the markdown logs inside `S1/Roadmap/` to verify your desired code points are fully vacant.
2. Navigate to the **Issues** tab on GitHub and submit a formal request using the `script_proposal.yml` form.
3. Provide the script name, total character/glyph count, sample metrics, and your proposed code point boundaries.
4. Once reviewed and accepted by the maintainer, the block will be written to `data/set2_sandbox.csv` for initial testing and integration vetting.

### 2. Infrastructure, Tooling, and Localization Updates
If you are modifying automated tooling in `tools/` or contributing documentation enhancements (such as translating documentation and localized acronyms into native scripts like Cyrillic, Greek, Armenian, or Georgian):
* Ensure all code modifications strictly adhere to the formatting regulations defined in `core/SPECIFICATION.md`.
* File a bug report or feature request using `.github/ISSUE_TEMPLATE/bug_report.yml` if you find issues with validation tools.

---

## 🤖 Automated Validation and CI/CD

Every pull request submitted to this repository automatically triggers our GitHub Actions integration pipeline running `.github/workflows/registry_check.yml`. This workflow directly executes `tools/validator.py` to:
1. Verify that all modified `.csv` data formatting perfectly aligns with `core/SPECIFICATION.md`.
2. Scan all code points to ensure zero overlaps between `data/set1_master.csv` and active sandbox entries.

**Important:** Your pull request *will not be merged* if the automated registry check fails. You can run `python tools/validator.py` locally to test your data matrices prior to pushing your changes.

---

## 🤝 Open-Source Etiquette and Attribution

* **Mandatory Attribution:** RNUR is a collaborative consortium built on open standards. If your submission or script layout incorporates, adapts, or references assets, glyphs, or design elements made by another creator, you must provide explicit credit and mention their source or username within your documentation or pull request.
* **Workflow Accessibility:** While the backend structure relies on precise engineering data, we keep the creative process accessible. System diagrams, asset localizations, and structural identity files added to `assets/` may be engineered using highly accessible, lightweight tools like Paint.NET, provided the final output meets standard web format and file size guidelines.

For community standards and behavioral expectations, please refer to our `CODE_OF_CONDUCT.md`. Thank you for helping map and preserve the future of digital neography!
