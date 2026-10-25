# VERIFICATION: front-page hero

Checked on 2026-10-25 against a local server of the repository.

## Harness (scroll-craft `shoot.mjs`)

| Run | Dead scroll | Contrast |
|---|---|---|
| Desktop 1440x900 | none | all cues clear 4.5:1 |
| Phone 390x844 | none | all cues clear 4.5:1 |
| Reduced motion | none | all cues clear 4.5:1 |

The signature move runs outside the engine, so the plate publishes
`data-sc-verify-state` (how far each of the three figures is drawn). Without it the harness
reported the whole act as dead scroll, which it was not.

Contact sheets: `lab/sheet-desktop.png`, `lab/sheet-phone.png`,
`lab/sheet-reduced.png`. Stills shown to the owner: `lab/hero-*.png`.

## Manual checks

- Overlap of any layer with the headline or deck, sampled at five positions
  through the act: 0px at 1440x900, 1366x768, 1280x720, 1920x1080, 820x1180,
  390x844, 375x667 and 430x932. No horizontal overflow at any size.
- The figures draw in order: at progress 0.75 the state reads
  `1.000|1.000|0.499`, and all three are complete by 0.88.
- Reduced motion: engine not mounted, no pinned scroll, all three figures
  complete.
- All 17 pages at 1366 and 390 wide: no overflow, every image loads, no JS
  errors or failed requests.

## Feel check (cold)

| Act stage | Intended | Felt |
|---|---|---|
| Open | Recognition | Recognition |
| Early | Curiosity (first figure draws) | Curiosity |
| Middle | Conviction (the gap opens) | Conviction |
| End | Settled (bars cross the line) | Settled |

Revision after owner feedback: the scattered chart clippings read as untidy,
so they were replaced by one aligned strip of three equal panels.

## Not verified

- A real phone (iOS Safari, Android Chrome). Headless Chromium cannot reproduce
  touch scrolling or a device's rendering of sticky positioning.
- GitHub Pages excluding `_scrollcraft/`: it relies on Jekyll skipping
  underscore folders; confirm after merge that `/_scrollcraft/` returns 404.
