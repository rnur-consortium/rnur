<p align="center">
  <img src="../assets/rnur_logo.png" alt="RNUR Logo" width="800">
  <br>
  <i>Custom N-G-R Neography glyph designed by <a href="https://www.reddit.com/user/W4t3rf1r3">u/W4t3rf1r3</a></i>
</p>

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

* **U+EE00–U+EFCF**: PROVISIONAL_RNUR_OPEN_SLOT.
* **U+F5C0–U+F7FF**: PROVISIONAL_RNUR_OPEN_SLOT.
* **U+F820–U+F87F**: PROVISIONAL_RNUR_OPEN_SLOT.

---

### 3.2 Empty Character Space Allocations

To prevent clashing layout telemetry within rendering engines, dedicated structural placeholders are assigned as empty characters strictly under **Set 1** specifications. No active scripts or symbols are mapped to these coordinates:

* **BMP Sector:** `U+EFD0`–`U+EFFF`
* **Plane 15 Sector (SPUA-A Hints/Specials):** `U+FFF00`–`U+FFFFF`
* **Plane 16 Sector (SPUA-B Hints/Specials):** `U+10FFF0`–`U+10FFFF`

---

### 3.3 Set 1 Open Real Estate & Tracking Matrix

The following blocks represent unallocated space (`OPEN_SLOT`) and defensively zoned space (`PROVISIONAL_RNUR_OPEN_SLOT`) within the active Set 1 framework.

#### Plane 15 (SPUA-A) Provisional Open Slots
* `U+F1D00`–`U+F1EFF` | `U+F26B0`–`U+F26FF` | `U+F28E0`–`U+F28FF` | `U+F2960`–`U+F29FF`
* `U+F3400`–`U+F4DFF` | `U+F50F0`–`U+F7FFF` | `U+F81B0`–`U+F8FFF` | `U+FA000`–`U+FAFFF`
* `U+FC000`–`U+FDFFF` | `U+FF200`–`U+FF27F` | `U+FF2A0`–`U+FF2BF` | `U+FF700`–`U+FF9FF`
* `U+FFE00`–`U+FFEFF`

> **Note on Provisional Eviction:** All ranges designated as `PROVISIONAL_RNUR_OPEN_SLOT` are held via defensive zoning under an active upstream vacuum. These are subject to the absolute Upstream Authority hierarchy and the Eviction Clause. If conflicting native allocations emerge upstream, these slots face automatic clean relocation routing to Set 2+ execution layers to prevent string parsing pollution.

#### Plane 16 (SPUA-B)
* `U+100000`–`U+10FFEF`

---

### 3.4 Sets 2+ Architecture & Global Routing

Unlike the structured block constraints mapped out in Set 1, **Sets 2 and beyond (Sets 2+)** possess total, unrestricted access across all unmapped PUA space bounds. 

Sets 2+ are completely exempt from structural block categories, provisional tracking rules, and empty character limitations. The explicit allocation bounds for Sets 2+ encompass the entire baseline PUA blocks:

* **BMP PUA Sector:** `U+E000`–`U+F8FF`
* **Plane 15 Sector (SPUA-A):** `U+F0000`–`U+FFFFF`
* **Plane 16 Sector (SPUA-B):** `U+100000`–`U+10FFFF`

This unrestricted total allocation model allows Sets 2+ to accommodate broad-spectrum fallback routing, high-density character transcoding, and custom font mapping overflows without polluting active Set 1 layout tracks.

---

### 3.5 Upstream Registry Synchronization & Diplomatic Safeguards

Because RNUR shares physical PUA space with established upstream registries—primarily the Under-ConScript Unicode Registry (UCSUR) and the Standard Private Use Code-point Extensions (SPUCE)—the permanence of Set 1 allocations depends on cross-registry diplomacy.

#### 3.5.1 The Fluidity Vulnerability
RNUR recognizes that upstream authorities do not possess rigid structural stability policies for unallocated or "Reserved for Hacks" ranges. Historical precedents (such as the 2023 UCSUR allocation of ATH within previously reserved corporate zones) demonstrate that unmapped space is subject to sudden, un-notified upstream occupation.

