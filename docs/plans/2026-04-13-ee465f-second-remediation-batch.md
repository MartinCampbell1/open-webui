# ee465f replay second remediation batch

Date: 2026-04-13
Target repo: `/Users/martin/open-webui-replay-ee465f`
Live target: `http://127.0.0.1:18081/`
Priority: second bounded remediation batch after user live review

## Why this batch exists

The user reviewed the current replay instance live on port 18081.
Feedback is positive on speed/performance:
- loading is fast
- dialogs scroll/load quickly
- this is a major win and must not regress

But the user reports several remaining problems that now matter more than the earlier batch:
- ugly yellow Hermes `H` logo that clashes with the monochrome portal
- tool transcript spam can occupy most of the screen
- tool calls need grouping/collapsing/accordion behavior
- type hierarchy regressed; main response typography feels more cramped / worse than a previously approved state
- previously liked gray code/script/account blocks and copyable shell blocks seem to have regressed/disappeared on recent messages
- ugly frame/outline treatment in some tool rows/cards
- tool icons are too generic/samey; different tools should have differentiated iconography
- user reports a hard freeze/throttle bug when opening an older dialog; old dialog becomes unscrollable/uninteractive

## Read first
- `/Users/martin/open-webui-replay-ee465f/AGENTS.md`
- previous brief: `/Users/martin/open-webui-replay-ee465f/docs/plans/2026-04-12-ee465f-ui-remediation-brief.md`
- `/Users/martin/open-webui/HANDOFF_HERMES_UI_2026-04-11_CONTEXT.md`
- `/Users/martin/open-webui/handoff.md`

## Grounding artifacts

Fresh user-provided artifacts:
- `/Users/martin/Desktop/Снимок экрана — 2026-04-13 в 09.22.56.png`
- `/Users/martin/Desktop/Снимок экрана — 2026-04-13 в 09.23.19.png`
- `/Users/martin/Desktop/Снимок экрана — 2026-04-13 в 09.24.51.png`
- `/Users/martin/Desktop/Снимок экрана — 2026-04-13 в 09.25.06.png`
- `/Users/martin/Desktop/Снимок экрана — 2026-04-13 в 09.26.05.png`
- `/Users/martin/Desktop/Снимок экрана — 2026-04-13 в 09.26.19.png`
- `/Users/martin/Desktop/Запись экрана — 2026-04-13 в 09.26.49.mov`

Grounding from review/orchestrator:
- `09.25.06.png` shows tool transcript rows (`patch`, `terminal`) with repetitive flat rows, weak hierarchy, generic icons, weak active outline, and clear need for grouping/collapsing.
- `09.26.19.png` shows previously-liked copyable shell/code block treatment with `bash` label and actions like `Свернуть / Сохранить / Копировать`; user explicitly wants this quality preserved/restored.
- extracted video frames confirm old-dialog/tool transcript views can become dominated by tool rows and feel throttle/freeze-prone.

## Non-negotiable product rules

- Do NOT regress current speed/performance.
- Do NOT redesign the whole shell.
- Do NOT introduce a new visual system.
- Preserve Open WebUI identity.
- Keep the now-good fast loading/scrolling behavior.
- Restore/refine transcript quality without bloating the UI.

## Exact user feedback translated into implementation tasks

### P0 — must do in this batch

1. Replace ugly yellow Hermes logo with monochrome-compatible mark
- Current yellow `H` is explicitly rejected by user
- Replace with a black/white or neutral monochrome `H` treatment that fits the portal
- Keep it simple and brand-compatible, not colorful
- Change wherever this logo currently appears in the shell and relevant transcript/header/avatar contexts

2. Group/collapse tool call spam
- Long tool sequences currently consume too much vertical space
- Need accordion/stack/grouping behavior for repeated tool calls
- Strong target behavior:
  - repeated/adjacent tool rows can be visually grouped
  - collapsed by default when long
  - expandable on demand
  - summary first, details second
- Avoid showing 20 near-identical tool rows at full height by default

3. Differentiate tool iconography by tool type
- Current tool icons/checks are too generic and all feel the same
- Different tools should get distinct, appropriate icon treatment, e.g.:
  - terminal/shell
  - search/web
  - file/read_file
  - patch/edit
  - memory/skills if relevant
- Keep iconography subtle and Open WebUI-compatible, not colorful toy icons

4. Restore approved transcript typography quality
- User reports regression: main response text feels more cramped / more stuck together than approved state
- Audit message text styling and restore calmer, more readable hierarchy
- Specifically revisit:
  - line-height
  - paragraph spacing
  - heading/text separation
  - density around prose after tool output
- Preserve compactness, but do not let prose become visually glued together

5. Restore/refine gray copyable code/script/account blocks
- User explicitly liked the prior treatment where scripts/accounts/commands were shown in gray, copy-friendly blocks
- Recent messages seem to have lost/regressed this treatment
- Restore or improve the formatting for:
  - bash scripts
  - shell commands
  - account/config snippets
  - copy/save affordances where appropriate
- Target the “good” quality seen in `09.26.19.png`

6. Remove ugly outline/frame treatment on tool rows/cards
- User explicitly called out current frame/outline as cheap/"kolkhoz"
- Tone down or redesign the selected/outlined state so it feels cleaner and less clunky
- Especially important for tool transcript rows and active row states

### P1 — debug/fix if feasible within same bounded slice

7. Investigate hard freeze on older dialog
- User reports opening an older dialog causes a hard freeze/throttle:
  - cannot click
  - cannot scroll to bottom
  - UI effectively locks up
- Investigate likely causes in transcript rendering/tool transcript virtualization/expansion behavior
- Fix if the cause is local and bounded
- If full fix is too risky in this batch, at minimum reduce the trigger surface:
  - collapse long tool groups by default
  - avoid rendering everything expanded
  - reduce DOM weight / repeated controls where possible

### P2 — only if cheap and coherent after P0

8. Keep the now-good speed while reducing transcript chrome noise
- repeated labels like `Details`, repetitive status chrome, duplicated action bars should not dominate the transcript
- reduce noise without harming affordance

## Suggested implementation approach

Recommended coherent slice:
1. tool transcript refactor first
   - grouping/collapse
   - differentiated icons
   - better row hierarchy
   - calmer outline treatment
2. transcript typography restoration
3. gray copyable command/code block restoration
4. monochrome logo replacement
5. freeze mitigation if tied to long expanded transcript rendering

## Acceptance criteria

This batch is successful only if:
- yellow logo is gone and replaced by a monochrome-compatible mark
- long tool sequences no longer take over the whole screen by default
- tool types are visually distinguishable without gaudiness
- transcript prose regains the better approved typographic feel
- code/script/account blocks again feel polished, gray, and easy to copy
- ugly heavy outlines/frames are reduced or redesigned
- old-dialog freeze is fixed or materially mitigated
- speed/performance stays excellent

## Deliverable expected from Forge

Return:
1. short plan
2. exact files changed
3. what was implemented for each P0 item
4. freeze root cause / mitigation note
5. what remains deferred
6. quick verification notes
