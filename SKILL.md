---
name: lanshu-animated-architecture-diagram
description: Create premium hand-drawn architecture and process diagrams in the Lanshu animated GIF style, with editable .excalidraw files, static PNG previews, and genuinely animated GIFs with moving flow highlights. Use this skill whenever the user asks for 岚叔动态架构图, Excalidraw-like diagrams, DailyDoseOfDS-style black-background sketches, animated architecture/process GIFs, polished flowcharts, visual explanations of articles or system designs, or asks to replicate or improve a reference diagram with hand-drawn animated effects.
---

# Lanshu Animated Architecture Diagram

Create a polished black-background hand-drawn technical diagram with:

- Editable `.excalidraw` source
- Static `.png` preview
- Animated `.gif` with moving glow points and pulsing module highlights

Use the bundled renderer for deterministic output. Avoid external icon libraries unless the user explicitly provides audited assets.

## Workflow

1. Extract the diagram content.
   - For an article or long post, identify the core architecture, actors, stages, data flow, decisions, and final outputs.
   - For a reference image, preserve the visual grammar: title structure, panels, arrows, density, and signature placement.

2. Create a spec JSON.
   - Start from `assets/default-spec.json`.
   - Keep labels short. Read `references/spec-format.md` when field details or copy length guidance are needed.
   - Use the user’s language for explanatory labels unless the reference style clearly calls for English titles.

3. Render the outputs.

```bash
python /path/to/skill/scripts/render_animated_diagram.py \
  --spec /path/to/spec.json \
  --outdir /path/to/output-dir \
  --basename descriptive-name \
  --verify \
  --check
```

4. Validate before delivery.
   - Confirm GIF dimensions, FPS, frame count, and duration with `ffprobe`.
   - Use `--verify` output or `--check` to prove the GIF is not static.
   - Confirm `.excalidraw` JSON has unique IDs, text uses `fontFamily: 5`, and `files` is empty. `--check` validates these output contracts automatically.
   - Open the PNG preview visually and fix overlap, cramped text, or weak hierarchy.

5. Deliver the three files.
   - Show the GIF preview when the interface supports local images.
   - Link the PNG and `.excalidraw` source.

## Style Rules

- Use a dark canvas with a thin outer rounded frame.
- Use one highlighted title phrase in a green capsule.
- Put the author signature in the top-right brand slot unless the user asks otherwise.
- Prefer clean white main arrows. Use colored motion only in the GIF overlay.
- Keep static diagrams restrained. Let animation add motion, not clutter.
- Use short text. If a phrase cannot fit, rewrite it instead of shrinking until unreadable.
- Use built-in simple icons: `folder`, `file`, `scan`, `shield`, `db`, `hash`, `package`.

## Spec Authoring Hints

Map common content to the fixed layout:

- `inputs`: source systems, triggers, documents, tools, or user actions
- `core.cards`: the three main stages of the process
- `decision`: the quality gate or readiness check
- `left_panel`: memory/context/source material
- `center_panel`: internal layers, safeguards, archive stores, or pipeline internals
- `right_panel`: packaged outputs, reusable assets, generated reports, or agent-facing artifacts

If the subject has more than three stages, group adjacent steps into three core cards and move details into the lower panels.

## Verification Commands

Use these checks after rendering:

```bash
ffprobe -v error -select_streams v:0 -count_frames \
  -show_entries stream=width,height,r_frame_rate,avg_frame_rate,nb_read_frames \
  -show_entries format=duration \
  -of default=noprint_wrappers=1 output.gif
```

```bash
python /path/to/skill/scripts/render_animated_diagram.py \
  --spec spec.json \
  --outdir outputs \
  --basename diagram \
  --verify \
  --check
```

The `--verify` report should show nonzero changed pixels between sampled GIF frames.
The `--check` report should return `"ok": true`; it exits nonzero on contract failures.
