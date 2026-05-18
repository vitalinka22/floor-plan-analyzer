# Floor Plan Analysis Report
**File:** input/Floorplan_P1_Mosbach.pdf

## Summary
- **Wohnfläche:** 212.9 m²
- **Rooms:** 9
- **Bathrooms:** 4
- **Kitchen:** separate
- **Balcony:** True
- **Terrace:** False
- **Storage room:** True
- **Floor level:** Floor 1-4
- **Property type:** house

## Wohnfläche Breakdown
| Room | Type | Area (m²) | Coefficient | Contribution (m²) |
|------|------|-----------|-------------|-------------------|
| PRIMARY BEDROOM | living | 18.5 | 1.0 | 18.5 |
| BEDROOM | living | 15.1 | 1.0 | 15.1 |
| HALLWAY | hallway | 3.7 | 1.0 | 3.7 |
| HALLWAY | hallway | 3.1 | 1.0 | 3.1 |
| LAUNDRY | storage | 3.6 | 1.0 | 3.6 |
| BATHROOM | bathroom | 3.8 | 1.0 | 3.8 |
| HALLWAY | hallway | 6.7 | 1.0 | 6.7 |
| LIVING ROOM | living | 18.3 | 1.0 | 18.3 |
| BEDROOM | living | 15.3 | 1.0 | 15.3 |
| HALLWAY | hallway | 3.1 | 1.0 | 3.1 |
| KITCHEN/DINING ROOM | kitchen | 13.1 | 1.0 | 13.1 |
| BATHROOM | bathroom | 4.8 | 1.0 | 4.8 |
| ENTRY | hallway | 5.9 | 1.0 | 5.9 |
| FAMILY ROOM | living | 18.4 | 1.0 | 18.4 |
| BEDROOM | living | 15.7 | 1.0 | 15.7 |
| HALLWAY | hallway | 3.2 | 1.0 | 3.2 |
| KITCHEN/DINING ROOM | kitchen | 13.1 | 1.0 | 13.1 |
| BATHROOM | bathroom | 4.3 | 1.0 | 4.3 |
| LANDING | hallway | 2.3 | 1.0 | 2.3 |
| BALCONY | balcony | 10.1 | 0.25 | 2.52 |
| LOFT | loft | 27.8 | 0.5 | 13.9 |
| HALLWAY | hallway | 18.7 | 1.0 | 18.7 |
| BATHROOM | bathroom | 5.8 | 1.0 | 5.8 |

## Assumptions & Notes
- Balconies and terraces counted at 25% per WoFlV
- Loft areas counted at 50% due to unknown ceiling height
- All interior rooms (hallway, bathroom, storage) counted at 100%
- Shared staircases excluded at 0%
- Room dimensions taken directly from floor plan labels
- Naming discrepancy for Floor 1 'PRIMARY BEDROOM' and 'BEDROOM' between AI extraction and PDF text.
- Minor width discrepancy for Floor 3 'BATHROOM' (AI: 1.98m, PDF: 1.89m).
- Unusually large hallway on Floor 4 (18.7 m²).
- A large 'PATIO' area (230 m² or ~312.2 m²) is mentioned in the PDF but is missing from the AI extraction and Wohnfläche calculation.
- AI-extracted room areas (total 224.3 m²) are less than the PDF stated 'TOTAL GROSS INTERNAL AREA' (239 m²), suggesting potential missing internal areas or different measurement methodologies.