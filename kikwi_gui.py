#kikwi_gui
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from pathlib import Path

from kikwi_core import run_kikwi

def safe_float(s, name):
    try:
        return float(s)
    except:
        raise ValueError(f"Invalid {name}: {s}")

def safe_int(s, name):
    try:
        return int(s)
    except:
        raise ValueError(f"Invalid {name}: {s}")

def browse_outdir():
    folder = filedialog.askdirectory()
    if folder:
        outdir_var.set(folder)

def on_run():
    try:
        site = site_var.get().strip() or "KikwiNok Site"
        lat  = safe_float(lat_var.get(), "latitude")
        elev = safe_float(elev_var.get(), "elevation (m)")
        yr0  = safe_int(yr0_var.get(), "start year")
        yr1  = safe_int(yr1_var.get(), "end year")

        out_dir = outdir_var.get().strip() or "outputs"
        Path(out_dir).mkdir(parents=True, exist_ok=True)

        results = run_kikwi(
            lat=lat,
            elev=elev,
            yr0=yr0,
            yr1=yr1,
            site_name=site,
            include_lunar=lunar_var.get(),
            compute_sunset=sunset_var.get(),
            compute_sunrise=sunrise_var.get(),
            out_dir=out_dir,
            show_plot=False
        )

        messagebox.showinfo(
            "KikwiNok complete",
            f"Saved files:\n\nPNG: {results['png']}\nCSV: {results['csv']}"
        )

    except Exception as e:
        messagebox.showerror("Error", str(e))

root = tk.Tk()
root.title("KikwiNok — Seasonal Azimuth Explorer")

site_var = tk.StringVar(value="Turtle Mound, Andover, MA")
lat_var  = tk.StringVar(value="42.38")
elev_var = tk.StringVar(value="125")
yr0_var  = tk.StringVar(value="-10000")
yr1_var  = tk.StringVar(value="2000")
outdir_var = tk.StringVar(value=str(Path.home() / "Desktop" / "KikwiNok_Outputs"))

lunar_var   = tk.BooleanVar(value=True)
sunset_var  = tk.BooleanVar(value=True)
sunrise_var = tk.BooleanVar(value=False)

frm = ttk.Frame(root, padding=12)
frm.grid()

def row(label, var, r):
    ttk.Label(frm, text=label).grid(column=0, row=r, sticky="w", pady=3)
    ttk.Entry(frm, textvariable=var, width=28).grid(column=1, row=r, sticky="w", pady=3)

row("Site name", site_var, 0)
row("Latitude (°)", lat_var, 1)
row("Elevation (m)", elev_var, 2)
row("Start year", yr0_var, 3)
row("End year", yr1_var, 4)

ttk.Label(frm, text="Output folder").grid(column=0, row=5, sticky="w", pady=3)
ttk.Entry(frm, textvariable=outdir_var, width=28).grid(column=1, row=5, sticky="w", pady=3)
ttk.Button(frm, text="Browse", command=browse_outdir).grid(column=2, row=5, padx=6)

ttk.Checkbutton(frm, text="Include lunar standstill rails", variable=lunar_var).grid(column=0, row=6, columnspan=3, sticky="w", pady=6)
ttk.Checkbutton(frm, text="Compute SUNSET", variable=sunset_var).grid(column=0, row=7, sticky="w")
ttk.Checkbutton(frm, text="Compute SUNRISE", variable=sunrise_var).grid(column=1, row=7, sticky="w")

ttk.Button(frm, text="Run KikwiNok", command=on_run).grid(column=0, row=8, columnspan=3, pady=12, sticky="we")

root.mainloop()
