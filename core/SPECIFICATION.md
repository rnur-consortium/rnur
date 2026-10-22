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
                  Vulcan Range   SPUCE / Community
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

#### 3.1.1 SPUCE-Supplied Allocation Map for `U+EE00–U+EFFF` (Represented in RNUR Set 1)

> **Governance distinction.** SPUCE does not use RNUR's Set 1 / Set 2 architecture; the set names in this document refer exclusively to RNUR's internal organization. SPUCE supplies the incoming allocation definitions listed below. RNUR defines how those definitions are represented within RNUR's own Set 1 layer, and how RNUR scripts displaced by them migrate into RNUR Set 2.

The entire RNUR Set 1 BMP PUA interval `U+EE00–U+EFFF` is represented by nine SPUCE-supplied script allocations. These nine ranges cover the interval exactly, with no gaps and no overlaps (inclusive sizes in code points):

| Script | Range | Size |
| :--- | :--- | ---: |
| Vulcan | `U+EE00`–`U+EE2F` | 48 |
| Gallifreyan | `U+EE30`–`U+EE5F` | 48 |
| Atlantean | `U+EE60`–`U+EE8F` | 48 |
| Valyrian | `U+EE90`–`U+EEBF` | 48 |
| Dovahzul | `U+EEC0`–`U+EEEF` | 48 |
| Utopian | `U+EEF0`–`U+EF0F` | 32 |
| Global Alphabet | `U+EF10`–`U+EF3F` | 48 |
| Ditema | `U+EF40`–`U+EF6F` | 48 |
| Quốc âm tân tự | `U+EF70`–`U+EFFF` | 144 |

These records are tracked in `data/set1_master.csv` (flag `SPUCE`) and `UNIDATA/S1/Blocks.txt`. **Provenance note:** this repository implements the supplied SPUCE allocation map for the BMP PUA; the records are declared as SPUCE allocations owned by SPUCE, and this specification does not assert an independent RNUR verification of the upstream SPUCE publication or formal ratification of this map beyond the SPUCE source agreement recorded in `UNIDATA/S1/Sources.txt`.

#### 3.1.2 Former Set 1 RNUR Allocations Relocated to Set 2

No displaced RNUR script remains an active Set 1 allocation inside `U+EE00–U+EFFF`. The six named RNUR scripts formerly allocated there were evicted to the Set 2 sandbox layer, occupying contiguous ranges that begin immediately after ConstantScript (`U+E000–U+E81F`):

| Script | Former Set 1 range | Set 2 range | Size |
| :--- | :--- | :--- | ---: |
| Benjamin Franklin's Phonetic Additions | `U+EE00`–`U+EE0F` | `U+E820`–`U+E82F` | 16 |
| Loopiform | `U+EE10`–`U+EE5F` | `U+E830`–`U+E87F` | 80 |
| Sulat Hiligaynon | `U+EE90`–`U+EEDF` | `U+E880`–`U+E8CF` | 80 |
| Western Script | `U+EEE0`–`U+EF2F` | `U+E8D0`–`U+E91F` | 80 |
| Zurjon | `U+EF30`–`U+EF6F` | `U+E920`–`U+E95F` | 64 |
| Foldian | `U+EF70`–`U+EFAF` | `U+E960`–`U+E99F` | 64 |

The destinations are contiguous, non-overlapping, preserve the original order and inclusive sizes, and cover `U+E820–U+E99F` exactly. `U+EB00–U+F8FF` remains open Set 2 sandbox space; the interval `U+E9A0–U+EAFF` is occupied by the Placeholder allocation relocated under the SPUCE allocation update of 2026-10-22 (see §3.1.3).

#### 3.1.3 Placeholder Relocated to Set 2 (SPUCE Allocation Update, 2026-10-22)

> **Governance distinction.** SPUCE does not use RNUR's Set 1 / Set 2 architecture; the set names in this document refer exclusively to RNUR's internal organization. SPUCE supplies the allocation definition recorded below. RNUR defines how that definition is represented within RNUR's own Set 1 layer, and how the displaced RNUR allocation was relocated into RNUR Set 2.

The named RNUR allocation `Placeholder` moved out of Set 1 and into the Set 2 sandbox layer, immediately after Foldian (`U+E960–U+E99F`, unchanged):

