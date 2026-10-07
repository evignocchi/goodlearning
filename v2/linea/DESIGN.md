---
name: Goodlearning Landing v2, La linea unica
description: A metro map. Many grey routes merge into one thick blue line that becomes the spine of the page and ends at the contact terminus.
colors:
  white: "#ffffff"
  soft: "#f5f7fb"
  ink: "#0a1230"
  ink-soft: "#47526e"
  line-blue: "#0a4fd6"
  gold: "#f0c010"
  route: "#c3cadb"
  track: "#e3e8f3"
  hairline: "#e1e6f0"
typography:
  display:
    fontFamily: "Host Grotesk, Helvetica Neue, Arial, sans-serif"
    fontSize: "clamp(2.75rem, 5.3vw, 4.875rem)"
    fontWeight: 800
    lineHeight: 0.97
    letterSpacing: "-0.04em"
  headline:
    fontFamily: "Host Grotesk, Helvetica Neue, Arial, sans-serif"
    fontSize: "clamp(2.125rem, 4.8vw, 4.25rem)"
    fontWeight: 800
    lineHeight: 0.98
    letterSpacing: "-0.035em"
  title:
    fontFamily: "Host Grotesk, Helvetica Neue, Arial, sans-serif"
    fontSize: "1.5rem"
    fontWeight: 700
    lineHeight: 1.1
  body:
    fontFamily: "Host Grotesk, Helvetica Neue, Arial, sans-serif"
    fontSize: "1.0625rem"
    fontWeight: 400
    lineHeight: 1.62
  label:
    fontFamily: "Host Grotesk, Helvetica Neue, Arial, sans-serif"
    fontSize: "0.8125rem"
    fontWeight: 700
    lineHeight: 1.4
rounded:
  field: "8px"
  button: "10px"
  card: "12px"
spacing:
  sm: "16px"
  md: "24px"
  lg: "48px"
  xl: "96px"
components:
  button-blue:
    backgroundColor: "{colors.line-blue}"
    textColor: "#ffffff"
    rounded: "{rounded.button}"
    padding: "0 24px"
    height: "52px"
  button-blue-hover:
    backgroundColor: "{colors.ink}"
  field:
    backgroundColor: "{colors.white}"
    textColor: "{colors.ink}"
    rounded: "{rounded.field}"
    padding: "0 14px"
    height: "48px"
  tray:
    backgroundColor: "{colors.white}"
    textColor: "{colors.ink}"
    rounded: "{rounded.card}"
    padding: "18px"
---

# Design System: Goodlearning Landing v2, La linea unica

## Overview

**Creative North Star: "The Single Line"**

A metro map where the story is the number of lines. At the top many thin grey routes (the old processes) run in from the left edge, bend at 45 degrees and merge into one thick blue line. That line runs through four stations (document, GoodContent AI, course, register) and ends at a bullseye terminus where the contact form hangs. Below the hero the same blue line becomes the spine on the left of the page: every section is a station that turns from grey to blue as the line reaches it, the audiences section splits it into two parallel tracks (blue and gold), and the page finishes at a terminus where the line ends.

The page gets simpler as it goes: eight routes at the top, two tracks in the middle, one line at the end. White ground, one blue, one gold, black ink, nothing else shouts.

**Key Characteristics:**
- One thick line (14px) is the whole identity; routes are 3px grey.
- Stations are white discs with a thick ring: grey until reached, then blue (gold for AI).
- Flat: no shadows, hairline borders only.
- Wide, tight, heavy grotesque headlines.
- Real screenshot and real numbers; sketches are labelled illustrative.

## Colors

White ground, ink, a single blue line, a gold branch, and grey routes.

### Primary
- **Line Blue** (#0a4fd6): the trunk and spine, reached stations, primary buttons, the number highlights, the terminus. White on it is 6.4:1.

### Secondary
- **Goodlearning Gold** (#f0c010): the AI modules' stations, the second track for training bodies, the ring around the terminus, text-link underlines. The same yellow as the AI logos. Text on it is always Ink.

### Neutral
- **White** (#ffffff) ground; **Soft** (#f5f7fb) for tinted UI; **Ink** (#0a1230) text, headlines, footer; **Ink Soft** (#47526e) secondary text.
- **Route Grey** (#c3cadb): the old routes only. **Track** (#e3e8f3): the empty rail the blue fill runs along. **Hairline** (#e1e6f0): list rules and card borders.

### Named Rules
**The One Blue Rule.** There is exactly one blue line. Blue never appears as a decorative fill.

**The Grey Is Before Rule.** Grey routes and unreached stations mean "not yet" or "before". They carry no text the visitor needs.

## Typography

**Font:** Host Grotesk (variable 300 to 800, self-hosted), Helvetica Neue and Arial as fallback.

**Character:** a clear, wide, Helvetica-like grotesque in the tradition of transit signage, heavy at display size and plain for reading.

### Hierarchy
- **Display** (800, clamp(2.75rem, 5.3vw, 4.875rem), 0.97, -0.04em): hero headline.
- **Headline** (800, clamp(2.125rem, 4.8vw, 4.25rem), 0.98, -0.035em): section headings and the terminus.
- **Title** (700, 1.5rem, 1.1): stage names; module leads at 700 and 1.25 to 1.625rem.
- **Body** (400, 1.0625rem, 1.62): paragraphs at 40 to 54ch.
- **Label** (700, 0.8125rem): form labels.

## Layout

A 1240px container. The hero is a two-column top (headline 8, lede 4) over a full-bleed map band at 500 to 600px tall: routes enter from the left edge, merge at 30%, stations sit at 35, 43, 51 and 59%, the terminus at 80% with the form card hung below it. Below the hero a rail runs down the left (spine at 30px, content from 118px) and each section adds one station. Sections use a 5/7 split of text and UI sketch. Below 860px the spine moves to 12px, the hero map becomes a short converging graphic followed by a vertical stop list, and everything stacks.

## Elevation & Depth

Flat. Cards use a 1px hairline, the tray and the contact form use a 2px blue outline, and stations get a white halo (box-shadow 0 0 0 6px white) only to cut the line cleanly behind them.

## Shapes

Rounded line ends (7px radius on the 14px line) and 45 degree bends; stations are circles; cards and fields are 8 to 12px radius rectangles. The line never curves.

## Components

### Buttons
- **Blue (primary):** Line Blue fill, white text, 10px radius, 52px high; hover turns Ink and lifts 2px.
- **Line:** 2px Ink border; fills Ink on hover.

### Stations
Disc with a thick ring (34px, 9px ring; 54px for section stations; 76px with a gold outer ring for the terminus). Grey until `is-reached`, then blue; gold for AI.

### Tray (hero form)
A 12px-radius card with a 2px blue outline hung under the terminus by a 4px stem.

### Tracks (audiences)
Two parallel 14px lines on the left rail, blue for companies and gold for training bodies, joined to the spine by short bars at both ends.

## Do's and Don'ts

### Do:
- **Do** keep a single blue line and let grey routes mean "before".
- **Do** put Ink text on gold, white on blue.
- **Do** reduce the number of lines as the page goes on.
- **Do** keep stations ringed and flat; the spine fills as you scroll.

### Don't:
- **Don't** add shadows, gradients or glass.
- **Don't** use a second blue or tint the line.
- **Don't** put equal feature cards in a row.
- **Don't** invent customers, certifications, AI models or hosting claims.

## Not canonized

The interface sketches (assets/css/ui.css) are illustrative and use their own muted palette; the screenshot is a crop of goodlearning.it's own promotional image and is soft at large sizes; the mobile hero's converging routes are decorative geometry.
