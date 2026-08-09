# Reviewer Skills Experiment Image Prompt

The README diagram was generated with OpenAI's built-in image-generation tool.
The existing project diagram was used as the conceptual edit target, while the
README diagrams from
[dryscope](https://github.com/kvsankar/dryscope),
[agent-history](https://github.com/kvsankar/agent-history), and
[sarathi](https://github.com/kvsankar/sarathi) were used only as style
references.

## Generation Prompt

```text
Use case: infographic-diagram
Asset type: replacement hero/process diagram for the README of the open-source
"Reviewer Skills" repository

Input images:
- Image 1 is the CURRENT PROJECT IMAGE and the conceptual edit target. Preserve
  its title, subtitle, four-stage historical arc, clean white technical-
  infographic character, restrained palette, and conclusion tone, but redesign
  the main body substantially.
- Images 2, 3, and 4 are STYLE REFERENCES ONLY. Match their polished
  documentation aesthetic, typography hierarchy, rounded panels, thin
  connectors, disciplined information density, and original line icons. Do not
  copy their project content or exact layouts.

Primary request: Redesign the image so it clearly presents a SUITE OF RESEARCH,
PROTOTYPES, AND EXPERIMENTS rather than implying that the project was only one
regular-versus-guided A/B test. Call out the four key experiment families. Show
that the final real-code A/B was the strongest closing test, but only one branch
of a multidimensional exploration.

Exact title: "reviewer skills"
Exact subtitle: "Can in-context guidance improve agentic code review?"

Composition:
- Wide 3:2 landscape canvas for a GitHub README.
- White background, generous margin, highly legible at README width.
- Title and subtitle centered at top.
- Retain a slim four-stage ribbon immediately below:
  "1  BUILD" — "23 reviewer skills"
  "2  RESEARCH" — "literature + prototypes"
  "3  EVALUATE" — "multiple branches, real code"
  "4  CLOSE" — "retain the evidence"

Main body: three connected zones from left to right.

LEFT ZONE, blue-gray, about 23% width:
Heading: "RESEARCH & PROTOTYPES"
Three compact stacked cards with simple original icons:
1. "IN-CONTEXT LEARNING"
   small text: "examples • selection • prompt size"
2. "RELEVANCE RETRIEVAL"
   small text: "embeddings • code structure"
3. "REVIEW ORCHESTRATION"
   small text: "multi-agent • Docker harness"
Use a book/magnifier icon, a target/filter icon, and a connected-agents icon.

CENTER ZONE, about 52% width:
Heading: "KEY EXPERIMENTS"
A clean 2-by-2 grid of four equal cards, each numbered and visually distinct but
coordinated:

Card 1, blue:
"PROMPT ABLATIONS"
"full skills • principles • IDs"
"trimmed • hybrid"

Card 2, purple:
"RHODES EVALUATIONS"
"synthetic + real code"
Add a small neutral outlined badge: "synthetic evidence withdrawn"

Card 3, green:
"LOCAL-MODEL PILOT"
"Pi + Ollama"
"Qwen3 Coder • Devstral"

Card 4, orange/navy emphasis:
"FINAL REAL-CODE A/B"
"regular vs lean • Codex"
"revised finding union"
Add a small badge: "strongest closing test"

Connect the research/prototype zone into the experiment suite with a subtle
arrow labeled "informed". Connect all four experiment cards toward the result,
visually indicating accumulated evidence rather than a single linear test.

RIGHT ZONE, navy-bordered, about 22% width:
Heading: "RESULT"
Central statement: "NO CONCLUSIVE IMPROVEMENT"
Supporting text: "No tested branch showed that the skills found more useful
issues."
Smaller text: "Full skills • compact guidance • retrieval"
Next line: "frontier agents • tested local models"
Footer in italic: "A dated experiment — not a universal claim."
Small badge: "COMPLETED EXPERIMENT"
Keep this neutral, calm, and evidence-led; do not use failure red.

BOTTOM FULL-WIDTH STRIP:
Heading: "FINAL EVIDENCE METHOD"
A compact left-to-right sequence of four icon-label steps:
"real code only" → "revised finding union" → "blind matching" →
"source-aware adjudication"
Small end label: "Claude judge"
This strip explains the closing methodology without making it look like the
only experiment.

Visual semantics:
- Navy for headings, conclusion, and archival status.
- Blue for research and prompt ablations.
- Purple for Rhodes evaluations and pooled evidence.
- Green for local models.
- Orange only as restrained emphasis for the final A/B and adjudication.
- Soft gray fills, mostly flat vector-like editorial rendering, very light
  shadows.
- Use consistent original line icons: book/research, filter/target, agent
  network, checklist, Python/code-quality symbol without logos, laptop/model,
  A/B split, evidence merge, magnifier/check, archive box.
- Arrows must clearly show research informing multiple experiment branches,
  then evidence accumulating into the result.

Typography:
- Bold condensed sans-serif title and section headers.
- Clean modern sans-serif body labels.
- Excellent spelling and text legibility.
- Render all quoted text exactly. Spell "Rhodes", "Ollama", "Qwen3 Coder",
  "Devstral", "Codex", "Claude", "adjudication", and "conclusive" correctly.

Constraints:
- No company logos, mascots, people, code screenshots, invented metrics,
  percentages, fake citations, equations, watermarks, signatures, or unrelated
  badges.
- Do not imply that synthetic tests were retained as effectiveness evidence.
- Do not imply that only compact IDs were tested.
- Do not imply that prompts can never help.
- Avoid clutter and tiny prose; the key structure and labels must remain
  readable at README width.
- Do not copy any reference image's exact composition or project-specific
  content.
```

## Accuracy Correction Prompt

The first result sentence was stronger than the retained evidence supported.
The following precision edit produced the committed image:

```text
Use case: precise-object-edit
Asset type: README technical infographic
Input image: Image 1 is the EDIT TARGET.

Primary request: Change only the supporting sentence in the navy-bordered
RESULT panel on the right.

Replace the existing sentence:
"No tested branch showed that the skills found more useful issues."

With exactly these two lines:
"No branch produced conclusive evidence"
"that the skills found more useful issues."

Invariants:
- Preserve the entire image composition, dimensions, white background, title,
  subtitle, four-stage ribbon, research cards, all four key-experiment cards,
  arrows, bottom evidence-method strip, icons, colors, typography, spacing, and
  line weights as closely as possible.
- Keep "NO CONCLUSIVE IMPROVEMENT" unchanged.
- Keep every other word and phrase exactly unchanged and correctly spelled.
- Match the replacement sentence's font, weight, color, alignment, and size to
  the current supporting sentence.
- Do not move or redraw any other element.
- No watermark or signature.
```
