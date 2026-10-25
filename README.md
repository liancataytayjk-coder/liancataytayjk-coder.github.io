# Lian Cataytay Portfolio

A personal portfolio website for Lian Cataytay, Data Analyst & Economist, designed as a classic
broadsheet: Times New Roman throughout, a newspaper masthead, a multi-column front page, and
article-style project pages.

## Live Site

https://liancataytayjk-coder.github.io/

## Structure

```text
index.html
about.html
projects.html
contact.html
portfolio.html
404.html
sitemap.xml
robots.txt
assets/
  styles.css
  portfolio.css
  script.js
  logo.svg                # LC monogram seal (logo-512.png is a raster copy)
  favicon.svg             # simplified seal for browser tabs
  favicon-64.png
  apple-touch-icon.png
  og-image.jpg            # 1200x630 link-preview image
  hero/                   # front-page hero layers (portrait cutout, schematic geometry)
  scrollcraft/            # scroll-craft runtime used by the hero
  hero.js                 # draws the hero's three figures on scroll
  about-night-sky.jpg
  portfolio.pdf
  lian-cataytay-resume.pdf
projects/
  customer-sentiment-intelligence-dashboard.html
  ecommerce-customer-retention-analytics.html
  ai-customer-churn-intelligence-system.html
  agricultural-scm-productivity-analysis.html
  philippines-labor-market-trend-analysis.html
  media-audience-engagement-analysis.html
  philippine-emigration-ardl-macroeconomic-analysis.html
  banking-risk-and-financial-performance-analysis.html
  employee-attrition-risk-and-workforce-intelligence-analysis.html
  ecommerce-marketplace-ads-performance-dashboard.html
  fpa-revenue-cost-expense-forecasting-dashboard.html
  crm-event-marketing-data-hygiene-system.html
```

## Figures

Every chart in `assets/figures/` is drawn from the project repositories' own data in black and
white (Times New Roman, line styles and grey fills, no colour). `assets/figures/figures.json` holds
each figure's caption and source note. To redraw them, clone the project repositories into one
folder and run:

```text
pip install matplotlib pandas openpyxl
python3 tools/figures.py <folder-with-project-repos> .
```

## Front-page hero

The top of `index.html` is a scroll-driven plate built with the scroll-craft skill. As
the reader scrolls, three small figures draw themselves in turn: find the pattern, measure
the effect, decide where to act. They are schematic illustrations of the
method, not data; the project pages carry the real figures. Under reduced motion the
plate is static and complete.

- Engine: `assets/scrollcraft/` (unmodified scroll-craft runtime); page code: `assets/hero.js`.
- Layers: `assets/hero/`. `story.json` (the figures' geometry) comes from `tools/figures.py`;
  the portrait cutout comes from `python3 tools/hero_portrait.py <headshot> assets/hero 22` (the last number trims a desk edge off the bottom).
- Planning, brief and verification: `_scrollcraft/` (set in `.scrollcraft.json`). Jekyll
  skips underscore folders, so GitHub Pages does not publish it.

## Updating the portfolio PDF

`assets/portfolio.pdf` is printed from `portfolio.html`. After editing it, serve the folder locally
and print the page to A4 PDF with background graphics enabled (Chrome: Print > Save as PDF, margins None).

## How to Run Locally

Open `index.html` directly in a browser.

## How to Deploy with GitHub Pages

1. Push all files to the main branch.
2. Open the GitHub repository.
3. Go to Settings.
4. Go to Pages.
5. Under Build and deployment, choose Deploy from a branch.
6. Select main branch.
7. Select root folder.
8. Save.
9. Wait for the site to publish.

## Notes

This website uses only HTML, CSS, and JavaScript.
No build step is required.

The contact form opens a prefilled Gmail compose window so the site can stay fully static on GitHub Pages.