| Script | Former Set 1 range | Set 2 range | Size |
| :--- | :--- | :--- | ---: |
| Placeholder | `U+F5C0`–`U+F71F` | `U+E9A0`–`U+EAFF` | 352 |

The destination is contiguous with, and does not overlap, the six Set 2 destinations of §3.1.2; the inclusive size (352 code points) is preserved.

The vacated Set 1 range is not left empty. It is subdivided into three contiguous, non-overlapping ranges that cover `U+F5C0–U+F71F` exactly:

| Set 1 range | Status | Description |
| :--- | :--- | :--- |
| `U+F5C0`–`U+F5FF` | PROVISIONAL_RNUR_OPEN_SLOT (`???`) | Provisional RNUR open slot; SPUCE has not assigned this range to another block yet. |
| `U+F600`–`U+F6FF` | SPUCE Allocation | Miscellaneous Symbols Extended-I. |
| `U+F700`–`U+F71F` | PROVISIONAL_RNUR_OPEN_SLOT (`???`) | Provisional RNUR open slot; SPUCE has not assigned this range to another block yet. |

* The two `???` ranges are provisional because SPUCE has not assigned them to another block yet. They carry no name, no allocation, and no encoded repertoire.
* `Miscellaneous Symbols Extended-I` is a SPUCE allocation: SPUCE supplies the definition and RNUR represents it within its own Set 1 layer (recorded in `data/set1_master.csv` with the `SPUCE` flag and in `UNIDATA/S1/Blocks.txt` under the SPUCE Project Allocations section). Like the other SPUCE allocations, it carries no encoded repertoire yet.
* The SPUCE allocation of `U+F92C0`–`U+F941F` (Placeholder, Plane 15) is a separate SPUCE allocation and is unaffected by this update.

#### 3.1.4 Other Set 1 BMP Allocations

* **U+F600–U+F6FF**: Miscellaneous Symbols Extended-I (SPUCE allocation — see §3.1.3).
* **U+F5C0–U+F5FF**: PROVISIONAL_RNUR_OPEN_SLOT (`???`).
* **U+F700–U+F71F**: PROVISIONAL_RNUR_OPEN_SLOT (`???`).
* **U+F720–U+F7FF**: PROVISIONAL_RNUR_OPEN_SLOT.
* **U+F820–U+F87F**: PROVISIONAL_RNUR_OPEN_SLOT.

#### 3.1.5 Permanent-Space Migration Rule for `???` Reservations

**When migrating from the Set 1 compatibility layer into the Set 2 sandbox layer, any `???` reservation encountered is dissolved into permanent space.** Concretely:

* The provisional RNUR reservation record is removed from the active migration result.
* No Set 2 destination is assigned to it; it is not recreated as a Set 2 open slot, placeholder, or provisional reservation, and it is not renamed to an invented script.
* The Unicode code points themselves are never deleted.

The two former Set 1 `???` reservations inside the SPUCE interval — `U+EE60–U+EE8F` and `U+EFB0–U+EFFF` — were removed by this rule and were **not** carried into Set 2. Their addresses nevertheless belong to SPUCE in the final Set 1 map because the nine SPUCE allocations replace the entire `U+EE00–U+EFFF` interval: `U+EE60–U+EE8F` is now part of Atlantean and `U+EFB0–U+EFFF` is part of Quốc âm tân tự. The permanent-space conversion describes how the provisional reservations were treated during migration; it does not override or erase the final RNUR Set 1 representation of the SPUCE-supplied allocations. The `???` ranges outside the migrated interval are untouched by this rule. The later `Placeholder` relocation (§3.1.3) is a separate, explicitly recorded allocation move, not a dissolution of a `???` reservation: `Placeholder` was a named allocation, and the two `???` ranges it leaves behind (`U+F5C0–U+F5FF` and `U+F700–U+F71F`) remain provisional RNUR territory in Set 1.

---

### 3.2 Empty Character Space Allocations

To prevent clashing layout telemetry within rendering engines, dedicated structural placeholders are assigned as empty characters strictly under **Set 1** specifications. No active scripts or symbols are mapped to these coordinates:

* **Plane 15 Sector (SPUA-A Hints/Specials):** `U+FFFF0`–`U+FFFFF` (the preceding `U+FFF00`–`U+FFFBF` provisional space and `U+FFFC0`–`U+FFFEF` Fragments allocation are tracked separately in §3.3 and §3.5.5)
* **Plane 16 Sector (SPUA-B Hints/Specials):** `U+10FFF0`–`U+10FFFF`

