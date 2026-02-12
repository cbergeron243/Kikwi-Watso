#kikwi_cli.py
KikwiNok CLI (Command Line Interface)
------------------------------------
Runs the KikwiNok core engine (kikwi_core.run_kikwi) from the terminal.

Examples:
  python kikwi_cli.py --site "Turtle Mound, Andover, MA" --lat 42.38 --elev 125 --start -10000 --end 2000 --out "KikwiNok_Output"
  python kikwi_cli.py   # interactive prompts
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from kikwi_core import run_kikwi


def _prompt_float(label: str, default: float | None = None) -> float:
    while True:
        suffix = f" [{default}]" if default is not None else ""
        raw = input(f"{label}{suffix}: ").strip()
        if raw == "" and default is not None:
            return float(default)
        try:
            return float(raw)
        except ValueError:
            print("Please enter a valid number.")


def _prompt_int(label: str, default: int | None = None) -> int:
    while True:
        suffix = f" [{default}]" if default is not None else ""
        raw = input(f"{label}{suffix}: ").strip()
        if raw == "" and default is not None:
            return int(default)
        try:
            return int(raw)
        except ValueError:
            print("Please enter a valid integer.")


def _prompt_yes_no(label: str, default: bool = True) -> bool:
    d = "Y/n" if default else "y/N"
    while True:
        raw = input(f"{label} ({d}): ").strip().lower()
        if raw == "":
            return default
        if raw in ("y", "yes"):
            return True
        if raw in ("n", "no"):
            return False
        print("Please enter y or n.")


def parse_args(argv: list[str]) -> argparse.Namespace:
    p = argparse.ArgumentParser(
        prog="kikwi_cli",
        description="KikwiNok — Seasonal Azimuth Explorer (CLI)",
    )

    p.add_argument("--site", default=None, help="Site name for output filenames/title")
    p.add_argument("--lat", type=float, default=None, help="Latitude in degrees (North positive)")
    p.add_argument("--elev", type=float, default=None, help="Observer elevation in meters")
    p.add_argument("--start", type=int, default=None, help="Start year (e.g. -10000)")
    p.add_argument("--end", type=int, default=None, help="End year (e.g. 2000)")
    p.add_argument("--out", default=None, help="Output folder path")

    # Options matching kikwi_gui
    p.add_argument("--lunar", dest="include_lunar", action="store_true", help="Include lunar standstill rails (default)")
    p.add_argument("--no-lunar", dest="include_lunar", action="store_false", help="Disable lunar standstill rails")
    p.set_defaults(include_lunar=True)

    p.add_argument("--sunset", dest="compute_sunset", action="store_true", help="Compute SUNSET series (default)")
    p.add_argument("--no-sunset", dest="compute_sunset", action="store_false", help="Disable SUNSET series")
    p.set_defaults(compute_sunset=True)

    p.add_argument("--sunrise", dest="compute_sunrise", action="store_true", help="Compute SUNRISE series")
    p.add_argument("--no-sunrise", dest="compute_sunrise", action="store_false", help="Disable SUNRISE series (default)")
    p.set_defaults(compute_sunrise=False)

    p.add_argument("--show", dest="show_plot", action="store_true", help="Show plot window after saving PNG")
    p.add_argument("--no-show", dest="show_plot", action="store_false", help="Do not show plot window (default)")
    p.set_defaults(show_plot=False)

    return p.parse_args(argv)


def interactive_fill(ns: argparse.Namespace) -> argparse.Namespace:
    print("\nKikwiNok CLI — interactive mode\n(Press Enter to accept defaults where shown)\n")

    site_default = ns.site or "KikwiNok Site"
    ns.site = input(f"Site name [{site_default}]: ").strip() or site_default

    ns.lat = ns.lat if ns.lat is not None else _prompt_float("Latitude (°)", None)
    ns.elev = ns.elev if ns.elev is not None else _prompt_float("Elevation (m)", 0.0)
    ns.start = ns.start if ns.start is not None else _prompt_int("Start year", -10000)
    ns.end = ns.end if ns.end is not None else _prompt_int("End year", 2000)

    out_default = ns.out or str(Path.cwd() / "KikwiNok_Output")
    ns.out = input(f"Output folder [{out_default}]: ").strip() or out_default

    # Only ask these if user didn't explicitly set flags (best-effort)
    ns.include_lunar = _prompt_yes_no("Include lunar standstill rails?", ns.include_lunar)
    ns.compute_sunset = _prompt_yes_no("Compute SUNSET?", ns.compute_sunset)
    ns.compute_sunrise = _prompt_yes_no("Compute SUNRISE?", ns.compute_sunrise)
    ns.show_plot = _prompt_yes_no("Show plot window after saving?", ns.show_plot)

    print()
    return ns


def main(argv: list[str]) -> int:
    ns = parse_args(argv)

    # If missing required core inputs, fall back to interactive
    missing = any(
        v is None
        for v in (ns.site, ns.lat, ns.elev, ns.start, ns.end, ns.out)
    )
    if missing:
        ns = interactive_fill(ns)

    out_dir = Path(ns.out).expanduser()

    try:
        outputs = run_kikwi(
            lat=float(ns.lat),
            elev=float(ns.elev),
            yr0=int(ns.start),
            yr1=int(ns.end),
            site_name=str(ns.site),
            include_lunar=bool(ns.include_lunar),
            compute_sunset=bool(ns.compute_sunset),
            compute_sunrise=bool(ns.compute_sunrise),
            out_dir=out_dir,
            show_plot=bool(ns.show_plot),
        )
    except Exception as e:
        print(f"ERROR: {e}")
        return 1

    print("✅ Done!")
    print(f"CSV: {outputs['csv']}")
    print(f"PNG: {outputs['png']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
