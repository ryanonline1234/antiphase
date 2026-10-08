# 00 · Concept

**One line.** A stealth heist where every sound is a real wave solved through the
building, and you hide your loudest moment by adding a second sound so that, at the
guard's ear only, the two cancel into silence.

**Player fantasy.** A thief who can see sound and makes silence out of more of it.

## 1. The verb

Stealth games have always treated noise as a one-way cost. In *Mark of the Ninja* a
footstep draws a ring; if it touches a guard, he hears you. In *Thief* sound travels a
graph of rooms. In both, adding noise can only hurt you. Antiphase's one new verb is
**destructive interference**: two steady tones at the same frequency add up, and where
they arrive half a cycle apart they cancel. Put the cancellation on the guard and you are
inaudible while your drill is still screaming.

The physics that makes it a skill rather than a button:

- **The null is a curve, not a wedge.** Two sources make a family of curves where their
  waves are in antiphase. In a room with walls, reflections bend and break those curves.
  You are not aiming a cone; you are steering a thin dark line.
- **Silence means "under his threshold", not zero.** Levels keep the drill only 3–6 dB
  above what a guard notices along his route, so the usable band is wider than the true
  zero. Estimated -6 dB half-width is about 0.08 λ, so with λ = 3–6 m (slowed sound,
  see §6) the band is roughly 0.6–0.9 m: one body width. **Unmeasured. The kill test
  (§9) exists to measure it.**
- **Mount points are far from the sources.** An emitter placed right beside the drill in
  antiphase would cancel it everywhere, and that would be the only strategy. Mounts sit at
  least 1.5 λ from any loud source, so cancellation is always local and placement is a
  real choice.
- **The field lags you.** Sound crosses the room and the guard's hearing averages over
  about half a second, so the band follows your wheel with a 0.3–0.8 s delay. A dashed
  **ghost contour** shows where the band will settle, and you lead a walking guard the way
  you'd lead a shot.

What this is **not**: a reflex game where you answer each footstep with an inverted pulse
within a second. Four independent judges of the original pitch all made the same
correction: pulse cancellation only works at long range, echoes leak, and once it's
assisted enough to be playable it collapses to "stand him on the halfway line". So the
core verb is shaping the **steady** field around a **continuous** tone. Footstep pulses
remain as the ordinary stealth layer. The pulse counter-thumper is a late gadget at most.

## 2. A minute of play

1. **Scout.** Toggle the sound x-ray. The floor shows the live pressure field, red for
   positive, blue for negative. Each guard wears an ear ring that fills orange as he hears
   more.
2. **Plan.** Pick a mount point for your counter-emitter and a gain step (Low / Med /
   High). Open or close doors; each door changes which room modes exist.
3. **Start the job.** Drill the vault, cut the case, spin up the server rack. It emits a
   steady tone for 20–60 s and throws standing fringes across the galleries.
4. **Steer.** The mouse wheel turns the emitter's phase. The ghost contour moves first,
   the black band follows and settles. You keep it on the guard as he walks.
5. **Move.** Cancelling the drill at his ear also removes the masking that hid your
   footsteps. Walk while the job is off, or use a machine hum as cover. That tension is
   the point.

## 3. A session

8–15 minutes. One building of 3–5 connected rooms. Each room is a set piece with one loud
job; then the objective and the exit. Every set piece is scored like *Opus Magnum*:
emitters used, total phase travel ("wheel travel", less is more elegant), and time,
compared with a par. If you are caught, a 10-second replay of the wave field shows the
exact fringe that reached the guard.

## 4. The ladder (MVP: 7 hand-written levels, one museum floor)

| # | Teaches | New constraint |
|---|---|---|
| 1 | A still guard | Find any phase that puts the band on him |
| 2 | A walking guard | Track and lead |
| 3 | A door | Opening it retunes the room; the band jumps |
| 4 | Two guards, one emitter | Placement: one setting must cover both |
| 5 | Two emitters | Two wheels, two bands |
| 6 | Hum masking | Raise his threshold instead of cancelling |
| 7 | Hero level | Cancelling unmasks your own footsteps |

Post-MVP depth, only if play proves the verb: a two-harmonic drill (two constraints per
point), higher-pitched tools with narrower bands, tunable resonators, three buildings
(museum, data hall, embassy), about 20 levels.

## 5. What it looks like

Near-black. Thin white line-art cutaway of the floor, seen from a steep orthographic
angle. The interference fringes **are** the art: signed pressure as red and blue with soft
bloom, the silence band as true black with a thin pale contour, the ghost contour dashed.
Guards and the player are capsule figures with a faint vision fan and an ear ring. Walls,
props and figures are all generated in code. Palette and references live in
[01-inspiration.md](01-inspiration.md).

## 6. What it sounds like

Sound in this world travels at **one tenth real speed (34.3 m/s)**. It is a stated rule
of the fiction, so you can watch your own footstep's ripple leave you. Everything the
player hears is a synthesized voice (drill = sawtooth + band-passed noise, hum = detuned
oscillators, footsteps = noise burst + low thump) whose loudness is driven by the
simulated amplitude at the listener. The drill's audible pitch (110–220 Hz) is
deliberately not its simulated frequency (6–11 Hz). Hold **Q** over a guard to switch the
listener to his ears: you hear your silence land.

## 7. Fairness rules

1. A guard hears exactly the field that is drawn. One live field on the GPU is the single
   source of truth. The ghost is prediction only; guards never hear it.
