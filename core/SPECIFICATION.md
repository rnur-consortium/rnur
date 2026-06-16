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

Instead of assigning a character to a singular scalar code point, RNUR abstracts the encoding layer using a relational coordinate tuple:

**Location = (S, C)**

Where:
* **S** represents the **Set Layer** ($S \in \mathbb{Z}^+$), a positive integer space partitioning distinct environment registry layers.
* **C** represents the valid hexadecimal **Unicode PUA Code Point** ($C \in \text{PUA}$).

```text
Set 3 (Sandbox)    [ U+E000 ] [ U+E001 ] [ U+E002 ] ... Local Dev Environment
                       │
Set 2 (Sandbox)    [ U+E000 ] [ U+E001 ] [ U+E002 ] ... Application-Specific
                       │
Set 1 (Global)     [ U+EE00 ] [ U+EE10 ] [ U+EE11 ] ... Global Permanent Mappings
                       └─┬────┘   └─┬─────────────────┘
                 Franklin Range   Xaini / Community
```

### 2.1 Set Layer Classification

#### Set 1: The Global Consensus Layer

Set 1 is globally unique, permanent, and strictly immutable once allocated. Characters assigned to Set 1 are architecturally guaranteed never to collide with other scripts within the same layer. It accommodates finalized community writing systems, stable constructed languages, and historical orthographic expansions.

#### Set 2+ : The Parallel Sandbox Layers

Sets 2 and beyond operate as completely isolated virtual environments. These layers allow font engineers, layout pre-processors, and application engines to mirror standard PUA spaces locally or within specific software ecosystems without threatening the structural integrity or clean string-parsing of the Global Consensus Layer.

## 3. Allocation Maps & Segment Strategy

To preserve memory space within Plane 0 (the Basic Multilingual Plane) while ensuring maximum accessibility and clean runtime font parsing, RNUR partitions blocks using a tier-based clustering mechanism based on character payload sizing. Structural layout behaviors are strictly governed by Set boundaries.

### 3.1 Plane 0 (BMP) Light Alphabetic Blocks

Reserved exclusively for low-payload, stable alphabets (such as simple featural, phonetic, or segmented writing systems) under Set 1 allocations.

* **U+EE00–U+EFCF**: OPEN_SLOT — Overflow micro-blocks / Open tracking slot.
* **U+F500–U+F6FF**: OPEN_SLOT — Overflow micro-blocks / Open tracking slot.
* **U+F820–U+F87F**: OPEN_SLOT — Overflow micro-blocks / Open tracking slot.

---

### 3.2 Empty Character Space Allocations

To prevent clashing layout telemetry within rendering engines, dedicated structural placeholders are assigned as empty characters strictly under **Set 1** specifications. No active scripts or symbols are mapped to these coordinates:

* **BMP Sector:** `U+EED0`–`U+EEFF`
* **Plane 15 Sector (SPUA-A Hints/Specials):** `U+FFF00`–`U+FFFFF`
* **Plane 16 Sector (SPUA-B Hints/Specials):** `U+10FFC0`–`U+10FFFF` *(Consisting of Source Hints `10FFC0-10FFCF`, Transcoding Hints `10FFD0-10FFEF`, and Specials `10FFF0-10FFFF`)*

---

### 3.3 Set 1 Open Real Estate & Tracking Matrix

The following blocks represent unallocated space (`OPEN_SLOT`) and defensively zoned space (`PROVISIONAL_RNUR_OPEN_SLOT`) within the active Set 1 framework.

#### Plane 15 (SPUA-A) Provisional Open Slots
* `U+F1CA0`–`U+F1EFF` | `U+F26B0`–`U+F26FF` | `U+F28E0`–`U+F28FF` | `U+F2960`–`U+F29FF`
* `U+F5080`–`U+F50FF` | `U+F5EE0`–`U+F5EFF` | `U+F6100`–`U+F615F` | `U+F6400`–`U+F6A7F`
* `U+F6DA0`–`U+F6DFF` | `U+F6F80`–`U+F6FFF` | `U+F7700`–`U+F7F5F` | `U+F8290`–`U+F82FF`
* `U+F8C00`–`U+F917F` | `U+F91C0`–`U+F91FF` | `U+F9250`–`U+F92FF` | `U+F9600`–`U+F99FF`
* `U+F9C00`–`U+FA2FF` | `U+FA500`–`U+FACFF` | `U+FC5E0`–`U+FC5FF` | `U+FC730`–`U+FC7FF`
* `U+FC920`–`U+FDEFF` | `U+FF2B0`–`U+FF2BF`

> **Note on Provisional Eviction:** All ranges designated as `PROVISIONAL_RNUR_OPEN_SLOT` are held via defensive zoning under an active upstream vacuum. These are subject to the absolute Upstream Authority hierarchy and the Eviction Clause. If conflicting native allocations emerge upstream, these slots face automatic clean relocation routing to Set 2+ execution layers to prevent string parsing pollution.

#### Plane 16 (SPUA-B) Structural Open Slots
* `U+100580`–`U+1005BF` | `U+100700`–`U+10109F` | `U+101100`–`U+1011FF` | `U+101380`–`U+1013DF`
* `U+101500`–`U+101FFF` | `U+102300`–`U+1024CF` | `U+102500`–`U+1026FF` | `U+102E00`–`U+102FFF`
* `U+103100`–`U+1071FF` | `U+107440`–`U+1074FF` | `U+108030`–`U+10806F` | `U+1081B0`–`U+1082FF`
* `U+108330`–`U+1083FF` | `U+1084B0`–`U+1085FF` | `U+108850`–`U+1088BF` | `U+108B80`–`U+108BBF`
* `U+108D00`–`U+108EFF` | `U+108F40`–`U+10937F` | `U+109640`–`U+1096FF` | `U+109780`–`U+1097DF`
* `U+10A0B0`–`U+10A0FF` | `U+10A1C0`–`U+10A1FF` | `U+10A6B0`–`U+10A6DF` | `U+10A700`–`U+10AE9F`
* `U+10B000`–`U+10CFFF` | `U+10D0A0`–`U+10D2FF` | `U+10D400`–`U+10DFFF` | `U+10E200`–`U+10E35F`
* `U+10E470`–`U+10E4EF` | `U+10E5A0`–`U+10E5DF` | `U+10E630`–`U+10E64F` | `U+10E6D0`–`U+10E7FF`
* `U+10E8A0`–`U+10E9FF` | `U+10EAA0`–`U+10EB9F` | `U+10EBE0`–`U+10EF9F` | `U+10EFD0`–`U+10F91F`
* `U+10F920`–`U+10FAFF` | `U+10FF00`–`U+10FFBF`

---

### 3.4 Sets 2+ Architecture & Global Routing

Unlike the structured block constraints mapped out in Set 1, **Sets 2 and beyond (Sets 2+)** possess total, unrestricted access across all unmapped PUA space bounds. 

Sets 2+ are completely exempt from structural block categories, provisional tracking rules, and empty character limitations. The explicit allocation bounds for Sets 2+ encompass the entire baseline PUA blocks:

* **BMP PUA Sector:** `U+E000`–`U+F8FF`
* **Plane 15 Sector (SPUA-A):** `U+F0000`–`U+FFFFF`
* **Plane 16 Sector (SPUA-B):** `U+100000`–`U+10FFFF`

This unrestricted total allocation model allows Sets 2+ to accommodate broad-spectrum fallback routing, high-density character transcoding, and custom font mapping overflows without polluting active Set 1 layout tracks.

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
