# ee465f replay strict remediation batch

Date: 2026-04-13
Target repo: `/Users/martin/open-webui-replay-ee465f`
Live target: `http://127.0.0.1:18081/`
Mode: strict handoff of user intent, minimal reinterpretation

## This brief overrides prior shorthand summaries

Do NOT rely on my paraphrase if it conflicts with the source docs below.
You must use the following as direct source-of-truth inputs:

1. `/Users/martin/Downloads/hermes_typography_tz.md`
2. `/Users/martin/Downloads/hermes_quick_wins.md`
3. user-provided screenshots/video from `2026-04-13`
4. previous brief only for context, not as typography source-of-truth:
   - `/Users/martin/open-webui-replay-ee465f/docs/plans/2026-04-13-ee465f-second-remediation-batch.md`

## Core correction

The user clarified an important point:
- typography should NOT merely be “restored to some older version”
- typography should be implemented according to `hermes_typography_tz.md`
- the target perception is ChatGPT-like readability principles, not a fuzzy return to an earlier local state

That means:
- stable reading axis
- calmer, narrower reading column
- quieter chrome
- proper markdown rhythm
- gray inline code/path/link/account emphasis where appropriate
- real code-block treatment for inserts/commands like in the user-provided reference/video

## Direct source requirements from `hermes_typography_tz.md`

These are not optional suggestions. They are the design target.

### Reading system
Implement Hermes as a reading system, not a shell with text inside it.
Primary actor on screen in reading mode must be the model answer.
Sidebar / toolbar / badges / archive hints / tool traces / composer are secondary.

### Width and reading axis
Use these as implementation targets where feasible in this shell:
- conversation shell width target: max-width around 920px, do not expand uncontrollably
- reading column target: around 68ch–72ch, roughly 720px–760px max for body content
- align the left edge of:
  - headings
  - paragraphs
  - lists
  - dividers
  - composer
  - inline tool/attachment wrappers
- do NOT let text column and composer live on different width systems

### Typography scale
Use calm system-stack body typography.
Body text target:
- 16px
- line-height around 1.6–1.65
- weight around 400–450

Headings target:
- H2 around 24/32 weight ~620
- H3 around 20/28 weight ~620

Meta text target:
- 13px–14px
- clearly quieter than body

Do NOT:
- make body text heavier for false clarity
- overuse bold
- let useful text and utility/meta text sit too close in visual importance

### Markdown rhythm
Treat markdown as editorial flow, not raw HTML dump.
Targets:
- paragraphs with clear spacing
- calm headings
- quiet divider
- inline code with soft gray treatment
- code blocks with proper dedicated treatment
- blockquotes with quiet left rule

### Inline code / gray emphasis
Important user requirement:
- paths, links, commands, accounts, and similar inline technical artifacts should get the gray-emphasis treatment the user liked
- this means soft gray inline code/path wrappers where semantically appropriate
- do not flatten them into plain text

### Code blocks / shell blocks
Important user requirement:
- when there are code/script inserts, they should use the dedicated code-block treatment like in the screenshot/video the user referenced
- the `09.26.19` screenshot quality is a positive reference:
  - dedicated code block
  - clear shell language label where appropriate
  - copyable / save-friendly affordances
  - visually separate from prose

### Composer
From the typography/system doc and quick wins:
- composer should not be huge and panel-like
- narrow it toward the reading axis
- reduce idle mass/height/contrast if needed
- align it with the reading column

## Direct source requirements from `hermes_quick_wins.md`

### Sidebar
Sidebar is currently too heavy and must be quieted.
Target model:
- brand row
- primary nav
- archive/history navigation
- recent chats

Specific user concern to preserve exactly:
- the selected dialog state on the left currently has a shadow/treatment the user explicitly dislikes
- the user marked this in red on screenshot
- this selected-dialog shadow/treatment must be changed
- do NOT keep or reintroduce a heavy shadow/cheap selected-state treatment
- selected state should be calmer, cleaner, and less generic/cheap

Also from quick wins:
- reduce explanatory copy by default
- soften count badges
- simplify active list item
- section labels like Today/Yesterday/Previous 7 days should be quieter

### Chrome / utility layer
- top-right utility layer is too visually loud
- group rare actions into overflow if needed
- lower their prominence relative to content

### Tool blocks / traces
From quick wins + user feedback:
- tool traces must not break reading flow
- short tool/status traces should be compact inline rows
- details should live behind disclosure/collapse
- they must not carry the same visual weight as useful content

### Message actions
- hide or strongly mute message action row in idle
- show strongly on hover/focus only

### Card overuse
- reduce dark rounded box/card treatment where plain layout is enough
- too many dark rounded boxes create dashboard feel

## Additional explicit user requirements from the new message

1. Replace ugly yellow Hermes `H`
- user explicitly dislikes the yellow `H`
- replace with black/white / monochrome-compatible `H`
- it should look organic in the portal

2. Tool calls must be grouped / accordionized
- long tool sequences must not take over the screen
- repeated tool runs should be grouped and collapsible
- summary first, details second

3. Tool types need differentiated icons
- terminal, search, file, patch, web, etc. should not all feel identical
- keep icon set subtle and coherent

4. Typography regression must be fixed according to the typography spec, not guessed
- text currently feels more glued together again
- main answer typography must follow the reading-system spec above

5. Restore the liked gray technical emphasis and copyable block treatment
- gray inline emphasis for links/paths/etc.
- proper dedicated code-block treatment for code/script inserts
- exactly the class of thing the user praised as “super” in the screenshot/video

6. Freeze/throttle bug on old dialogs
- user reports opening an older dialog causes hard freeze / no scrolling / no interaction
- investigate transcript/tool rendering and mitigate/fix
- collapsing/grouping tool spam is part of the mitigation surface

7. Cheap frame/outline treatment must be removed
- user explicitly called the current frame/outline ugly/cheap
- this applies especially to tool rows and selected-ish states

## Strong implementation direction

Preferred bounded batch order:
1. transcript reading system / typography pass using `hermes_typography_tz.md`
2. tool transcript compaction and grouping
3. restore gray inline emphasis + dedicated code block treatment
4. selected-dialog state cleanup in sidebar (remove disliked shadow treatment)
5. monochrome logo replacement
6. freeze mitigation for old dialogs

## What not to do
- Do not improvise a new visual system.
- Do not turn this into a generic dashboard cleanup without honoring the typography spec.
- Do not say “looks cleaner” while ignoring reading-column/composer/markdown rhythm.
- Do not keep the current selected-dialog shadow if it is only slightly softened; the complaint is specific and must be addressed.
- Do not preserve tool spam as full-height repeated rows.

## Acceptance criteria
This batch is successful only if:
- typography meaningfully follows `hermes_typography_tz.md`
- reading column and composer feel more ChatGPT-like in readability, not just cosmetically different
- gray inline emphasis and proper code/script block treatment are clearly present
- selected dialog left-side shadow/treatment no longer feels cheap and is visibly changed
- yellow logo is gone and replaced by monochrome-compatible mark
- tool rows are grouped/collapsible and stop dominating the screen
- tool icons are differentiated by type
- old dialog freeze is fixed or materially mitigated
- speed/performance remains excellent

## Deliverable expected from Forge
Return:
1. short plan
2. exact files changed
3. explicit mapping from implementation to:
   - `hermes_typography_tz.md`
   - `hermes_quick_wins.md`
   - selected-dialog-shadow complaint
4. freeze root cause or mitigation note
5. deferred items
6. quick verification notes