> **Correction (Set 1 → Set 2 migration):** the former BMP empty-character sector `U+EFD0`–`U+EFFF` is superseded by the SPUCE allocation map for `U+EE00–U+EFFF` described in §3.1.1. Because the nine SPUCE allocations replace the whole interval, those code points now belong to the Quốc âm tân tự allocation and can no longer be tracked as an empty-character sector. The Plane 15 and Plane 16 empty-character sectors are unaffected.

---

### 3.3 Set 1 Open Real Estate & Tracking Matrix

The following blocks represent unallocated space (`OPEN_SLOT`) and defensively zoned space (`PROVISIONAL_RNUR_OPEN_SLOT`) within the active Set 1 framework.

#### Plane 15 (SPUA-A) Provisional Open Slots
* `U+F1D00`–`U+F1EFF` | `U+F26B0`–`U+F26FF` | `U+F28E0`–`U+F28FF` | `U+F2960`–`U+F29FF`
* `U+F3400`–`U+F4DFF` | `U+F5150`–`U+F7FFF` | `U+F81B0`–`U+F8FFF` | `U+FA000`–`U+FAFFF`
* `U+FC000`–`U+FDFFF` | `U+FF200`–`U+FF27F` | `U+FF2A0`–`U+FF2BF`
* `U+FFE00`–`U+FFEFF` | `U+FFF00`–`U+FFFBF`

> **Note (SPUCE Fragments reduction, 2026-10-19):** SPUCE reduced its Zone 12 Fragments allocation from `U+FFF00`–`U+FFFEF` to `U+FFFC0`–`U+FFFEF`. The remaining Fragments allocation is therefore exactly `U+FFFC0`–`U+FFFEF`, and the released range `U+FFF00`–`U+FFFBF` is tracked in Set 1 as `PROVISIONAL_RNUR_OPEN_SLOT` (charted as `???` territory in `S1/Roadmap/spua-a_roadmap.md`). The released range is neither a SPUCE allocation nor confirmed UCSUR space.

> **Note on Provisional Eviction:** All ranges designated as `PROVISIONAL_RNUR_OPEN_SLOT` are held via defensive zoning under an active upstream vacuum. These are subject to the absolute Upstream Authority hierarchy and the Eviction Clause. If conflicting native allocations emerge upstream, these slots face automatic clean relocation routing to Set 2+ execution layers to prevent string parsing pollution. The former BMP provisional reservations `U+EE60–U+EE8F` and `U+EFB0–U+EFFF` are no longer part of this list: they were dissolved into permanent space during the Set 1 → Set 2 migration (see §3.1.5) and their addresses are now SPUCE allocations.

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

As of the SPUCE allocation update of 2026-10-22, the active Set 2 BMP allocations are: ConstantScript (`U+E000`–`U+E81F`, unchanged), the six relocated RNUR scripts (`U+E820`–`U+E99F`, see §3.1.2), and the relocated Placeholder allocation (`U+E9A0`–`U+EAFF`, see §3.1.3), with `U+EB00`–`U+F8FF` remaining open sandbox space. The dissolved `???` reservations from Set 1 are deliberately absent: no Set 2 record represents them as allocations or reservations.

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

##### 3.5.3.1 Tier A: Non-Provisional Allocations & Gaps (Plane 16 Gaps and Locked Plane 15 Sectors)
This tier applies to finalized allocations and the permanent structural space tracking slots of Plane 16. Because these ranges represent rigid, permanent RNUR real estate, an upstream collision triggers a precise, deterministic architectural shift:
1. **Parallel Addressing Mirror:** The registry master pipeline automatically triggers a 1:1 structural eviction. Instead of shifting to an unassigned block, the affected script mirrors directly into its exact corresponding mathematical coordinate address within **Set 2** (e.g., a collision at Set 1 $U+100580$ maps directly to Set 2 $U+100580$).
2. **Flag Deployment:** The script’s historical data table entry is appended with an `UPSTREAM_COLLISION` flag.
3. **Runtime Asset Override:** For software environments operating under RNUR compliance, the local font pre-processor runtime engine forces high-priority asset targeting over the native host system string fallback to prevent immediate layout corruption.

