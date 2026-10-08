# State — Antiphase
_Updated: 2026-10-07_

## Now

Design phase. No game code. Repo scaffolded with the concept, the inspiration doc and
code-rendered mood-board studies. Hack Club Terra: prep weeks until Oct 18; required
weeks Oct 19 2026 – Jan 10 2027 at 10 Hackatime hours a week.

## Verified

- `docs/inspiration/render_fringes.py` runs clean under `uv run --with numpy --with pillow`
  and writes `before.png`, `after.png`, `phase-sweep.gif` (5.0 MB). Measured numbers are
  in `docs/01-inspiration.md`: band 1.4 m wide, wheel reach 5 m of a 9.6 m patrol.
- No shipped game named Antiphase found (one standard web search, 2026-10-07).

## Pending

1. Ryan decides `docs/00-concept.md` §12: stack (rec: TypeScript + Canvas2D, CPU sim),
   view (rec: top-down until week 9), grid (rec: 0.1 m).
2. Ask #terra-help how AI-assisted code is treated; record the ruling in `DECISIONS.md`.
3. Install Hackatime before Oct 10 so prep hours count.
4. Kill test (`00-concept.md` §9) in Ryan's own code, compared with the render's numbers.
5. Shrink `phase-sweep.gif` if 5 MB bothers anyone cloning the repo.

## Pending spec patches

None.
