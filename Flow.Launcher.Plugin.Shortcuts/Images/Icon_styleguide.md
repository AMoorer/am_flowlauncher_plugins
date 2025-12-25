## 1. Proposed filenames (semantic, composable, boring in the best way)

Based on the corner glyphs visible in your images, here’s a clean, consistent naming scheme:

```
icon_dog_vr_display.png
icon_dog_vr_featured.png
icon_dog_vr_delete.png
icon_dog_vr_document.png
icon_dog_vr_folder.png
icon_dog_vr_sensor.png
icon_dog_vr_ai_core.png
icon_dog_vr_processor.png
```

Notes on intent:

- `dog_vr` is the **stable namespace** — this lets you add future dog-based icon sets without collisions.
- The final token is always the **semantic role**, not the visual metaphor.
- Avoid plurals unless the concept itself is plural (e.g. `assets`, `logs`).

If you later introduce stateful variants, they compose naturally:

```
icon_dog_vr_folder_active.png
icon_dog_vr_folder_disabled.png
icon_dog_vr_folder_filled.png
```

This plays very nicely with both humans and build systems.

------

## 2. Style guide & parametric system document

Below is a ready-to-drop document.

------

### **Dog-VR Icon System — Style & Parametric Design Guide**

#### Overview

This icon system is built around a single, recognizable silhouette:
 **a dog wearing a VR headset**, rendered in bold monochrome linework.

The dog functions as a **semantic anchor**. Meaning is conveyed by pairing this anchor with a **secondary glyph** that represents role, action, or category.

This approach optimizes for:

- Rapid recognition
- Visual consistency
- Scalable icon vocabulary
- Parametric generation

------

#### Core Design Principles

**1. Persistent Anchor**

- The dog-with-VR silhouette remains constant across the entire icon family.
- Orientation, proportions, and headset geometry must not change.
- Minor internal simplifications are allowed only if required for small sizes.

**2. Monochrome First**

- Icons are authored in black on transparent background.
- No gradients, shadows, or color are part of the base design.
- Color may be applied downstream via tinting, not baked into the asset.

**3. Stroke Discipline**

- Primary stroke weight must survive at 48×48 px.
- Avoid strokes thinner than ~1.25 px at final resolution.
- Secondary glyphs may be equal or slightly heavier in stroke weight than the dog outline.

**4. Corner Grammar**

- Secondary glyphs occupy a consistent corner (recommended: bottom-left).
- Glyphs should not exceed ~30% of the icon’s total area.
- Placement is optical, not mathematical — avoid tangent collisions with the dog silhouette.

------

#### Semantic Composition Model

Each icon expresses meaning as:

```
[ DOG_VR ] + [ ROLE / ACTION GLYPH ]
```

Examples:

- Dog + monitor → display / UI
- Dog + folder → library / collection
- Dog + trash → delete / remove
- Dog + star → featured / favorite
- Dog + circuit → compute / AI

Users learn the anchor once; meaning scales combinatorially.

------

#### State Variants (Optional but Recommended)

Without introducing color, state can be communicated via fill and opacity:

- **Default**: outline only
- **Active / Selected**: filled dog silhouette + outlined glyph
- **Disabled**: outline at reduced opacity
- **Alert / Warning**: optional badge glyph, not color

This keeps the system accessible and UI-agnostic.

------

#### Parametric Generation Strategy

This icon family is well-suited to parametric or procedural generation.

**Recommended structure:**

- **Master Dog Silhouette**
  - Single vector source (SVG or equivalent)
  - Locked proportions and orientation
  - Exported as a reusable layer
- **Glyph Library**
  - Individual vector glyphs (folder, trash, star, circuit, etc.)
  - Normalized stroke weight and bounding box
  - Designed to scale independently
- **Composition Rules**
  - Anchor placement: fixed
  - Glyph placement: rule-based (corner + padding)
  - Scale factor: glyphs scale relative to anchor, not canvas

**Pipeline Example:**

1. Load dog silhouette
2. Load glyph by semantic name
3. Apply scale + offset rules
4. Export at target resolutions (48×48, 64×64, 128×128)
5. Apply optional state transforms (fill, opacity)

This enables batch generation, theming, and future expansion with minimal manual work.

------

#### Naming Convention

```
icon_dog_vr_<semantic_role>[_<state>].png
```

Examples:

```
icon_dog_vr_folder.png
icon_dog_vr_folder_active.png
icon_dog_vr_ai_core.png
```

Names describe *what the icon means*, not what it looks like.

------

#### Design North Star

If forced to choose between:

- visual cleverness
- semantic clarity

Always choose clarity.

These icons succeed because they are iconic, not illustrative.