##### 3.5.3.2 Tier B: Provisional Allocations (BMP Provisional Blocks & Empty Plane 15 Gaps)
This tier applies to sectors explicitly designated as Provisional RNUR Territory — including the BMP provisional blocks `U+F5C0–U+F5FF`, `U+F700–U+F71F`, `U+F720–U+F7FF` and `U+F820–U+F87F` — which operate defensively under an active upstream vacuum. Because these regions are subject to an absolute Upstream Authority hierarchy, a collision triggers an agile escape vector:
1. **Dynamic Database Migration:** The registry master pipeline executes an automated offline database migration, shifting the displaced script's records away from the collision zone and into the first available, unassigned tracking ranges at the base of the Set 2 sandbox layer.
2. **Metric Refactoring:** Font compilation tools rebuild and refactor the underlying glyph metrics and code point mappings to align cleanly with the new sandbox target plane destination.
3. **Upstream Compliance:** The vacated Set 1 coordinate pair $(1, C)$ is updated in the master database to mirror the native upstream allocation, completely clearing out runtime font rendering pollution.

> **Migration note (BMP `???` dissolution):** The former BMP provisional blocks `U+EE60–U+EE8F` and `U+EFB0–U+EFFF` no longer exist as RNUR provisional reservations. During the Set 1 → Set 2 migration they were dissolved into permanent space per §3.1.5 — no Set 2 destinations were assigned to them — and their Set 1 addresses now belong to the SPUCE Atlantean and Quốc âm tân tự allocations. Tier B routing no longer applies to those ranges. The remaining BMP provisional blocks (`U+F5C0–U+F5FF`, `U+F700–U+F71F`, `U+F720–U+F7FF`, `U+F820–U+F87F`) remain Tier B provisional ranges (§3.1.4, §3.3), subject to the Set 2 relocation routing described above.

##### 3.5.4 RNUR Embassy Space in SPUCE (Shared Private Use Character Encoding)
To maintain permanent, collision-safe visibility for active Set 1 scripts within the shared SPUCE registry, RNUR holds a dedicated embassy layer inside SPUCE territory. SPUCE has formally reserved the `U+F9000`–`U+F9FFF` and `U+FB000`–`U+FBFFF` sectors for RNUR, making these ranges **permanent Tier A slots owned by RNUR** and not subject to the eviction vectors defined in §3.5.3.

These sectors are tracked in `data/set1_master.csv` as permanent `OPEN_SLOT` territory — permanently reserved for RNUR, yet open for submission:

* **`U+F9000`–`U+F9FFF`** (RNUR Embassy Space in SPUCE)
* **`U+FB000`–`U+FBFFF`** (RNUR Embassy Space in SPUCE)

The Placeholder cipher is also allocated within the RNUR SPUA-A embassy space at `U+F92C0`–`U+F941F` (mirroring the RNUR Set 2 BMP PUA allocation `U+E9A0`–`U+EAFF`).

#### 3.5.5 Plane 15 Zone Map (SPUCE Provisional Zoning)

SPUCE provisionally partitions Plane 15 (SPUA-A) into thirteen zones. Two of them, `U+F9000`–`U+F9FFF` and `U+FB000`–`U+FBFFF`, are carved out and permanently reserved for RNUR as the embassy layer described in §3.5.4, and `U+FE000`–`U+FEFFF` is reserved for SPUCE admin and FontStruct user @erictom333. The full grid is charted in `S1/Roadmap/spua-a_roadmap.md`:

| Zone | Code Range | Scope | Steward |
| :--- | :--- | :--- | :--- |
| **1** | `F0000–F2AFF` | Large UCSUR scripts | SPUCE |
| **2** | `F2B00–F4FFF` | Extensions of existing Unicode scripts and existing real-world scripts | SPUCE |
| **3** | `F5000–F5FFF` | Notation, ciphers, undeciphered scripts, and pseudohistorical scripts | SPUCE |
| **4** | `F6000–F7FFF` | Constructed scripts from existing media | SPUCE |
| **5** | `F8000–F8FFF` | Constructed scripts for existing languages | SPUCE |
| **6** | `F9000–F9FFF` | Constructed scripts for existing languages | Reserved for RNUR |
| **7** | `FA000–FAFFF` | Constructed scripts for constructed languages | SPUCE |
| **8** | `FB000–FBFFF` | Constructed scripts for constructed languages | Reserved for RNUR |
| **9** | `FC000–FDFFF` | Constructed scripts by FontStruct users | SPUCE |
| **10** | `FE000–FEFFF` | Personal reservation | Reserved for @erictom333 |
| **11** | `FF000–FFEFF` | Symbols | SPUCE |
| **12** | `FFFC0–FFFEF` | Fragments | SPUCE |
| **13** | `FFFF0–FFFFF` | Specials | SPUCE |

