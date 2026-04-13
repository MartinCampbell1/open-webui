# ee465f replay UI remediation brief

Date: 2026-04-12
Target repo: `/Users/martin/open-webui-replay-ee465f`
Live target: `http://127.0.0.1:18081/c/d2bca9e1-e612-44a7-a5a2-bd53af53819d`
Current process: `open-webui dev --host 127.0.0.1 --port 18081 --no-reload`
Base commit: `ee465f16519c352321bebdcdcd9d3698cf393392`

## Context

This is NOT a redesign.
This IS a bounded remediation pass on the ee465f replay tree.

Preserve:
- Open WebUI visual identity and shell calmness
- improved transcript typography that the user explicitly liked
- workspace improvements that are now finally in a good place

Do NOT:
- restart the architecture
- introduce a new visual system
- turn the UI into a dashboard
- “improve” by adding more chrome/cards/pills everywhere
- regress layout stability in sidebar/right panel/session flow

## Grounding sources

Read first:
- `/Users/martin/open-webui-replay-ee465f/AGENTS.md`
- `/Users/martin/open-webui/HANDOFF_HERMES_UI_2026-04-11_CONTEXT.md`
- `/Users/martin/open-webui/handoff.md`

User feedback source of truth:
- latest explicit user feedback in Hermes transcript, summarized below
- screenshots provided by user:
  - `/Users/martin/Desktop/Снимок экрана — 2026-04-12 в 21.58.18.png`
  - `/Users/martin/Desktop/Снимок экрана — 2026-04-12 в 21.59.30.png`
  - `/Users/martin/Desktop/Снимок экрана — 2026-04-12 в 21.59.46.png`
  - `/Users/martin/Desktop/Снимок экрана — 2026-04-12 в 22.00.03.png`
  - `/Users/martin/Desktop/Снимок экрана — 2026-04-12 в 22.00.36.png`
  - `/Users/martin/Desktop/Снимок экрана — 2026-04-12 в 22.00.56.png`
  - `/Users/martin/Desktop/Снимок экрана — 2026-04-12 в 22.01.56.png`
  - `/Users/martin/Desktop/Снимок экрана — 2026-04-12 в 22.02.54.png`
  - `/Users/martin/Desktop/Снимок экрана — 2026-04-12 в 22.03.58.png`
  - `/Users/martin/Desktop/Снимок экрана — 2026-04-12 в 22.04.39.png`
  - `/Users/martin/Desktop/Снимок экрана — 2026-04-12 в 22.06.44.png`
  - `/Users/martin/Desktop/Снимок экрана — 2026-04-12 в 22.07.07.png`

## User feedback distilled into fixable tasks

### P0 — polish regressions the user clearly dislikes

1. Left sidebar archive area still feels generic/cheap
- `Архив Hermes` region and the block below it look too generic
- active/current dialog selection state on the left feels cheap
- selection affordance should be calmer and more premium, not loud but not flimsy
- do a UX pass specifically on archive/list row hierarchy, hover, active state, metadata density, divider rhythm

2. Active dialog row selection looks cheap
- current selected conversation row outline/highlight feels low quality
- replace the “cheap” outlined/boxed feeling with a more polished Open WebUI-native active state
- the result should feel restrained, not flashy, and clearly selected

3. User message row “привет” looks too thick/heavy
- the user liked the transcript typography overall
- but simple user messages currently look too bold/heavy/large
- reduce weight/visual thickness so user rows feel calmer and more integrated with the transcript hierarchy

4. Tool call surfaces still look messy/unclean
- tool calls / tool activity / operational rows still look dirty and unrefined
- improve spacing, hierarchy, iconography, borders/backgrounds, and expansion affordances
- keep them compact and operational, not dashboard cards

5. Agent icon is wrong for the black-and-white theme
- current agent icon/logo style does not fit the monochrome aesthetic
- user wants something calmer and more black/white-compatible
- avoid colorful or off-brand icon treatment

### P1 — discoverability and semantics problems

6. “Active tasks” panel is semantically unclear
- user does not understand what active tasks are
- where they come from
- what their provenance is
- the UI needs better labeling/explanatory copy/status/source semantics
- if the surface is currently fake/empty/placeholder-ish, make that explicit rather than pretending it is a complete product surface

7. Model switching / key management discoverability is poor
- user cannot tell where to change model
- user cannot tell where to add a key/provider/model for speech/Whisper etc.
- audit current navigation/settings surface and make the path discoverable
- if full model/key editing is not implemented in this shell, say so clearly in the UI and route the user to the correct place instead of leaving ambiguity

8. Archive semantics are unclear
- user asks whether archive is global or chat-specific
- whether archived items can be re-added/imported back into chats
- whether archived dialogs can be continued from here
- UI copy and actions should clarify this

9. Workspace/file preview behavior still has a bad state
- user reports that when opening files they can get truncated/oddly cropped content
- inspect workspace/file preview area for clipping/truncation bug or bad container sizing/overflow behavior

10. Empty/placeholder panels need semantic honesty
- `Memories: 0`, checklist, overview/graph, active tasks, etc. feel unclear or fake
- improve empty states and explanatory copy
- make it clear what is implemented, what is derived, what is placeholder, and how users add/use each thing

### P2 — visual refinement with bounded external inspiration

11. Skills surface needs a redesign using 21st.dev as bounded component inspiration
- current compact skills look generic and not neat
- older version used too much space; current version uses less space but looks sloppy
- use 21st.dev for bounded inspiration only (not full-page replacement)
- add per-skill iconography by category/type where possible
  - search/web -> magnifier
  - memory -> memory/bookmark/brain-like icon
  - tasks -> checklist icon
  - etc.
- keep the result compact, tidy, and Open WebUI-compatible

12. Language/settings controls have awkward emphasis
- some controls (e.g. language selector) visually “stick out” too much
- calm the emphasis and align with overall settings UI hierarchy

13. Overview/graph may be more trouble than value
- user finds it visually interesting but semantically unclear
- it takes horizontal space and may cause performance issues/hangs
- audit whether it should be deprioritized, collapsed, hidden behind disclosure, or made materially more useful

## Expected execution style

1. First inspect affected components and screenshot evidence.
2. Produce a short implementation plan grouped by:
- P0 fixes now
- P1 semantic/discoverability fixes now if cheap
- P2 deferred or partial
3. Implement a cohesive first remediation slice, not a random scattershot rewrite.
4. Keep all changes bounded and reversible.

## Strong suggestion for first remediation slice

A good first execution slice is:
- left sidebar archive/list/active row polish
- reduce user message heaviness
- tool activity row cleanup
- agent icon cleanup for monochrome theme
- improve active tasks/archive explanatory copy if cheap in same pass

## Acceptance criteria

The pass is successful only if:
- left sidebar feels calmer and less generic
- active row no longer looks cheap
- user messages are less visually thick while keeping good readability
- tool activity looks cleaner and more intentional
- skills surface direction is clearly improved or a bounded follow-up plan is left
- users can understand where model/key-related configuration lives, or the UI clearly states current limitation
- empty panels stop pretending and instead explain themselves honestly
- no regressions in workspace, session import/open, sidebar restore, or right panel stability

## Constraints

- Limited RAM machine: avoid heavy parallel builds/tests
- Prefer narrow verification
- Do not run broad project-wide checks unless needed
- Preserve Open WebUI identity
- 21st.dev is allowed only for specific new micro-surfaces, especially the skills row/card treatment

## Deliverable expected from Forge

Return:
1. a short remediation plan
2. exact files changed
3. concise summary of what was implemented
4. any items intentionally deferred
5. quick verification notes
