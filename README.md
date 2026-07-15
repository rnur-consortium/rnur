<p align="center">
  <img src="/assets/rnur_logo.png" alt="RNUR Logo" width="800">
  <br>
  <i>Custom N-G-R Neography glyph designed by <a href="https://www.reddit.com/user/W4t3rf1r3">u/W4t3rf1r3</a></i>
</p>

# Reddit Neographical Unicode Registry (RNUR)

The official, open-source registry framework standardizing conflict-free Private Use Area (PUA) allocations for original scripts, conlangs, and neographies. 

RNUR solves the limitations of classic monolithic PUA registries by introducing a multi-dimensional layering system, preventing code point collisions and bypassing the 65,535 OpenType glyph ceiling.

---

## 🛠️ Core Architecture

RNUR operates on a **Coordinate-Pair System** mapped as `(Set_Number, Code_Point)`. This shifts typography from a flat, single-layer grid to a multi-dimensional matrix.

### The Set Layering System
* **Set 1 (Global Stability Layer):** Reserved for finalized, fully documented community scripts, active conlangs, and verified historical additions. Characters locked into Set 1 are globally unique and protected.
* **Set 2+ (Sandbox Layers):** Unrestricted, isolated environments for experimental scripts, application-specific tokens, or localized rendering workflows. Set 2 maps across the entire 16-plane PUA standard structure, allowing developers to reuse ranges locally while serving as the landing zone for automated evictions.

### 🗺️ Registry Layer Architecture (Set 1)

| Plane Layer | Code Point Range | Classification | Collision Strategy |
| :--- | :--- | :--- | :--- |
| **Plane 0 (BMP)** | `U+EE00–U+EFFF` | Tier B: Provisional Territory | Dynamic relocation to the base of Set 2 |
| **Plane 0 (BMP)** | `U+F500–U+F6FF`<br>`U+F820–U+F87F` | Tier A: Permanent Structural Slots | 1:1 Parallel Address Mirror to Set 2 + Runtime Override |
| **Plane 15 (SPUA-A)**| Explicit Gaps* | Tier B: Provisional Territory | Dynamic relocation to the base of Set 2 |
| **Plane 15 (SPUA-A)**| Active Mappings (`U+F2A00+`) | Tier A: Permanent Allocations | Runtime Font Asset Override Protection |
| **Plane 16 (SPUA-B)**| All Empty Gaps | Tier A: Permanent Structural Slots | 1:1 Parallel Address Mirror to Set 2 + Runtime Override |

> *\*Note: Explicit Plane 15 Provisional Gaps include:* `F1D00–F1EFF`, `F26B0–F26FF`, `F28E0–F28FF`, `F2960–F29FF`, `F5080–F50FF`, `F5EE0–F5EFF`, `F60C0–F60FF`, `F6100–F615F`, `F6400–F6A7F`, `F6DA0–F6DFF`, `F7700–F7F5F`, `F8290–F82FF`, `F8C00–F917F`, `F91C0–F91FF`, `F9250–F92FF`, `F9600–F99FF`, `F9C00–FA2FF`, `FA500–FACFF`, `FC5E0–FC5FF`, `FC730–FC7FF`, `FC920–FDEFF`, *and* `FF2B0–FF2BF`.

---

## ⚠️ Upstream Conflict & Eviction Policy

Because RNUR shares physical PUA space with established upstream authorities—primarily the Under-ConScript Unicode Registry (UCSUR) and the Standard Private Use Code-point Extensions (SPUCE)—external collisions are handled automatically by our pipeline architecture based on slot classification:

### 🔹 Tier A: Hardened Slots & Plane 16 Gaps
This applies to finalized permanent allocations, the permanent structural space tracking slots of Plane 16, and designated Plane 0 gaps (`U+F500–U+F6FF`, `U+F820–U+F87F`). If an upstream registry overrides these sectors:
1. **Parallel Addressing Mirror:** The registry pipeline triggers a **1:1 mathematical eviction** straight into the exact corresponding coordinate within **Set 2** (e.g., Set 1 `U+100580` maps directly to Set 2 `U+100580`).
2. **Flag Deployment:** The script is appended with an `UPSTREAM_COLLISION` flag in the database.
3. **Runtime Override:** Compliant local pre-processors forcibly prioritize the RNUR font layer over native system fallbacks to preserve layout integrity.

