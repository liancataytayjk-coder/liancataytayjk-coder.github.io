# PLAN: front-page hero

## Grammar: Broadsheet plate (new)

The hero is one plate set into an existing newspaper front page. Why the eight
defined grammars lost:

| Grammar | Why not |
|---|---|
| Filmic one-shot | A flythrough of acts; this is one plate inside a document |
| Chaptered editorial | Closest, but its hero must be a title page with no media above the fold, and the brief needs the portrait and charts there |
| Live surface | No tool or input is the product here |
| Continuous world | No world to fly through; the subject is a person and their method |
| Typographic poster | The owner asked for more images, not fewer |
| Gallery / catalog | The project index already does this job below the fold |
| Split stage | No two-sided argument |
| Rhythmic cutlist | Fast cuts are the opposite of "rigorous" |

What makes it a different structure, not a relabel: the chrome is the
pre-existing masthead (not owned by the hero), the hero is a single pinned plate
with three depth planes whose layout is a newspaper column grid, and the ending is
a hand-over into ordinary document flow rather than a close or a CTA.

## Planes (back to front)

| Plane | Content | Motion |
|---|---|---|
| Atmosphere | Column hairlines of the page grid | `data-sc-parallax="0.3"`, a slow drift |
| Type | Kicker, `<h1>`, deck | Still; greets with a cue |
| Subject | Portrait cutout (alpha) in its own right-hand grid column, standing on the plate's double rule | Still; it is the anchor |
| Foreground | "How I work, in three figures": one strip of three equal panels (pattern, counterfactual, decision), geometry from `assets/hero/story.json` | Set directly under the deck in the left column; each panel draws with a clip-rect pen |

Layout is a two-column grid (left: type, then the strip; right: portrait), so
no layer can overlap another. Phone and tablet: one column, headline, then the
portrait standing on the strip's top rule, then the strip with titles only.

Reduced motion: no pin and no added scroll length; every plane in its final
position, all three figures complete.

## Score

One act. Device families used: `pin`, `parallax`, `cue`, plus the bespoke
signature (three figures drawn in sequence). The four-family rule is satisfied inside
the act; there is no second act to alternate with.

| Beat | Device | Why this one |
|---|---|---|
| Recognition | `pin` + greet cues | The plate holds still; the headline is on screen on landing |
| Curiosity | figure 1 draws | A scatter finds its line |
| Conviction (peak) | signature: figures 2 and 3 draw from `--sc-p` | The method tells its own story |
| Settled | final cue holds; plate rests on a double rule | Resolves into the document instead of fading |

Span 2.6 viewport-heights; the three figures own 0.06 to 0.32, 0.34 to 0.60 and 0.62 to 0.88, so no stretch of the act is still.

## Signature move

**The method draws itself in three figures.** Each panel is inline SVG clipped by
a rectangle (the pen) whose width follows `--sc-p`: first a scatter and its fit
line ("Find the pattern"), then an actual path leaving the expected one after a
policy line, the gap shaded ("Measure the effect"), then bars rising
past a threshold ("Decide where to act"). The figures are labelled as schematic;
real data stays on the project pages.

## Fingerprint gate

`_scrollcraft/FINGERPRINTS.md` is empty: this is the first build in this
workspace, so there is no row to clear. Row appended after approval.
