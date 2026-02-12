#Kikwi_core.py
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from astropy.utils import iers
iers.conf.auto_download = False
iers.conf.iers_degraded_accuracy = "ignore"

# --- Constants ---
RAD = math.pi / 180.0
R_E = 6_371_000.0  # Earth radius (m)
H0 = -0.833        # Sun-centre alt at upper-limb touch (°)

# --- Eight seasonal spokes (Gregorian) ---
SEASONS = {
    "Cross-Qtr (Feb)" : (2, 1),
    "Equinox (Mar)"   : (3, 20),
    "Cross-Qtr (May)" : (5, 1),
    "Solstice (Jun)"  : (6, 21),
    "Cross-Qtr (Aug)" : (8, 1),
    "Equinox (Sep)"   : (9, 22),
    "Cross-Qtr (Nov)" : (11, 1),
    "Solstice (Dec)"  : (12, 21),
}

# Standstill declinations (geocentric, no nutation; close enough for visual/archaeo screening)
LUNAR_STANDSTILL_DECS = {
    "Lunar_Major_North":  28.6,
    "Lunar_Major_South": -28.6,
    "Lunar_Minor_North":  18.1,
    "Lunar_Minor_South": -18.1,
}

# --- Julian-day helper (UTC 12h) ---
def jd_utc(y, m, d, ut=12):
    if m <= 2:
        y -= 1
        m += 12
    A = y // 100
    B = 2 - A + A // 4
    jd = math.floor(365.25 * (y + 4716)) + math.floor(30.6001 * (m + 1)) + d + B - 1524.5
    return jd + ut / 24

# --- Solar declination (good ±10 k yr) ---
def sun_lon_dec(jd):
    T  = (jd - 2451545.0) / 36525
    L0 = (280.46646 + 36000.76983 * T + 0.0003032 * T * T) % 360
    g  = 357.52911 + 35999.05029 * T - 0.0001537 * T * T
    C  = (1.914602 - 0.004817 * T - 0.000014 * T * T) * math.sin(RAD * g) + \
         (0.019993 - 0.000101 * T) * math.sin(2 * RAD * g) + 0.000289 * math.sin(3 * RAD * g)
    lam = (L0 + C) % 360
    eps = 23.439291 - 0.0130042 * T
    dec = math.degrees(math.asin(math.sin(RAD * eps) * math.sin(RAD * lam)))
    return dec

# --- Horizon azimuth (sunset / sunrise) ---
def horizon_az(lat_deg, dec_deg, elev_m=0.0, *, rising=False):
    # horizon dip approximation (same as your original)
    dip = math.degrees(math.sqrt(2 * elev_m / R_E))
    h0  = math.radians(H0 - dip)
    φ, δ = map(math.radians, (lat_deg, dec_deg))

    cosH = (math.sin(h0) - math.sin(φ) * math.sin(δ)) / (math.cos(φ) * math.cos(δ))
    if abs(cosH) > 1:
        return None

    H = math.acos(cosH)
    if rising:
        H = -H

    A = math.atan2(-math.sin(H), math.tan(δ) * math.cos(φ) - math.cos(H) * math.sin(φ))
    return (math.degrees(A) + 360) % 360

def run_kikwi(
    *,
    lat: float,
    elev: float,
    yr0: int,
    yr1: int,
    site_name: str = "KikwiNok Site",
    include_lunar: bool = True,
    compute_sunset: bool = True,
    compute_sunrise: bool = False,
    out_dir: str | Path = "outputs",
    show_plot: bool = False,
) -> dict:
    """
    Returns dict with output file paths: {"csv": Path, "png": Path}
    """
    if yr1 < yr0:
        raise ValueError("End year must be >= start year.")

    if not compute_sunset and not compute_sunrise:
        raise ValueError("Select at least one of: compute_sunset, compute_sunrise.")

    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    YEARS = np.arange(yr0, yr1 + 1)

    frame = {"Year": YEARS}

    # solar series columns
    for tag in SEASONS:
        if compute_sunset:
            frame[f"{tag}_Sunset_Az"] = []
        if compute_sunrise:
            frame[f"{tag}_Sunrise_Az"] = []

    # lunar rails columns (constant in your current model, but we keep per-year for easy plotting/export)
    if include_lunar:
        for tag in LUNAR_STANDSTILL_DECS:
            frame[f"{tag}_Sunset_Az"] = []

    for yr in YEARS:
        # solar
        for tag, (m, d) in SEASONS.items():
            jd  = jd_utc(int(yr), m, d, 12)
            dec = sun_lon_dec(jd)

            if compute_sunset:
                az = horizon_az(lat, dec, elev_m=elev, rising=False)
                frame[f"{tag}_Sunset_Az"].append(az)

            if compute_sunrise:
                az = horizon_az(lat, dec, elev_m=elev, rising=True)
                frame[f"{tag}_Sunrise_Az"].append(az)

        # lunar rails (sunset-style rails, matching your chart)
        if include_lunar:
            for tag, dec in LUNAR_STANDSTILL_DECS.items():
                az = horizon_az(lat, dec, elev_m=elev, rising=False)
                frame[f"{tag}_Sunset_Az"].append(az)

    df = pd.DataFrame(frame)

    # Save CSV
    safe_site = "".join(c for c in site_name if c.isalnum() or c in (" ", "_", "-", ",")).strip().replace(" ", "_")
    csv_path = out_dir / f"{safe_site}_{yr0}_{yr1}_kikwi.csv"
    df.to_csv(csv_path, index=False)

    # Plot PNG (save, optionally show)
    png_path = out_dir / f"{safe_site}_{yr0}_{yr1}_kikwi.png"
    plt.figure(figsize=(14, 7))

    # Solar lines
    for tag in SEASONS:
        if compute_sunset:
            plt.plot(df["Year"], df[f"{tag}_Sunset_Az"], label=f"{tag} (Sunset)")
        if compute_sunrise:
            plt.plot(df["Year"], df[f"{tag}_Sunrise_Az"], label=f"{tag} (Sunrise)")

    # Lunar rails
    if include_lunar:
        plt.plot(df["Year"], df["Lunar_Major_North_Sunset_Az"], linestyle="--", linewidth=1.6, label="Lunar Major Standstill (N)")
        plt.plot(df["Year"], df["Lunar_Major_South_Sunset_Az"], linestyle="--", linewidth=1.6, label="Lunar Major Standstill (S)")
        plt.plot(df["Year"], df["Lunar_Minor_North_Sunset_Az"], linestyle=":",  linewidth=1.2, label="Lunar Minor Standstill (N)")
        plt.plot(df["Year"], df["Lunar_Minor_South_Sunset_Az"], linestyle=":",  linewidth=1.2, label="Lunar Minor Standstill (S)")

    plt.xlabel("Year")
    plt.ylabel("Azimuth (° from North)")
    mode = "SUNSET" if compute_sunset and not compute_sunrise else "SUNRISE/SUNSET"
    plt.title(
        f"{site_name} — Seasonal {mode} + Lunar Standstill Azimuths\n"
        f"lat {lat:.2f}°, elev {elev:.0f} m • Cross-quarter markers: Feb/May/Aug/Nov (midpoints)"
    )
    plt.grid(True)
    plt.legend(loc="center left", bbox_to_anchor=(1, 0.5))
    plt.tight_layout()
    plt.savefig(png_path, dpi=200, bbox_inches="tight")
    if show_plot:
        plt.show()
    plt.close()

    return {"csv": csv_path, "png": png_path}