> **Note (SPUCE Fragments reduction, 2026-10-19):** SPUCE reduced the Zone 12 Fragments allocation to `U+FFFC0`–`U+FFFEF`, leaving `U+FFF00`–`U+FFFBF` outside every SPUCE zone. That released range is tracked in Set 1 as `PROVISIONAL_RNUR_OPEN_SLOT` (§3.3) and is not confirmed UCSUR space.

> **Provenance (2026-10-19):** The public SPUCE Plane 15 Roadmap still showed the pre-reduction Fragments zone line and the GS Unicode 3.0 Plane F map listed `FFFxx` as unassigned when this record was reconciled. RNUR follows the maintainer-confirmed reduction to `FFFC0–FFFEF`; `FFF00–FFFBF` remains provisional RNUR space.

> **Note (Plane 15 status reconciliation, 2026-10-19):** `¿Hacm?` (`U+F2700`–`U+F27FF`), `¿Liparxe?` (`U+F2800`–`U+F282F`), `¿Shaleian?` (`U+F2830`–`U+F289F`), and `¿Visible Speech Extended-I?` (`U+F2900`–`U+F295F`) originate in UCSUR: UCSUR reserves those four ranges, and in this repository “UCSUR-Only Allocations” means allocated in UCSUR rather than CSUR — not that SPUCE has never named the range. All four are therefore charted as UCSUR-only allocations (🟩). The SPUCE Plane 15 Roadmap names the same four ranges; that overlap is recorded here as provenance, not as SPUCE ownership. UCSUR's allocation table does not yet list the four as registrations and its roadmap still marks them `¿Hacm?`, `¿Liparxe?`, `¿Shaleian?`, and `¿Visible Speech Extended?`, so the green classification asserts allocation-level UCSUR origin, not a published UCSUR character chart. Fairfax HD maps the first three ranges completely and lists the fourth as planned — observed font usage, not a UCSUR registration. The exact RNUR label is `Visible Speech Extended-I`; Fairfax HD and the GS Unicode 3.0 Plane F map use the shorter alias `Visible Speech Extended`. `Zbalermorna` (`U+F28A0`–`U+F28DF`) is a named UCSUR proposal and also remains a UCSUR-only allocation (🟩) without the marker. The `¿Script Name?` notation marks a UCSUR-included script whose detailed proposal has not yet been written — a proposal-completeness marker, not a statement that UCSUR has not included the script. These seven Plane 15 scripts — `¿Hacm?`, `¿Liparxe?`, `¿Shaleian?`, `¿Visible Speech Extended-I?`, `¿Sitelen Pona Extended-A?` (`U+F1A00`–`U+F1AFF`), `¿Sitelen Pona Extended-B?` (`U+F1F00`–`U+F1FFF`), and `¿Quikscript?` (`U+F2680`–`U+F26AF`) — are all UCSUR-included and all lack a detailed proposal, so they remain in the UCSUR-Only (🟩) class. It is distinct from the `???` Provisional RNUR Open Slot (§3.3), which denotes provisional RNUR lease territory rather than a script awaiting a written proposal. Fairfax HD's complete Quikscript coverage is observed font usage, not a detailed proposal or registration.

Because SPUCE zoning is provisional and does not cover every code point in a zone, only the space SPUCE leaves unallocated inside its zones stays RNUR territory. Once SPUCE allocates a script, those code points leave the RNUR provisional list in §3.3 and become SPUCE allocations — for example `U+F50F0`–`U+F514F` (Enochian, Litterae Ignotae, and Theban) and `U+FF700`–`U+FF9FF` (Control Pictures Extended-II, soon going to be encoded in Plane 16). Scripts that remain UCSUR-listed keep their UCSUR classification instead of the zone steward. The four Plane 15 scripts noted above — `¿Hacm?`, `¿Liparxe?`, `¿Shaleian?`, and `¿Visible Speech Extended-I?` — are UCSUR-reserved ranges that predate the SPUCE naming, so they keep their UCSUR classification even though the SPUCE Plane 15 roadmap names them.

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
