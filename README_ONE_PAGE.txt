# KikwiNok (Kikwi Watso) — Seasonal Azimuth Explorer (Offline)
**Version:** v0.1.1  
**Author:** Cam Bergeron (Ndakinna Creations)  
**Purpose:** Fast, repeatable screening for possible solar/lunar alignment directions at a site.

![KikwiNok GUI Screenshot](KikwiNok.png)
<img src="KikwiNok.png" alt="KikwiNok GUI Screenshot" width="520">

## Download (Windows)
- ✅ **Windows Installer (recommended):** https://github.com/cbergeron243/Kikwi-Watso/releases/tag/v0.1.1  
- ✅ **Portable ZIP:** https://github.com/cbergeron243/Kikwi-Watso/releases/tag/v0.1.1  
- (Mirror) OneDrive Installer: https://1drv.ms/u/c/cd84df7252bd943e/IQCsVe3g2I9-QJQxSvrwcJE5AZ6glqTQGTAkkulBs6tvVvM?e=ryaRoD

If Windows SmartScreen appears, click **More info → Run anyway** (unsigned build).

---

## What KikwiNok does
KikwiNok computes **azimuth targets (degrees from North)** across a user-defined year range for:

- **Seasonal SUNSET and/or SUNRISE markers** (Solstices, Equinoxes, Cross-quarter midpoints)
- Optional **lunar standstill reference rails** (major/minor, North/South)

It saves:
- **PNG chart** (visual summary)
- **CSV dataset** (all computed values)

---

## What it is / what it isn’t
✅ A **triage / screening tool** to guide field checks and prioritize return visits  
✅ Best used alongside field measurement, horizon notes, and archaeological/cultural context  
❌ Not proof of intentional design, dating, or cultural attribution

---

## Why there is no Longitude field
For **rise/set azimuth targets**, longitude is not required.  
Longitude is needed for **clock times** (local event timing) and time-specific sky positions—not the azimuth targets themselves.

---

## How to run (30 seconds)
1. Launch **KikwiNok**
2. Enter **Site name, Latitude, Elevation, Start year, End year**
3. Choose options (**Lunar rails / Compute SUNSET / Compute SUNRISE**)
4. Click **Run**

---

## Output files
Saved to your selected output folder:
- `…_kikwi.png` (chart)
- `…_kikwi.csv` (table)

---

## Field workflow tip
Measure a site sightline azimuth (a phone compass is fine for screening), then compare it to the chart’s target families.  
If it’s close, it may be worth deeper measurement, horizon modeling, and follow-up.


