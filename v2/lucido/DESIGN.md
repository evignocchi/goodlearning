---
name: Goodlearning Landing v2, Il lucido
description: A light table. A grey tangle underneath, vellum sheets over it, one bold cobalt line that keeps only what matters.
colors:
  table: "#eef1f7"
  table-lift: "#f7f9fc"
  sheet: "#ffffff"
  ink: "#0b1430"
  ink-soft: "#47536f"
  graphite: "#8a94ab"
  trace: "#0b57d0"
  highlighter: "#f5c400"
typography:
  display:
    fontFamily: "Bricolage, Helvetica Neue, Arial, sans-serif"
    fontSize: "clamp(2.75rem, 5.7vw, 5.25rem)"
    fontWeight: 700
    lineHeight: 1
    letterSpacing: "-0.028em"
  headline:
    fontFamily: "Bricolage, Helvetica Neue, Arial, sans-serif"
    fontSize: "clamp(2.125rem, 4.6vw, 4rem)"
    fontWeight: 700
    lineHeight: 1
    letterSpacing: "-0.022em"
  title:
    fontFamily: "Bricolage, Helvetica Neue, Arial, sans-serif"
    fontSize: "1.5rem"
    fontWeight: 700
    lineHeight: 1.12
  body:
    fontFamily: "Hanken, system-ui, sans-serif"
    fontSize: "1.0625rem"
    fontWeight: 400
    lineHeight: 1.65
  label:
    fontFamily: "Hanken, system-ui, sans-serif"
    fontSize: "0.875rem"
    fontWeight: 600
    lineHeight: 1.4
rounded:
  field: "12px"
  button: "14px"
  sheet: "18px"
spacing:
  sm: "16px"
  md: "24px"
  lg: "48px"
  xl: "96px"
components:
  button-ink:
    backgroundColor: "{colors.ink}"
    textColor: "#ffffff"
    rounded: "{rounded.button}"
    padding: "0 24px"
    height: "52px"
  button-ink-hover:
    backgroundColor: "{colors.trace}"
  field:
    backgroundColor: "{colors.sheet}"
    textColor: "{colors.ink}"
    rounded: "{rounded.field}"
    padding: "0 16px"
    height: "52px"
  sheet:
    backgroundColor: "{colors.sheet}"
    textColor: "{colors.ink}"
    rounded: "{rounded.sheet}"
    padding: "22px"
---

# Design System: Goodlearning Landing v2, Il lucido

## Overview

**Creative North Star: "The Light Table"**

An architect's light table in daylight: the old process lies underneath as a grey tangle of hairlines and half-drawn spreadsheets, mail and registers, and a sheet of vellum lies over it. On the vellum one thick cobalt line keeps only the essential. The page is that act of tracing, repeated: each platform sheet lies over its own faded tangle and the tangle fades further when the sheet enters the view, and the contact form is the last clean sheet, with almost nothing left around it.

The mood is airy, precise and calm, with one loud move at the top. Colour is restrained: a cool table ground, white vellum, ink, one blue, and a yellow highlighter used only on the thing being traced (the headline word, the key numbers, the AI region of the real screenshot).

**Key Characteristics:**
- Translucent sheets whose blur is real: they soften what lies beneath them.
- One bold blue line over a grey tangle is the signature.
- Yellow is a highlighter pen, never a fill for large areas.
- Real GoodSuite screen at the end of the line; sketches are marked as illustrative.
- The contact action stays level in the corner once the first screen has gone.

## Colors

A cool grey-blue table, white vellum, ink, cobalt, and a yellow marker.