### 🔹 Tier B: Provisional Territory (BMP `U+EE00–U+EFFF` & Plane 15 Gaps)
These blocks function as defensive zones operating under an active upstream vacuum. If an upstream collision occurs, affected scripts trigger the **Automated Eviction Clause**:
1. **Dynamic Database Migration:** The script is automatically migrated down to the first available, unassigned rows at the base of the Set 2 sandbox layer.
2. **Metric Refactoring:** Compilation tools rewrite and refactor glyph metrics to align with the new sandbox target location.
3. **Upstream Alignment:** The vacated Set 1 slot is updated to mirror the native upstream allocation, clearing out runtime font rendering pollution.

---

## 📋 Submission Criteria

RNUR mirrors formal Unicode Consortium submission standards to ensure high-quality, stable implementation. To submit a script for a formal Set 1 allocation, proposals must include:

1.  **The Repertoire:** A definitive character list defining exact glyph counts and organizational structure.
2.  **Character Properties:** Clear functional definitions (e.g., `Lu` for Upper Case, `Ll` for Lower Case, `Nd` for Decimal Numbers).
3.  **Visual Chart:** A companion font file, glyph sheet, or clear grid reference demonstrating exact metrics and appearance.

> **The Graduation Rule:** RNUR acts as a standardized "waiting room." If a script achieves long-term usage and prepares a formal proposal for the Unicode Consortium, its RNUR layout remains locked as a historical record until official, universal character blocks are assigned.

---

## 🗄️ Repository Structure

```text
├── .github/                # Issue templates and workflows
├── assets/                 # Assets
├── core/                   # Registry specification documentation
│   └── specification.md    # Core architectural guidelines
├── UNIDATA/                # Unicode data
├── data/
│   ├── set1_master.csv     # The definitive master mapping for Set 1 (with Flags schema)
│   └── set2_sandbox.csv    # Registered sandbox identifiers
├── tools/
│   └── validator.py        # Python script to check submissions for overlap conflicts
└── README.md               # You are here
```

---

## 🛠️ How to Contribute

RNUR is an open-source, community-driven framework. Whether you are submitting a new script allocation or fixing a tool, please use the project structure detailed above to direct your changes:

### 1. Proposing a New Script Allocation
To claim a block of code points for a custom writing system, please follow this pipeline:
* **Step 1:** Look at `data/set1_master.csv` and the files inside `S1/Roadmap/` (`bmp_pua_roadmap.md`, `spua-a_roadmap.md`, and `spua-b_roadmap.md`) to verify your desired code points are entirely unassigned.
* **Step 2:** Go to the **Issues** tab on GitHub and open a new proposal using our structured `script_proposal.yml` template.
* **Step 3:** Once reviewed, your script will initially be assigned to `data/set2_sandbox.csv` for testing and layout layout validation.

### 2. Infrastructure & Tooling Updates
* If you are modifying automated validation logic, work within the `tools/` directory.
* Every single pull request automatically triggers our automated GitHub Actions workflow (`.github/workflows/registry_check.yml`). Your PR will not merge unless this script successfully verifies that your data formatting conforms strictly to our `core/SPECIFICATION.md`.
* Bug reports regarding the infrastructure should be filed using the `.github/ISSUE_TEMPLATE/bug_report.yml` form.

### 3. Open-Source Etiquette & Asset Submission
* **Community Attribution:** RNUR is built on community collaboration. If you incorporate or build upon glyphs, assets, or text created by another user, you must provide explicit credit to them within your documentation or commit log.
* **Visual Media:** Project graphics, repository diagrams, and localized asset variations stored in the `assets/` folder (such as `rnur_logo.png`) can be designed in lightweight, accessible tools like Paint.NET, provided they meet our clear format guidelines.

For full step-by-step submission workflows and formatting rules, please read the complete [CONTRIBUTING.md](CONTRIBUTING.md) file.
