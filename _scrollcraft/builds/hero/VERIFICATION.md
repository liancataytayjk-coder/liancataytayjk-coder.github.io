# VERIFICATION: front-page hero

Checked on 2026-10-25 against a local server of the repository.

## Harness (scroll-craft `shoot.mjs`)

| Run | Dead scroll | Contrast |
|---|---|---|
| Desktop 1440x900 | none | all cues clear 4.5:1 |
| Phone 390x844 | none | all cues clear 4.5:1 |
| Reduced motion | none | all cues clear 4.5:1 |

The signature move runs outside the engine, so the plate publishes
`data-sc-verify-state` (pen position, ledger year, fan). Without it the harness
reported the whole act as dead scroll, which it was not.

Contact sheets: `lab/sheet-desktop.png`, `lab/sheet-phone.png`,
`lab/sheet-reduced.png`. Stills shown to the owner: `lab/hero-*.png`.

## Manual checks

- Overlap of any layer with the headline or deck, sampled at five positions
  through the act: 0px at 1440x900, 1366x768, 1280x720, 1920x1080, 820x1180,
  390x844, 375x667 and 430x932. No horizontal overflow at any size.
- Ledger values at the pen match `assets/hero/carp-labor.json`; the closing
  average (-18.2%) matches the study's -18.19%.
- Reduced motion: engine not mounted, no pinned scroll, chart complete, ledger
  at the average.
- All 17 pages at 1366 and 390 wide: no overflow, every image loads, no JS
  errors or failed requests.

## Feel check (cold)

| Act stage | Intended | Felt |
|---|---|---|
| Open | Recognition | Recognition |
| Early | Curiosity (clippings fan) | Anticipation (empty axes waiting) |
| Middle | Conviction | Conviction |
| End | Settled | Settled |

The fan is too small to register as its own beat; the empty chart carries the
anticipation instead. Kept as is, since the brief asked for restraint.

## Not verified

- A real phone (iOS Safari, Android Chrome). Headless Chromium cannot reproduce
  touch scrolling or a device's rendering of sticky positioning.
- GitHub Pages excluding `_scrollcraft/`: it relies on Jekyll skipping
  underscore folders; confirm after merge that `/_scrollcraft/` returns 404.
