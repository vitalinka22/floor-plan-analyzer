# Floor Plan Analyzer

An AI-powered pipeline that analyzes floor plan PDFs and produces structured property summaries including Wohnfläche calculation, room extraction, and attribute analysis.

---

## Architecture

The system is built as a **multi-agent pipeline** where each agent has a single responsibility:

```
PDF
 ├──► extraction_agent    →  extracts text + coordinates via pdfplumber
 └──► vision_agent        →  extracts rooms + attributes via Gemini vision AI
          │
          ▼
     calculation_agent    →  calculates Wohnfläche using WoFlV rules
          │
          ▼
     reconciliation_agent →  cross-validates both sources, flags inconsistencies
          │
          ▼
      evaluation_agent    →  resolves conflicts, produces final structured output
          │
          ▼
        main.py           →  orchestrates pipeline, saves JSON + Markdown report
```

### Why two extraction sources?

- **pdfplumber** extracts text with pixel coordinates from the PDF text layer — deterministic, no hallucination risk
- **Gemini vision** understands the visual layout — spatial relationships, room shapes, unlabeled features

Together they cross-validate each other. If Gemini extracts a room dimension that doesn't appear anywhere in the PDF text, it gets flagged as uncertain.

---

## Wohnfläche Calculation Methodology

Calculation follows a simplified Wohnflächenverordnung (WoFlV) approach:

| Room Type | Coefficient | Examples |
|---|---|---|
| Living rooms, bedrooms | 100% | Wohnzimmer, Schlafzimmer, Kinderzimmer |
| Kitchen | 100% | Küche, EBK |
| Bathroom / WC | 100% | Bad, Duschbad, WC |
| Hallway / Entry | 100% | Flur, Diele, Eingang |
| Storage room | 100% | Abstellraum, HWR |
| Balcony / Terrace / Loggia | 25% | Balkon, Terrasse |
| Loft / Attic | 50% | DG-Zimmer, Galerie (ceiling height unknown) |
| Shared staircase | 0% | Treppenhaus outside apartment |

**If the floor plan states a total area** (e.g. `GESAMTFLÄCHE: 44.95 m²` or `GROSS INTERNAL AREA`), that value is preferred over the sum of individual rooms, as labeled totals are more reliable than AI-extracted room-by-room calculations.

---

## Project Structure

```
floor_plan_analyzer/
├── agents/
│   ├── extraction_agent.py     # pdfplumber text + coordinate extraction
│   ├── vision_agent.py         # Gemini vision floor plan analysis
│   ├── calculation_agent.py    # Wohnfläche calculation (WoFlV rules)
│   ├── reconciliation_agent.py # cross-validation of both sources
│   └── evaluation_agent.py     # final conflict resolution + structured output
├── utils/
│   └── pdf_to_image.py         # PDF page to PIL image conversion
├── input/                      # place floor plan PDFs here
├── output/                     # generated reports saved here
├── main.py                     # pipeline orchestrator
├── requirements.txt
└── .env                        # GEMINI_API_KEY
```

---

## Setup

**1. Clone the repository and create a virtual environment:**
```bash
python -m venv venv
source venv/bin/activate
```

**2. Install dependencies:**
```bash
pip install -r requirements.txt
```

**3. Add your Gemini API key to `.env`:**
```
GEMINI_API_KEY=your_key_here
```

**4. Place floor plan PDFs in the `input/` folder.**

---

## Usage

```bash
python main.py
```

This processes all PDFs listed in `main.py` and saves two files per PDF to `output/`:
- `{filename}_result.json` — structured data
- `{filename}_report.md` — human-readable report with breakdown table and notes

---

## Output Format

```json
{
  "wohnflaeche_sqm": 44.95,
  "rooms": 2,
  "bathrooms": 1,
  "balcony": false,
  "terrace": false,
  "kitchen": "open",
  "storage_room": true,
  "floor_level": "2.OG",
  "property_type": "apartment",
  "special_features": [],
  "notes": [
    "Balconies and terraces counted at 25% per WoFlV",
    "PDF states 6 rooms, vision AI extracted 4 — two rooms may be missing"
  ],
  "wohnflaeche_breakdown": [
    {
      "name": "Wohnzimmer",
      "type": "living",
      "area": 18.24,
      "coefficient": 1.0,
      "contribution": 18.24
    }
  ]
}
```

---

## Sample Results

### Appartment Transvaal
| Attribute | Value |
|---|---|
| Wohnfläche | 44.95 m² |
| Rooms | 2 |
| Bathrooms | 1 |
| Kitchen | open |
| Floor | 2.OG |
| Property type | apartment |

### Floorplan Mosbach
| Attribute | Value |
|---|---|
| Wohnfläche | 212.9 m² |
| Rooms | 9 |
| Bathrooms | 4 |
| Kitchen | separate |
| Floors | Floor 1–4 |
| Property type | house |
| Special features | Open to below, Patio |

---

## Assumptions & Limitations

- Loft ceiling heights are unknown from floor plans — assumed 50% coefficient
- AI vision extraction may miss rooms on complex multi-floor plans — reconciliation agent flags these gaps
- Patio/garden areas are excluded from Wohnfläche (outdoor area, 0%)
- Where dimensions are labeled but not area, area = width × length
- This implementation is a simplified WoFlV approach — not a legally certified calculation

---

## Tech Stack

- [Google Gemini 2.5 Flash](https://deepmind.google/technologies/gemini/) — vision AI for floor plan analysis
- [pdfplumber](https://github.com/jsvine/pdfplumber) — PDF text extraction with coordinates
- [PyMuPDF](https://pymupdf.readthedocs.io/) — PDF to image conversion
- [Pillow](https://pillow.readthedocs.io/) — image handling
