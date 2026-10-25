# PLAN: front-page hero

## Grammar: Broadsheet plate (new)

The hero is one plate set into an existing newspaper front page. Why the eight
defined grammars lost:

| Grammar | Why not |
|---|---|
| Filmic one-shot | A flythrough of acts; this is one plate inside a document |
| Chaptered editorial | Closest, but its hero must be a title page with no media above the fold, and the brief needs the portrait and charts there |
| Live surface | No tool or input is the product here |
| Continuous world | No world to fly through; the subject is a person and his figures |
| Typographic poster | The owner asked for more images, not fewer |
| Gallery / catalog | The project index already does this job below the fold |
| Split stage | No two-sided argument |
| Rhythmic cutlist | Fast cuts are the opposite of "rigorous" |

What makes it a different structure, not a relabel: the chrome is the
pre-existing masthead (not owned by the hero), the hero is a single pinned plate
with four depth planes whose layout is a newspaper column grid, and the ending is
a hand-over into ordinary document flow rather than a close or a CTA.

## Planes (back to front)

| Plane | Content | Motion |
|---|---|---|
| Atmosphere | Column hairlines of the page grid | `data-sc-parallax="-1.2"`, recedes |
| Archive | Three chart clippings (Banking, Churn, Emigration figures, from `tools/figures.py`) stacked behind the portrait | Bespoke: fan out up and outward with `--sc-p`, about 70px each |
| Type | Kicker, `<h1>`, deck | 1x (no transform), never parallaxed |
| Subject | Portrait cutout (alpha) standing on its own rule | `data-sc-parallax="-0.45"`; rule moves with it so the contact point holds |
| Foreground | CARP chart plate with the live ledger, overlapping the portrait's shoulder | `data-sc-parallax="0.9"`, rises faster than the page, occludes the subject |

Phone: type on top, portrait centred and smaller, chart plate full width below,
one clipping instead of three, no overlap of the headline.

Reduced motion: no pin and no added scroll length; every plane in its final
position, chart fully drawn, ledger at the final average.

## Score

One act. Device families used: `pin`, `parallax`, `cue`, plus the bespoke
signature (stroke drawing and ledger). The four-family rule is satisfied inside
the act; there is no second act to alternate with.

| Beat | Device | Why this one |
|---|---|---|
| Recognition | `pin` + greet cues | The plate holds still; the headline is on screen on landing |
| Curiosity | bespoke fan-out on the archive plane, `parallax` | Small differential motion reads as depth before it reads as motion |
| Conviction (peak) | signature: chart draws from `--sc-p`, ledger ticks | The work proves itself with the real series |
| Settled | final cue holds; plate rests on a double rule | Resolves into the document instead of fading |

Span 2.6 viewport-heights; peak owns progress 0.10 to 0.86 (76% of the act). The clippings fan out over 0 to 0.30, alongside the start of the pen, so no stretch of the act is still.

## Signature move

**The proof draws itself with a running ledger.** The real 1970 to 2008 labor
productivity series for the Philippines and its synthetic control are inline SVG
paths whose `stroke-dashoffset` follows `--sc-p`. After 1988 the gap between the
lines fills with hatching as the pen passes, and a tabular-numeral ledger under
the chart reads the year at the pen, both values, and that year's real gap. It
lands on the study's published average, minus 18.2 percent.

## Fingerprint gate

`_scrollcraft/FINGERPRINTS.md` is empty: this is the first build in this
workspace, so there is no row to clear. Row appended after approval.
