# Reddit Neographical Unicode Registry (RNUR)

The official, open-source registry framework standardizing conflict-free Private Use Area (PUA) allocations for original scripts, conlangs, and neographies. 

RNUR solves the limitations of classic monolithic PUA registries by introducing a multi-dimensional layering system, preventing code point collisions and bypassing the 65,535 OpenType glyph ceiling.

---

## 🛠️ Core Architecture

RNUR operates on a **Coordinate-Pair System** mapped as `(Set_Number, Code_Point)`. This shifts typography from a flat, single-layer grid to a multi-dimensional matrix.

### The Set Layering System
*   **Set 1 (Global Stability Layer):** Reserved for finalized, fully documented community scripts, active conlangs, and verified historical additions (e.g., Benjamin Franklin's phonetic alphabet reforms). Characters in Set 1 are globally unique and permanent.
*   **Set 2+ (Sandbox Layers):** Isolated environments for experimental scripts, application-specific tokens (e.g., custom code syntax fonts), or localized rendering workflows. Set 2 allows developers to reuse standard PUA ranges (like `U+E000`) locally without corrupting the global consensus of Set 1.

### The Anchor Tenant Rule
To preserve efficiency within Plane 0 (BMP), extensive writing systems requiring massive, uninterrupted code blocks for complex layout engines (like syllabaries requiring heavy OpenType ligature structures) bypass fragmented spaces and are allocated dedicated blocks starting at the gateway of **Plane 15** (`U+F0000`).

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
├── core/                   # Registry specification documentation
├── data/
│   ├── set1_master.csv     # The definitive master mapping for Set 1
│   └── set2_sandbox.csv    # Registered sandbox identifiers
├── tools/
│   └── validator.py        # Python script to check submissions for overlap conflicts
└── README.md               # You are here
