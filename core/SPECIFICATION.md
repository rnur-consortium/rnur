# RNUR-TS-01: Neographical Unicode Registry Architecture Specification

**Version:** 1.0.0

**Status:** Standard / Active

**Author:** RNUR Core Architecture Group

## 1. Abstract & Rationale

Classic font engineering models map custom characters to a flat, single-layer Private Use Area (PUA) spectrum. This design introduces two system-level failure points:

*   **Coordinate Collisions:** Multiple creators allocating independent scripts to identical code points (e.g., U+E000), corrupting text rendering across systems.

*   **The 65,535 Glyph Wall:** The OpenType specification limits the total number of glyphs inside a single font file to a maximum of 65,535. Complex writing systems requiring extensive typographic variations and contextual ligatures rapidly exhaust this ceiling.

The Reddit Neographical Unicode Registry (RNUR) mitigates these architectural constraints by treating the Unicode PUA space as an abstract multi-dimensional coordinate matrix rather than a static linear array.

## 2. The Coordinate-Pair Matrix Model

Instead of assigning a character to a singular scalar code point, RNUR abstracts the encoding layer using a relational tuple:

**Location = (S, C)**

Where:

*   S represents the **Set Layer** (S ∈ Z⁺), an arbitrary integerspace partitioning environment layers.

*   C represents the valid hexadecimal **Unicode PUA Code Point** (C ∈ PUA).

```
Set 3 (Sandbox)    [ U+E000 ] [ U+E001 ] [ U+E002 ] ... Local Dev Environment
           │
Set 2 (Sandbox)    [ U+E000 ] [ U+E001 ] [ U+E002 ] ... Application Specific
           │
Set 1 (Global)     [ U+EE00 ] [ U+EE10 ] [ U+EE11 ] ... Global Permanent Mappings
                        └─┬────┘   └─┬─────────────────┘
                 Franklin Range     Xaini / Community
```

### 2.1 Set Layer Classification

#### Set 1: The Global Consensus Layer

Set 1 is globally unique, permanent, and strictly immutable once allocated. Characters assigned to Set 1 are guaranteed never to collide with other scripts within the same layer. It accommodates finalized community writing systems, active conlangs, and historical orthographic expansions.

#### Set 2+ : The Parallel Sandbox Layers

Sets 2 and above operate as isolated environments. These layers allow font developers and software engines to mirror standard PUA spaces locally or within specific app ecosystems without threatening the structural integrity of the Global Consensus Layer.

## 3. Allocation Maps & Segment Strategy

To preserve memory space within Plane 0 (the Basic Multilingual Plane) while ensuring maximum accessibility, RNUR partitions blocks using a tier-based clustering mechanism based on character payload sizing.

### 3.1 Plane 0 (BMP) Light Alphabetic Blocks

Reserved exclusively for low-payload, stable alphabets (such as simple featural, phonetic, or segmented writing systems).

*   U+EE00 to U+EE0F: Reserved for historical incubator systems (e.g., Benjamin Franklin's 1768 phonetic reform).

*   U+EE10 to U+EFFF: Open allocation territory for community scripts.

*   U+F500 to U+F7FF & U+F820 to U+F87F: Overflow micro-blocks.

### 3.2 Plane 15 (SPUA-A) The Grand Corridor

Designed for medium-to-large writing systems that rely heavily on complex OpenType features, extensive layout engines, or continuous ligature structures.

*   U+F2A00 to U+F4DFF (Tier 1)

*   U+F5100 to U+F7FFF (Tier 2)

*   U+F8200 to U+FDFFF (Tier 3)

### 3.3 Plane 16 (SPUA-B) The Mass Core Reserve

*   U+102000 to U+10FFEF: Dedicated storage layer for massive community logographies, complex syllabaries, or highly detailed historic scripts requiring wide address spaces.

## 4. Character Property Protocol

Every character submission under RNUR Set 1 must match the Unicode Character Database (UCD) properties to maintain strict parity with modern text-shaping engines (e.g., HarfBuzz). Implementations must specify the following data structures:

*   **General Category Code:**

    *   Lu: Letter, Uppercase (requires tracking pairing vectors to lowercase counterparts).

    *   Ll: Letter, Lowercase.

    *   Lo: Letter, Other (uncased alphabetic structures).

    *   Nd: Number, Decimal Digit (requires defining numeric base matrices).

*   **Bidirectional Class:** Explicit declaration of structural directionality (L for Left-to-Right, R for Right-to-Left).

## 5. The Graduation & Lifecycle Rules

RNUR works as an incubator, tracking the long-term utility of contemporary scripts.

```
[ Proposal Submission ] ──> [ RNUR Set 1 Map ] ──> [ Script Adoption Phase ]
                                                            │
[ Universal Native Support ] <── [ Unicode Registry ] <───┘ (Graduation Rule)
```

*   **The Preservation Principle:** Once a coordinate pair (1, C) is assigned to a script within Set 1, that block is locked permanently. No script can ever overwrite it, even if the script falls into inactivity, serving as a historical record.

*   **The Graduation Exception:** If a community script receives massive real-world adoption and successfully passes formal approval by the ISO/IEC 10646 and the Unicode Consortium, its native Unicode blocks will take precedence. However, its original RNUR coordinate mapping remains statically preserved in the data tables to maintain backwards compatibility for legacy font implementations.
