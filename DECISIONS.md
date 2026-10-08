# Decisions

Append-only. Newest at the bottom. Each entry: what, why, and what it rules out.

## 2026-10-07 — Antiphase is the Hack Club Terra project

Chosen over Catenary (buildability 4, no slack at 10 h/week), Foley+morph (magic lives in
a third-party audio model), and AP Calc interactives (crowded). Antiphase scored
buildability 7 in the September ideation, has a novel verb, and decomposes into weekly
ships naturally (sim → silence map → emitter → player → guard → levels).

## 2026-10-07 — Core verb is steady-field shaping, not pulse cancellation

All four judges of the original pitch independently rejected "answer each footstep with
an inverted pulse": only works at long range, echoes leak, and assisted versions collapse
to one trick. The drill is a continuous tone; the player steers a persistent silence band.
Rules out the reactive counter-thumper as a core mechanic (late gadget at most).

## 2026-10-07 — Ryan writes the game code; Claude is tutor, reviewer and doc drafter

Terra's water comes from Hackatime hours of Ryan's own coding, and Terra's AI-code rule is
unverified (sibling program 3am bans AI-generated work). Claude-written scripts that do
land in the repo (the mood-board render) are labelled as design tools, not game code.
Revisit if #terra-help gives a clear ruling.

## 2026-10-07 — Public GitHub repo from day one

Hack Club builds in public; the repo holds design docs and nothing sensitive. Flip with
`gh repo edit --visibility private` if that changes.

## 2026-10-07 — Stack: OPEN

See docs/00-concept.md §12. Recommendation on the table is TypeScript + Canvas2D with a
CPU typed-array sim, GPU later if needed.