#### 3.5.2 Diplomatic Non-Aggression Protocols
To transition Set 1 from a localized allocation model to a true Global Consensus Layer, the RNUR Architecture Group enforces a mandatory upstream registry treaty protocol:
1. **Formal Reservation:** RNUR must maintain active, verified registration status within the master documentation of UCSUR and SPUCE for all claimed BMP, Plane 15, and Plane 16 sectors.
2. **Conflict Resolution Vectors:** In the event that an upstream vendor proposes an allocation that overlaps with an active RNUR Set 1 script, RNUR will coordinate with the vendor to steer the upstream allocation into an RNUR `OPEN_SLOT` or trigger a defensive relocation before the upstream spec formalizes.

#### 3.5.3 Upstream Collision Mitigation & Eviction Vectors
If an uncoordinated upstream allocation occurs that overwrites an active RNUR coordinate pair $(1, C)$, mitigation routing branches into two distinct operational pipelines based on the underlying slot classification:

##### 3.5.3.1 Tier A: Non-Provisional Allocations & Gaps (Plane 16 Gaps, Locked Plane 15 Sectors, and Selected BMP Blocks)
This tier applies to finalized allocations and the permanent structural space tracking slots of Plane 16, as well as the designated Plane 0 gaps (`U+F5C0–U+F6FF` and `U+F820–U+F87F`). Because these ranges represent rigid, permanent RNUR real estate, an upstream collision triggers a precise, deterministic architectural shift:
1. **Parallel Addressing Mirror:** The registry master pipeline automatically triggers a 1:1 structural eviction. Instead of shifting to an unassigned block, the affected script mirrors directly into its exact corresponding mathematical coordinate address within **Set 2** (e.g., a collision at Set 1 $U+100580$ maps directly to Set 2 $U+100580$).
2. **Flag Deployment:** The script’s historical data table entry is appended with an `UPSTREAM_COLLISION` flag.
3. **Runtime Asset Override:** For software environments operating under RNUR compliance, the local font pre-processor runtime engine forces high-priority asset targeting over the native host system string fallback to prevent immediate layout corruption.

##### 3.5.3.2 Tier B: Provisional Allocations (BMP Block U+EE00–U+EFFF & Empty Plane 15 Gaps)
This tier applies to sectors explicitly designated as Provisional RNUR Territory, which operate defensively under an active upstream vacuum. Because these regions are subject to an absolute Upstream Authority hierarchy, a collision triggers an agile escape vector:
1. **Dynamic Database Migration:** The registry master pipeline executes an automated offline database migration, shifting the displaced script's records away from the collision zone and into the first available, unassigned tracking ranges at the base of the Set 2 sandbox layer.
2. **Metric Refactoring:** Font compilation tools rebuild and refactor the underlying glyph metrics and code point mappings to align cleanly with the new sandbox target plane destination.
3. **Upstream Compliance:** The vacated Set 1 coordinate pair $(1, C)$ is updated in the master database to mirror the native upstream allocation, completely clearing out runtime font rendering pollution.

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

## 6. Release Cadence & Versioning Protocol

The RNUR specification operates on a flexible, time-gated progression model, balanced by a strict structural circuit-breaker mechanism to safeguard text-rendering stability.

### 6.1 Major Release Cadence
The registry updates its foundational architecture dynamically rather than on a rigid calendar date. A new major version becomes eligible for deployment **anytime after a minimum duration of one full year has elapsed** since the official release of the preceding major version. 

* **Current Cycle (Launched 2026):** `RNUR v1.0` (Base Abstraction Layer & Initial Consensus Claims)
* **Next Target Cycle (2027+):** `RNUR v2.0` (Eligible for release anytime after `v1.0` has been live for $\ge 1$ year)

### 6.2 The Flaw-Gate Postponement Rule
To prevent breaking changes, syntax flaws, or telemetry collisions from cascading into future registry layers, **no major version may release while an active flaw exists in the current branch.** If a structural flaw or regression is detected in an active version:

1. **Major Gating:** The upcoming annual major version is immediately frozen and postponed, even if the one-year minimum threshold has already passed.
2. **Minor Target Routing:** The engineering focus shifts exclusively to delivering a minor patch release (`[Current Major].[Minor Patch Count]`).
3. **Unfreezing Asset Line:** The next major version is unlocked for release only after the minor version successfully patches, validates, and stabilizes the flaw layer.

```text
[Current v1.0] ──(Flaw Detected)──> [v2.0 Frozen / Postponed]
       │                                  ▲
       └───> [Deploy Patch v1.1] ─────────┘ (Validation Clear: v2.0 Unlocked for Release)
