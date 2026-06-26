<div align="center">

# Lanshu Animated Architecture Diagram

**岚叔动态架构图: premium hand-drawn animated architecture diagrams for articles, systems, and workflows.**

[![Codex Skill](https://img.shields.io/badge/Codex-Skill-22C86F?style=for-the-badge)](./SKILL.md)
[![Python](https://img.shields.io/badge/Python-3.9%2B-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Pillow](https://img.shields.io/badge/Pillow-Renderer-8A2BE2?style=for-the-badge)](https://python-pillow.org/)
[![Excalidraw](https://img.shields.io/badge/Excalidraw-JSON-6965DB?style=for-the-badge)](https://excalidraw.com/)
[![Animated GIF](https://img.shields.io/badge/Animated-GIF-FFB000?style=for-the-badge)](./scripts/render_animated_diagram.py)
[![License](https://img.shields.io/badge/License-MIT-111827?style=for-the-badge)](./LICENSE)

`JSON spec` -> `.excalidraw` + `.png` + animated `.gif`

</div>

<p align="center">
  <a href="#gallery">Gallery</a> ·
  <a href="#quick-start">Quick Start</a> ·
  <a href="#features">Features</a> ·
  <a href="#spec-structure">Spec</a> ·
  <a href="#verification">Verification</a>
</p>

`lanshu-animated-architecture-diagram` is a Codex skill and local renderer for creating premium black-canvas technical diagrams with hand-drawn typography, editable Excalidraw output, static PNG previews, and genuinely animated GIFs.

It is designed for article explanations, system architecture diagrams, process diagrams, and DailyDoseOfDS-style black-background technical sketches.

## Gallery

The default visual system uses a dark canvas, moving flow highlights, pulsing modules, subtle grain, vignette, and a top-right hand-drawn signature.

<table>
  <tr>
    <td width="50%" align="center">
      <strong>Claude Loops</strong><br />
      <img src="./assets/previews/claude-loops.gif" alt="Claude Loops animated architecture diagram" width="100%" />
    </td>
    <td width="50%" align="center">
      <strong>Memory Pack</strong><br />
      <img src="./assets/previews/memory-pack.gif" alt="Memory Pack animated architecture diagram" width="100%" />
    </td>
  </tr>
</table>

## Features

- Generates `.excalidraw`, `.png`, and animated `.gif` from one JSON spec
- Produces real animation with moving glow points and pulsing module highlights
- Keeps the `.excalidraw` source editable and text-based
- Uses local Python rendering through Pillow
- Does not require Excalidraw, browser automation, ImageMagick, remote APIs, or external icon libraries
- Includes frame-diff verification to prove GIF motion
- Uses a fixed high-quality layout for clean technical storytelling

## Outputs

Each render produces:

```text
<basename>.excalidraw
<basename>.png
<basename>.gif
```

The default canvas is:

```text
1210 x 1138
20 fps
41 frames
2.05 seconds
```

## Quick Start

```bash
git clone https://github.com/cclank/lanshu-animated-architecture-diagram.git
cd lanshu-animated-architecture-diagram
python3 -m pip install -r requirements.txt
python3 scripts/render_animated_diagram.py \
  --spec assets/default-spec.json \
  --outdir outputs \
  --basename sample \
  --verify
```

## Installation

Place this folder in your Codex skills directory:

```bash
~/.codex/skills/lanshu-animated-architecture-diagram
```

Typical local install path:

```bash
${CODEX_HOME:-$HOME/.codex}/skills/lanshu-animated-architecture-diagram
```

Install the runtime dependency:

```bash
python3 -m pip install -r requirements.txt
```

## Use With Codex

Invoke the skill by name:

```text
Use $lanshu-animated-architecture-diagram to turn this article into a premium hand-drawn animated architecture GIF.
```

Chinese prompt example:

```text
用 $lanshu-animated-architecture-diagram 把这篇文章整理成岚叔动态架构图，输出 GIF、PNG 和 Excalidraw。
```

## CLI Usage

Start from the bundled template:

```bash
cp assets/default-spec.json work/my-diagram-spec.json
```

Render:

```bash
python3 scripts/render_animated_diagram.py \
  --spec work/my-diagram-spec.json \
  --outdir outputs \
  --basename my-diagram \
  --verify
```

The `--verify` flag prints sampled frame differences. Nonzero changed pixels confirm that the GIF is genuinely animated.

## Spec Structure

The renderer uses `assets/default-spec.json` as a compact art-directed template.

Most edits happen in these fields:

```text
signature
title.prefix
title.highlight
title.subtitle
inputs
core.cards
decision
output
left_panel
center_panel
right_panel
```

Supported icon keys:

```text
folder
file
scan
shield
db
hash
package
```

For details, see [references/spec-format.md](./references/spec-format.md).

## Verification

Validate the skill structure:

```bash
python3 ${CODEX_HOME:-$HOME/.codex}/skills/.system/skill-creator/scripts/quick_validate.py \
  ${CODEX_HOME:-$HOME/.codex}/skills/lanshu-animated-architecture-diagram
```

Validate GIF media parameters:

```bash
ffprobe -v error -select_streams v:0 -count_frames \
  -show_entries stream=width,height,r_frame_rate,avg_frame_rate,nb_read_frames \
  -show_entries format=duration \
  -of default=noprint_wrappers=1 outputs/my-diagram.gif
```

Validate animation:

```bash
python3 scripts/render_animated_diagram.py \
  --spec assets/default-spec.json \
  --outdir outputs \
  --basename sample \
  --verify
```

## Dependencies

Required:

- Python 3.9+
- Pillow 10.0.0+

Install Python packages with:

```bash
python3 -m pip install -r requirements.txt
```

Optional:

- `ffprobe` for media inspection
- Excalidraw web app or editor plugin for manual editing of generated `.excalidraw` files

## Project Layout

```text
lanshu-animated-architecture-diagram/
├── SKILL.md
├── README.md
├── LICENSE
├── requirements.txt
├── agents/
│   └── openai.yaml
├── assets/
│   ├── default-spec.json
│   └── previews/
│       ├── claude-loops.gif
│       └── memory-pack.gif
├── references/
│   └── spec-format.md
└── scripts/
    └── render_animated_diagram.py
```

## Design Notes

This project intentionally keeps the visual system narrow:

- Dark canvas
- Hand-drawn title treatment
- Top input strip
- Middle core pipeline
- Bottom source, layer, and pack panels
- Top-right signature
- Clean static diagram with motion added only in GIF overlays

That constraint keeps outputs consistent and polished across different architecture topics.

## License

MIT