### Primary
- **Cobalt Trace** (#0b57d0): the traced line, links in motion, hover on ink buttons, the number discs.

### Secondary
- **Highlighter Yellow** (#f5c400): the marker stroke behind "tracciati" and the key numbers, the ring around the AI menu in the screenshot, underline of text links. The same yellow as the Goodlearning AI logos.

### Neutral
- **Table** (#eef1f7): page ground. **Table Lift** (#f7f9fc): alternate bands. **Sheet White** (#ffffff, used at about 72% as vellum): sheets, chips and fields.
- **Ink** (#0b1430): text, primary buttons, footer. **Ink Soft** (#47536f): secondary text (6.9:1 on Table). **Graphite** (#8a94ab): the tangle only, never text.

### Named Rules
**The Marker Rule.** Yellow marks the one thing that was traced. It never fills a button, a card or a background.

**The Graphite Is Mess Rule.** Graphite hairlines mean "before". Nothing the visitor must read is ever graphite.

## Typography

**Display Font:** Bricolage Grotesque (variable, self-hosted). **Body Font:** Hanken Grotesk (variable, self-hosted).

**Character:** an expressive, slightly condensed grotesque for headlines and a calm, open grotesque for reading. Headlines are sentence case, tight but never touching (tracking -0.022 to -0.028em).

### Hierarchy
- **Display** (700, clamp(2.75rem, 5.7vw, 5.25rem), 1.0): hero headline only.
- **Headline** (700, clamp(2.125rem, 4.6vw, 4rem), 1.0): section headings.
- **Title** (700, 1.5rem, 1.12): stage and list headings; module leads at 600.
- **Body** (400, 1.0625rem, 1.65): paragraphs, 54 to 62ch; leads at 1.125 to 1.3125rem in Ink Soft.
- **Label** (600, 0.875rem): form labels and captions.

## Layout

A 1240px container with a fluid 16 to 48px gutter. The hero stacks headline, lede and a four-field row (three fields and the button), then a full-bleed band that holds the tracing: tangle on the left, a vellum sheet from 29% to 98%, the line and four chips, the real screenshot at 68%. Platform stages alternate sheet and text at 7/5 columns; the audiences are two staggered sheets; proof is a 12-column grid of quote sheets; the contact is one centred sheet. Below 860px the band becomes a vertical list with a blue line on the left and the screenshot at full width.

## Elevation & Depth

Depth is optical, not decorative. Vellum sheets carry a short offset shadow (0 12px 22px -14px at 30%), a 1px contact shadow and a top catch-light, and they blur what lies under them (8px). Nothing glows. Hover is a 2px lift.

### Named Rules
**The Real Blur Rule.** A sheet may blur only when something worth softening lies beneath it (a tangle, another sheet). Never blur an empty ground.

## Shapes

Soft but not pillowy: 18px sheets, 14px buttons, 12px fields and chips, 10px UI sketches. The blue line has round caps and joins; the tangle uses uneven curves on purpose.

## Components

### Buttons
- **Ink (primary):** Ink fill, white text, 14px radius, 52px high; hover turns Cobalt and lifts 2px.
- **Line:** 1.5px Ink border; inverts on hover.
- **Dock:** the contact button fixed in the corner after 640px of scroll, hidden while the contact section is on screen.

### Fields
White fill, 1.5px 22% Ink border, 12px radius; focus is a Cobalt border with a 4px soft ring. Choice chips fill with Ink when checked.

### Chips (tracing stops)
White cards with a ringed dot on the line and a 2px stem; they alternate above and below the line.

## Do's and Don'ts

### Do:
- **Do** keep one line, one blur reason and one highlighted thing per view.
- **Do** show the real screenshot where the line ends, and label sketches as illustrative.
- **Do** keep Ink on yellow and white on Ink or Cobalt.
- **Do** let the page get simpler toward the contact sheet.

### Don't:
- **Don't** fill areas with yellow or use it for text.
- **Don't** add glows, neon, coloured shadows or gradient text.
- **Don't** use eyebrows or kickers above headings.
- **Don't** invent customers, certifications, AI models or hosting claims.

## Not canonized

The interface sketches (assets/css/ui.css) are illustrative and carry their own muted palette; the hero screenshot is a crop of goodlearning.it's own promotional image and is soft at large sizes; the tangle is generated geometry, not a drawing.