2. Physics resolution and step rate are identical on every machine. A slow machine gets
   time dilation, never coarser physics, so outcomes match everywhere.
3. Guard perception reads the field at a fixed step delay, so his behaviour is a pure
   function of the field, not of frame timing.
4. The ear ring and ear-tap audio show his exact input. The caught-replay shows the
   fringe that got you.

## 8. Cut from the MVP

Multi-floor coupling through stairwells and vents, the procedural building generator
(levels are hand-written), the gadget kit and meta-progression, tunable resonators, the
reactive pulse counter-thumper, two-harmonic tools, full-heist replay, a WebGL2 fallback,
phones.

## 9. Kill test (before any real game code)

A throwaway NumPy wave sim of a two-room level with one drill and one mount, measuring:

- **-6 dB silence-band width** at the guard as λ (3–6 m) and wall damping vary.
- **How steadily the band moves** as phase turns.
- **Pass:** a band ≥ 0.5 m wide over ≥ 4 m of the patrol at one phase setting, moving
  smoothly with phase. **Fail:** retune damping, λ, or threshold margin before continuing.

The mood-board render in `docs/inspiration/render_fringes.py` is a crude first version of
this test; its numbers are in [01-inspiration.md](01-inspiration.md). It is Claude's code
and is not the kill test of record. Ryan's own version should reproduce it.

## 10. Risks

| Risk | Mitigation |
|---|---|
| The band is too thin, jittery or laggy in echoey rooms; steering feels like pixel-hunting | Kill test with explicit pass numbers. Longer λ, more wall damping, smaller threshold margin, slower guards (0.8 m/s). The ghost contour removes lag guesswork. Last resort: a 1 s grace on the ear meter. |
| The verb collapses to one trick or reads as fiddly | Moving guards, several guards per emitter, doors retuning modes, masking vs unmasking. Playtest stop rule: if more than 3 of 5 players say "fiddly", snap the wheel to 15° steps before adding content. |
| It reads as "a ripple-tank applet with a stealth HUD" | The hero clip is built around the one thing only this game does: a band of silence visibly following a walking guard while his ear-tap goes quiet. Line art, bloom and guards whose footsteps ripple make it a place, not a sim. |

## 11. Terra fit: 12 weekly ships

Terra wants about 10 hours a week of Ryan's own coding, with something shipped each week,
from Oct 19 2026 to Jan 10 2027. The architecture brief this came from assumed a
different builder and a 4-week sprint; this is a re-cut into twelve ships. **Draft:** it
moves once the stack is chosen (see §12).

| Week | Starts | Ship |
|---|---|---|
| 1 | Oct 19 | Wave sim on a typed array, red/blue canvas render, one pulse source, rigid walls. A ripple toy you can click. |
| 2 | Oct 26 | Steady tone, per-cell amplitude (lock-in), threshold → black silence map. A doorway that diffracts. |
| 3 | Nov 2 | Second emitter, phase wheel, gain steps. Reference channels → ghost contour. Measure the band; compare with the kill test. |
| 4 | Nov 9 | Player movement, footstep pulses by floor material (carpet, marble). |
| 5 | Nov 16 | Guard: ear probe, intensity-vector heading, state machine (patrol → suspicious → investigate → alert), vision fan. |
| 6 | Nov 23 | Level format + rasteriser (one source of truth for walls). Levels 1–3. |
| 7 | Nov 30 | Audio synth voices driven by the field. Ear-tap on Q. |
| 8 | Dec 7 | Levels 4–7. Scoring vs hand-set pars. |
| 9 | Dec 14 | Line-art cutaway, bloom, HUD typography. Move the render to shaders if the canvas can't hold 60 fps. |
| 10 | Dec 21 | Caught-replay, menu, progress in localStorage, WebGPU/WebGL detect page. |
| 11 | Dec 28 | Playtest with 5 people, tuning rig, snap-dial decision. |
| 12 | Jan 4 | Hero level polish, 15 s clip, ship to Vercel. |

## 12. Open decisions

1. **Stack.** Options: (a) TypeScript + Canvas2D with the wave sim on the CPU in typed
   arrays, moving to shaders only if needed; (b) WebGL2 fragment-shader ping-pong sim;
   (c) WebGPU compute via three.js TSL, as the original brief proposed.
   Recommendation: **(a)**. At 320×240 cells × 8 substeps × 60 fps the CPU does about
   37 M cell updates a second, which a tight typed-array loop handles. It is the most
   readable, debuggable path for code Ryan writes himself, and it leaves GPU work as a
   week-9 upgrade rather than a week-1 wall. Unverified: the exact CPU headroom once
   lock-in channels are added; week 1 measures it.
2. **View.** Top-down 2D for the MVP, or the orthographic cutaway from the start?
   Recommendation: top-down through week 8, cutaway in week 9. The verb is identical.
3. **Grid.** 0.1 m cells on a 32 × 24 m floor, as the brief. Recommendation: keep.

## Provenance

Concept, judges' corrections and architecture brief: game-ideation batch 2, 2026-09-23
(session report, not in this repo). Adopted for Hack Club Terra 2026-10-07. Prior art
checked then: *Destructive Interference* (LÖVE Jam 2022), *A.N.C.* (TUM jam 2022), *IT
REALLY HERTZ* (MelonJam 2025) all touch cancellation as a toy or reflex; none aims a
steady null at a listening AI in a room. A 2026-10-07 search found no shipped game named
Antiphase (one standard search, not exhaustive).
