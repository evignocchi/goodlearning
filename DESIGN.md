---
name: Goodlearning Landing
description: Flat cobalt bands, a continuous conveyor belt and one orange sheet: Italian industrial modernism for an LMS that turns documents into tracked courses.
colors:
  cobalt-field: "#0a47c9"
  cobalt-deep: "#073296"
  sky-tint: "#8fb9f2"
  sky-text: "#cfe0ff"
  paper: "#f2f5fb"
  white: "#ffffff"
  ink: "#071a45"
  ink-soft: "#34456f"
  signal: "#ff4a1c"
  signal-dark: "#c93410"
typography:
  display:
    fontFamily: "Archivo, Helvetica Neue, Arial, sans-serif"
    fontSize: "clamp(2.75rem, 8.4vw, 6rem)"
    fontWeight: 800
    lineHeight: 0.98
    letterSpacing: "-0.035em"
    fontVariation: "wdth 118"
  headline:
    fontFamily: "Archivo, Helvetica Neue, Arial, sans-serif"
    fontSize: "clamp(2rem, 4.8vw, 3.75rem)"
    fontWeight: 800
    lineHeight: 0.98
    letterSpacing: "-0.035em"
    fontVariation: "wdth 112"
  title:
    fontFamily: "Archivo, Helvetica Neue, Arial, sans-serif"
    fontSize: "1.375rem"
    fontWeight: 700
    lineHeight: 1.15
    letterSpacing: "-0.015em"
    fontVariation: "wdth 108"
  body:
    fontFamily: "Archivo, Helvetica Neue, Arial, sans-serif"
    fontSize: "1.0625rem"
    fontWeight: 400
    lineHeight: 1.6
    fontVariation: "wdth 100"
  label:
    fontFamily: "Archivo, Helvetica Neue, Arial, sans-serif"
    fontSize: "0.875rem"
    fontWeight: 700
    lineHeight: 1.4
    fontVariation: "wdth 104"
rounded:
  none: "0px"
spacing:
  xs: "8px"
  sm: "16px"
  md: "24px"
  lg: "48px"
  xl: "96px"
components:
  button-signal:
    backgroundColor: "{colors.signal}"
    textColor: "{colors.ink}"
    rounded: "{rounded.none}"
    padding: "0 24px"
    height: "52px"
  button-signal-hover:
    backgroundColor: "#ff6a42"
  button-line:
    backgroundColor: "transparent"
    textColor: "{colors.white}"
    rounded: "{rounded.none}"
    padding: "0 24px"
    height: "52px"
  field-input:
    backgroundColor: "{colors.paper}"
    textColor: "{colors.ink}"
    rounded: "{rounded.none}"
    padding: "12px 14px"
    height: "52px"
  tray:
    backgroundColor: "{colors.white}"
    textColor: "{colors.ink}"
    rounded: "{rounded.none}"
    padding: "32px"
---

# Design System: Goodlearning Landing

## Overview

**Creative North Star: "The Assembly Line"**

GoodSuite takes a document in and delivers a tracked course out, so the page is built like the machine that does it: flat, frontal, one object seen once. Whole bands of electric cobalt carry the page, a chain-link conveyor belt runs under the stations of the hero and returns at the foot of the proof band, and the only warm colour is the orange of the paper moving along it and of the action that asks for contact. It borrows the discipline of Italian industrial modernism (flat blocks, hard alignment, oversized lowercase grotesque) and executes it as a contemporary screen, with no retro texture, no faux material and no ornament that does not belong to the machine.

Density is generous in the headlines and tight in the ledgers. Large type and colour do the persuading; ruled lists (extras, audience tables, testimonials, FAQ) do the explaining. The page avoids the category default of headline left, dashboard right, logo strip below.

**Key Characteristics:**
- Committed colour: cobalt owns whole bands, not accents.
- One signature, repeated: the belt, with the orange sheet on it.
- Lowercase, wide, heavy display type that echoes the lowercase logo.
- Square corners everywhere; depth comes from colour blocks, never from shadow.
- Real content only: numbers, quotes and prices come from the live site.

## Colors

A committed cobalt field, cool white plates, deep ink and a single signal orange.

### Primary
- **Cobalt Field** (#0a47c9): the hero, the contact band and the proof band. Pushes the logo's blue family (#0060b0) to full saturation. Text on it is white (7.6:1) or Sky Text (5.7:1).
- **Cobalt Deep** (#073296): the mobile menu panel only.

### Secondary
- **Sky Tint** (#8fb9f2): the "enti di formazione" half of the audience band, rollers, back cards in drawings. Ink text on it reads at 8.4:1.
- **Sky Text** (#cfe0ff): secondary copy on cobalt and on ink.

### Tertiary
- **Signal Orange** (#ff4a1c): the contact action, the sheet on the belt, ticks in the register, the selected AI module. Always with Ink text, never white (white fails at 3.6:1). **Signal Dark** (#c93410) is the folded corner and the pressed state.

### Neutral
- **Paper** (#f2f5fb): page ground and field backgrounds. Cool, never cream.
- **White** (#ffffff): nameplate, tray, audience column, proof.
- **Ink** (#071a45): all text on light grounds, the AI band, drawing linework.
- **Ink Soft** (#34456f): secondary text on light grounds (8.6:1).

### Named Rules
**The Orange Is Paper Rule.** Orange appears only as something being processed (the sheet, the ticks) or as the action that continues the process (contact). It is never a decorative accent.

**The Cool Ground Rule.** Light grounds stay cool (Paper, White). Warm cream is the rendition prior for this category and is not part of this world.

## Typography

**Display Font:** Archivo variable (self-hosted, wght 100 to 900, wdth 62 to 125), with Helvetica Neue and Arial as fallback.
**Body Font:** the same family at normal width. One family, two widths.

**Character:** a wide, heavy grotesque for headlines and the same letterforms at normal width for reading, so the page reads as one machine-cut voice. Headlines are written lowercase in the source (acronyms and brand names keep their capitals); there is no automatic text transform.

### Hierarchy
- **Display** (800, clamp(2.75rem, 8.4vw, 6rem), 0.98, wdth 118, tracking -0.035em): the hero headline only.
- **Headline** (800, clamp(2rem, 4.8vw, 3.75rem), 0.98, wdth 112): section headings.
- **Title** (700, 1.375rem, 1.15, wdth 108): stage and list headings, tray title, station names at 1.0625rem.
- **Body** (400, 1.0625rem, 1.6, wdth 100): paragraphs, measure capped at 62ch; leads at 1.1875 to 1.375rem.
- **Label** (700, 0.875rem, wdth 104): form labels and small captions.

### Named Rules
**The Lowercase Voice Rule.** Display and headline text is lowercase in the source to echo the logo. Do not apply `text-transform`: it breaks "AI" and "GoodSuite".

**The Tracking Floor Rule.** Tight tracking stops at -0.035em. Numerals are tabular.

## Layout

A 1320px container with a fluid 16 to 48px gutter. The hero is a stack: headline, belt across the full width, then a two-column foot (lede left, contact tray right). Sections alternate full-bleed bands (cobalt, paper, ink, white, sky) and run on an 8px base with section padding of 64 to 128px. Below 900px the foot stacks and the tray bleeds to the screen edges; below 760px the belt turns vertical along the left edge and the four stations stack. On screens 840px tall or less the hero shrinks (belt height 112px, headline sized from viewport height) so the contact button stays in the first screen.

## Elevation & Depth

Flat by default and flat on purpose. Depth is carried by adjacent colour blocks, a 2px ink rule over lists, and 1px hairlines between rows. There are no box shadows. Layering inside drawings (a pale card behind a white one) is the only stacking.

### Named Rules
**The No Shadow Rule.** Nothing casts a shadow. Hover is a 2px lift and a lighter orange, nothing more.

## Shapes

Square corners (0px) on every button, field, tray and plate. The conveyor is a repeating chain of 16px plates with 6px gaps at 8px height; its arrowhead and the sheet's folded corner are clipped polygons. The drawings are flat primitives: rectangles, circles, one triangle, no gradients, no outlines thinner than 2px.

## Components

### Buttons
- **Shape:** square (0px), 52px high, 700 weight at wdth 108.
- **Signal (primary):** Signal Orange fill, Ink text, 0 24px padding. Hover lifts 2px and lightens to #ff6a42; pressed drops to Signal Dark.
- **Line (secondary):** 2px currentColor border; inverts to white with cobalt text on hover over cobalt grounds.
- **Focus:** 3px outline, 3px offset, white on cobalt and ink bands, orange on light bands, cobalt inside the tray.

### Inputs / Fields
- **Style:** 2px Ink border, Paper fill, 52px minimum height, 16px text.
- **Focus:** the 3px focus outline plus a white fill. **Invalid:** a #b3250a border on a pale red fill.
- **Choice chips:** the same border; the checked chip fills with Ink.

### Navigation
A white nameplate tab holding the logo sits flush to the top-left of a cobalt bar; links are 15px, 600 weight, with an orange underline on hover. Under 1020px the links collapse into a Cobalt Deep panel opened by a bordered "Menu" button.

### Belt Station (signature)
A flat drawing standing on the belt, a one-line name in Title weight, a one-line note in Sky Text. The belt is the chain gradient across the whole row. On load an orange sheet travels the belt once and each station arrives in sequence; with reduced motion everything shows in its final state.

### Module Selector
Three oversized names stacked as a tablist. The selected one turns orange and slides 20px right; the others sit at 40% opacity (3.7:1 on Ink, allowed for large type). The panel is sticky on the right.

### Ledger and FAQ rows
A 2px Ink rule opens the list, 1px hairlines separate rows. Testimonials use a 4/8 two-column split with name and role left; the lead quote is larger and heavier.

## Do's and Don'ts

### Do:
- **Do** let cobalt own whole bands and keep every light ground cool.
- **Do** put Ink text on orange and white or Sky Text on cobalt.
- **Do** repeat the belt where the story is about process, and keep the orange sheet singular.
- **Do** keep copy plain and factual; every number, price and quote must exist on the live site.
- **Do** keep corners square and depth flat.

### Don't:
- **Don't** use white text on Signal Orange.
- **Don't** add shadows, gradients, glass, cream grounds or decorative orange.
- **Don't** use eyebrows or kickers above headings.
- **Don't** apply `text-transform: lowercase` to headings.
- **Don't** invent customers, certifications, AI model names or hosting claims.

## Not canonized

Carried by the build and not part of the system: the four 420x300 section drawings are assembled from primitives and stand in for real GoodSuite screenshots; the logo is a 190x31 PNG from the live site and looks soft on high-density screens; the hero's negative-margin nameplate is a layout workaround at widths under 1420px.
