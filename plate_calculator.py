"""
Day 1: Barbell Plate Calculator
Workout Tracker Suite — Visual plate loader with saved lifts
"""

import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import json
from pathlib import Path

# ─────────────────────────── CONSTANTS ───────────────────────────

SAVED_LIFTS_FILE = Path(__file__).parent / "saved_lifts.json"

BAR_WEIGHTS = {
    "Standard (20kg / 45lbs)": {"kg": 20, "lbs": 45},
    "Women's Bar (15kg / 35lbs)": {"kg": 15, "lbs": 35},
    "Ez-Curl Bar (10kg / 25lbs)": {"kg": 10, "lbs": 25},
    "No Bar (0kg / 0lbs)": {"kg": 0, "lbs": 0},
}

PLATES_LBS = [45, 35, 25, 10, 5, 2.5]
PLATES_KG  = [25, 20, 15, 10, 5, 2.5, 1.25]

PLATE_COLORS_LBS = {
    45:  "#E53935",   # red
    35:  "#FDD835",   # yellow
    25:  "#43A047",   # green
    10:  "#E0E0E0",   # white/light-grey
    5:   "#1E88E5",   # blue
    2.5: "#C62828",   # small red
}

PLATE_COLORS_KG = {
    25:   "#E53935",
    20:   "#1E88E5",
    15:   "#FDD835",
    10:   "#43A047",
    5:    "#F5F5F5",
    2.5:  "#C62828",
    1.25: "#3949AB",
}

PLATE_HEIGHT_LBS = {
    45: 110, 35: 95, 25: 80, 10: 60, 5: 50, 2.5: 38,
}
PLATE_HEIGHT_KG = {
    25: 110, 20: 95, 15: 80, 10: 65, 5: 50, 2.5: 38, 1.25: 28,
}

PLATE_WIDTH_LBS = {
    45: 22, 35: 20, 25: 18, 10: 14, 5: 12, 2.5: 9,
}
PLATE_WIDTH_KG = {
    25: 22, 20: 20, 15: 18, 10: 14, 5: 12, 2.5: 9, 1.25: 7,
}

PRESETS_LBS = [
    ("Empty Bar", 45),
    ("Warm-up (95)", 95),
    ("135 lbs", 135),
    ("185 lbs", 185),
    ("225 lbs", 225),
    ("275 lbs", 275),
    ("315 lbs", 315),
    ("405 lbs", 405),
]

PRESETS_KG = [
    ("Empty Bar", 20),
    ("Warm-up (60)", 60),
    ("100 kg", 100),
    ("120 kg", 120),
    ("140 kg", 140),
    ("160 kg", 160),
    ("180 kg", 180),
    ("200 kg", 200),
]

# ─────────────────────────── ALGORITHM ───────────────────────────

def calculate_plates(target_weight: float, bar_weight: float, plates: list[float]):
    """
    Greedy plate calculator.
    Returns list of (plate_weight, count) tuples for ONE side.
    Also returns the actual achievable weight.
    """
    if target_weight <= bar_weight:
        return [], bar_weight

    plates_total = target_weight - bar_weight
    # Round to nearest achievable increment (smallest plate × 2)
    increment = min(plates) * 2
    plates_total = round(plates_total / increment) * increment
    actual_weight = plates_total + bar_weight

    weight_per_side = plates_total / 2
    remaining = weight_per_side
    result = []

    for plate in sorted(plates, reverse=True):
        count = int(remaining / plate + 1e-9)  # tiny epsilon avoids float errors
        if count > 0:
            result.append((plate, count))
            remaining -= plate * count
            remaining = round(remaining, 6)

    return result, actual_weight


# ─────────────────────────── PERSISTENCE ─────────────────────────

def load_lifts() -> dict:
    if SAVED_LIFTS_FILE.exists():
        with open(SAVED_LIFTS_FILE, "r") as f:
            return json.load(f)
    return {}


def save_lift(name: str, weight: float, unit: str):
    lifts = load_lifts()
    lifts[name] = {"weight": weight, "unit": unit}
    with open(SAVED_LIFTS_FILE, "w") as f:
        json.dump(lifts, f, indent=2)


def delete_lift(name: str):
    lifts = load_lifts()
    lifts.pop(name, None)
    with open(SAVED_LIFTS_FILE, "w") as f:
        json.dump(lifts, f, indent=2)


# ─────────────────────────── MAIN APP ────────────────────────────

class BarbellCalculatorApp:
    # ── Colours / fonts ──────────────────────────────────────────
    BG        = "#1A1A2E"
    PANEL     = "#16213E"
    ACCENT    = "#E94560"
    ACCENT2   = "#0F3460"
    TEXT      = "#EAEAEA"
    TEXT_DIM  = "#8899AA"
    BAR_COLOR = "#607D8B"
    COLLAR    = "#90A4AE"
    FONT_H1   = ("Helvetica", 22, "bold")
    FONT_H2   = ("Helvetica", 13, "bold")
    FONT_BODY = ("Helvetica", 11)
    FONT_SM   = ("Helvetica", 9)

    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("🏋️  Barbell Plate Calculator")
        self.root.configure(bg=self.BG)
        self.root.resizable(True, True)
        self.root.minsize(900, 640)

        # State
        self.unit_var      = tk.StringVar(value="lbs")
        self.bar_var       = tk.StringVar(value="Standard (20kg / 45lbs)")
        self.weight_var    = tk.StringVar(value="135")
        self.actual_weight = 0.0
        self.plates_result = []

        self._build_ui()
        self._update()

    # ── UI Construction ──────────────────────────────────────────

    def _build_ui(self):
        # Title bar
        title_bar = tk.Frame(self.root, bg=self.ACCENT, height=5)
        title_bar.pack(fill="x")

        header = tk.Frame(self.root, bg=self.BG, pady=10)
        header.pack(fill="x", padx=20)
        tk.Label(header, text="🏋️  BARBELL PLATE CALCULATOR",
                 font=self.FONT_H1, fg=self.ACCENT, bg=self.BG).pack(side="left")
        tk.Label(header, text="Workout Tracker Suite — Day 1",
                 font=self.FONT_SM, fg=self.TEXT_DIM, bg=self.BG).pack(side="right", anchor="s", pady=6)

        # Main layout: left controls | right canvas
        body = tk.Frame(self.root, bg=self.BG)
        body.pack(fill="both", expand=True, padx=14, pady=(0, 14))

        self._build_controls(body)
        self._build_canvas_panel(body)

    def _build_controls(self, parent):
        ctrl = tk.Frame(parent, bg=self.PANEL, bd=0, relief="flat", width=300)
        ctrl.pack(side="left", fill="y", padx=(0, 10), pady=4)
        ctrl.pack_propagate(False)

        pad = {"padx": 16, "pady": 6}

        # ── Unit toggle ──
        self._section_label(ctrl, "UNIT")
        unit_row = tk.Frame(ctrl, bg=self.PANEL)
        unit_row.pack(fill="x", **pad)
        for u in ("lbs", "kg"):
            b = tk.Radiobutton(
                unit_row, text=u.upper(), variable=self.unit_var, value=u,
                command=self._on_unit_change,
                bg=self.PANEL, fg=self.TEXT, selectcolor=self.ACCENT2,
                activebackground=self.PANEL, activeforeground=self.ACCENT,
                font=self.FONT_H2, indicator=0, relief="flat",
                padx=14, pady=6, cursor="hand2",
            )
            b.pack(side="left", padx=(0, 6))

        # ── Bar weight ──
        self._section_label(ctrl, "BAR TYPE")
        bar_menu = ttk.Combobox(
            ctrl, textvariable=self.bar_var,
            values=list(BAR_WEIGHTS.keys()),
            state="readonly", font=self.FONT_BODY,
        )
        bar_menu.pack(fill="x", **pad)
        bar_menu.bind("<<ComboboxSelected>>", lambda _: self._update())
        self._style_combobox()

        # ── Target weight ──
        self._section_label(ctrl, "TARGET WEIGHT")
        weight_frame = tk.Frame(ctrl, bg=self.PANEL)
        weight_frame.pack(fill="x", **pad)

        self.weight_entry = tk.Entry(
            weight_frame, textvariable=self.weight_var,
            font=("Helvetica", 20, "bold"), width=8,
            bg=self.ACCENT2, fg=self.ACCENT, insertbackground=self.ACCENT,
            relief="flat", bd=8, justify="center",
        )
        self.weight_entry.pack(side="left", fill="x", expand=True)
        self.weight_entry.bind("<KeyRelease>", lambda _: self._update())

        self.unit_label = tk.Label(
            weight_frame, text="LBS", font=self.FONT_H2,
            fg=self.TEXT_DIM, bg=self.PANEL, padx=6,
        )
        self.unit_label.pack(side="left")

        # Increment buttons
        inc_row = tk.Frame(ctrl, bg=self.PANEL)
        inc_row.pack(fill="x", padx=16, pady=(0, 4))
        for delta in (-5, -2.5, +2.5, +5):
            label = f"{'−' if delta < 0 else '+'}{abs(delta)}"
            tk.Button(
                inc_row, text=label, font=self.FONT_SM,
                bg=self.ACCENT2, fg=self.TEXT, relief="flat",
                activebackground=self.ACCENT, activeforeground="white",
                cursor="hand2", padx=6, pady=3,
                command=lambda d=delta: self._increment(d),
            ).pack(side="left", padx=2)

        # ── Result display ──
        self._section_label(ctrl, "RESULT")
        self.result_frame = tk.Frame(ctrl, bg=self.ACCENT2, bd=0)
        self.result_frame.pack(fill="x", padx=16, pady=6)
        self.actual_label = tk.Label(
            self.result_frame, text="—",
            font=("Helvetica", 18, "bold"), fg=self.ACCENT, bg=self.ACCENT2, pady=8,
        )
        self.actual_label.pack()
        self.plates_label = tk.Label(
            self.result_frame, text="Enter a weight above",
            font=self.FONT_SM, fg=self.TEXT_DIM, bg=self.ACCENT2,
            wraplength=240, justify="left", pady=4, padx=10,
        )
        self.plates_label.pack(fill="x")

        # ── Presets ──
        self._section_label(ctrl, "QUICK PRESETS")
        self.preset_frame = tk.Frame(ctrl, bg=self.PANEL)
        self.preset_frame.pack(fill="x", padx=12, pady=(0, 6))
        self._build_presets()

        # ── Saved lifts ──
        self._section_label(ctrl, "SAVED LIFTS")
        save_btn = tk.Button(
            ctrl, text="💾  Save Current",
            font=self.FONT_BODY, bg=self.ACCENT, fg="white",
            relief="flat", cursor="hand2", pady=6,
            activebackground="#C62828", activeforeground="white",
            command=self._save_current,
        )
        save_btn.pack(fill="x", padx=16, pady=(0, 6))

        self.saved_frame = tk.Frame(ctrl, bg=self.PANEL)
        self.saved_frame.pack(fill="x", padx=12)
        self._refresh_saved_list()

    def _build_canvas_panel(self, parent):
        right = tk.Frame(parent, bg=self.BG)
        right.pack(side="left", fill="both", expand=True)

        self._section_label(right, "BARBELL VISUALISER", pad_top=0)

        canvas_bg = tk.Frame(right, bg=self.PANEL, bd=0)
        canvas_bg.pack(fill="both", expand=True, pady=4)

        self.canvas = tk.Canvas(
            canvas_bg, bg=self.PANEL, highlightthickness=0,
        )
        self.canvas.pack(fill="both", expand=True, padx=8, pady=8)
        self.canvas.bind("<Configure>", lambda _: self._draw_barbell())

    # ── Helper builders ──────────────────────────────────────────

    def _section_label(self, parent, text, pad_top=8):
        tk.Label(
            parent, text=text, font=("Helvetica", 9, "bold"),
            fg=self.ACCENT, bg=parent.cget("bg"),
            anchor="w", padx=16,
        ).pack(fill="x", pady=(pad_top, 2))

    def _style_combobox(self):
        style = ttk.Style()
        style.theme_use("clam")
        style.configure(
            "TCombobox",
            fieldbackground=self.ACCENT2,
            background=self.ACCENT2,
            foreground=self.TEXT,
            arrowcolor=self.ACCENT,
            borderwidth=0,
        )

    def _build_presets(self):
        for w in self.preset_frame.winfo_children():
            w.destroy()
        presets = PRESETS_LBS if self.unit_var.get() == "lbs" else PRESETS_KG
        for name, weight in presets:
            tk.Button(
                self.preset_frame, text=name, font=self.FONT_SM,
                bg="#0F2040", fg=self.TEXT, relief="flat",
                cursor="hand2", padx=6, pady=4, anchor="w",
                activebackground=self.ACCENT, activeforeground="white",
                command=lambda w=weight: self._set_weight(w),
            ).pack(fill="x", pady=1)

    def _refresh_saved_list(self):
        for w in self.saved_frame.winfo_children():
            w.destroy()
        lifts = load_lifts()
        if not lifts:
            tk.Label(self.saved_frame, text="No saved lifts yet.",
                     font=self.FONT_SM, fg=self.TEXT_DIM, bg=self.PANEL).pack(pady=4)
            return
        for name, data in lifts.items():
            row = tk.Frame(self.saved_frame, bg=self.PANEL)
            row.pack(fill="x", pady=1)
            tk.Button(
                row,
                text=f"  {name}  ({data['weight']} {data['unit']})",
                font=self.FONT_SM, bg="#0F2040", fg=self.TEXT,
                relief="flat", cursor="hand2", anchor="w", padx=6, pady=3,
                activebackground=self.ACCENT2, activeforeground=self.TEXT,
                command=lambda d=data, n=name: self._load_lift(d),
            ).pack(side="left", fill="x", expand=True)
            tk.Button(
                row, text="✕", font=self.FONT_SM,
                bg="#0F2040", fg=self.ACCENT,
                relief="flat", cursor="hand2", padx=4,
                activebackground="#C62828", activeforeground="white",
                command=lambda n=name: self._delete_lift(n),
            ).pack(side="right")

    # ── Events ───────────────────────────────────────────────────

    def _on_unit_change(self):
        self.unit_label.config(text=self.unit_var.get().upper())
        self._build_presets()
        self._update()

    def _increment(self, delta):
        try:
            val = float(self.weight_var.get()) + delta
            self.weight_var.set(str(max(0, val)))
            self._update()
        except ValueError:
            pass

    def _set_weight(self, weight):
        self.weight_var.set(str(weight))
        self._update()

    def _save_current(self):
        try:
            w = float(self.weight_var.get())
        except ValueError:
            messagebox.showwarning("Invalid Weight", "Enter a valid weight first.")
            return
        name = simpledialog.askstring(
            "Save Lift", "Name this lift:",
            initialvalue=f"My Lift ({w} {self.unit_var.get()})",
            parent=self.root,
        )
        if name and name.strip():
            save_lift(name.strip(), w, self.unit_var.get())
            self._refresh_saved_list()

    def _load_lift(self, data):
        self.weight_var.set(str(data["weight"]))
        self.unit_var.set(data["unit"])
        self.unit_label.config(text=data["unit"].upper())
        self._build_presets()
        self._update()

    def _delete_lift(self, name):
        if messagebox.askyesno("Delete", f'Delete saved lift "{name}"?'):
            delete_lift(name)
            self._refresh_saved_list()

    # ── Core update ──────────────────────────────────────────────

    def _update(self):
        unit    = self.unit_var.get()
        bar_key = self.bar_var.get()
        bar_w   = BAR_WEIGHTS[bar_key][unit]
        plates  = PLATES_LBS if unit == "lbs" else PLATES_KG

        try:
            target = float(self.weight_var.get())
        except ValueError:
            self.actual_label.config(text="—")
            self.plates_label.config(text="Enter a valid number above.")
            self.canvas.delete("all")
            return

        self.plates_result, self.actual_weight = calculate_plates(target, bar_w, plates)

        # Result label
        self.actual_label.config(text=f"{self.actual_weight} {unit}")

        if not self.plates_result:
            if target <= bar_w:
                self.plates_label.config(text="Empty bar — no plates needed.")
            else:
                self.plates_label.config(text="Cannot be achieved with available plates.")
        else:
            lines = [f"Per side:"]
            for pw, cnt in self.plates_result:
                lines.append(f"  {cnt} × {pw} {unit}")
            total_side = sum(pw * cnt for pw, cnt in self.plates_result)
            lines.append(f"\nTotal per side: {total_side} {unit}")
            self.plates_label.config(text="\n".join(lines))

        self._draw_barbell()

    # ── Drawing ──────────────────────────────────────────────────

    def _draw_barbell(self):
        c = self.canvas
        c.delete("all")
        W = c.winfo_width()
        H = c.winfo_height()
        if W < 10 or H < 10:
            return

        unit   = self.unit_var.get()
        ph     = PLATE_HEIGHT_LBS if unit == "lbs" else PLATE_HEIGHT_KG
        pw_map = PLATE_WIDTH_LBS  if unit == "lbs" else PLATE_WIDTH_KG
        colors = PLATE_COLORS_LBS if unit == "lbs" else PLATE_COLORS_KG

        cx  = W // 2   # centre x
        cy  = H // 2   # centre y (bar axis)
        bar_half  = int(W * 0.40)
        bar_top   = cy - 7
        bar_bot   = cy + 7
        sleeve_h  = 14

        # Shadow
        c.create_rectangle(cx - bar_half + 4, bar_top + 4,
                            cx + bar_half + 4, bar_bot + 4,
                            fill="#0A0A18", outline="")

        # Bar shaft
        c.create_rectangle(cx - bar_half, bar_top,
                            cx + bar_half, bar_bot,
                            fill=self.BAR_COLOR, outline="#455A64", width=1)

        # Knurling marks
        for kx in range(cx - int(bar_half * 0.60), cx + int(bar_half * 0.60), 18):
            c.create_line(kx, bar_top + 2, kx, bar_bot - 2, fill="#455A64", width=1)

        # Centre ring
        c.create_rectangle(cx - 6, bar_top - 2, cx + 6, bar_bot + 2,
                            fill=self.COLLAR, outline="#78909C", width=1)

        # Sleeve indicators (ends)
        for sign in (-1, 1):
            x0 = cx + sign * bar_half - sign * 30
            x1 = cx + sign * bar_half
            c.create_rectangle(x0, cy - sleeve_h, x1, cy + sleeve_h,
                                fill=self.COLLAR, outline="#78909C", width=1)

        # Draw plates both sides
        margin = 4
        for sign, label_sign in ((-1, "LEFT"), (1, "RIGHT")):
            x_cursor = cx + sign * (bar_half - 30)
            for plate_w, count in self.plates_result:
                color  = colors.get(plate_w, "#9E9E9E")
                height = ph.get(plate_w, 60)
                width  = pw_map.get(plate_w, 12)
                for _ in range(count):
                    x0 = x_cursor if sign == 1 else x_cursor - width
                    x1 = x_cursor + width if sign == 1 else x_cursor
                    y0 = cy - height // 2
                    y1 = cy + height // 2

                    # Plate shadow
                    c.create_rectangle(x0 + 2, y0 + 2, x1 + 2, y1 + 2,
                                       fill="#0A0A18", outline="")
                    # Plate body
                    c.create_rectangle(x0, y0, x1, y1,
                                       fill=color, outline="black", width=2)
                    # Highlight stripe
                    stripe_w = max(2, width // 5)
                    c.create_rectangle(
                        x0 + 2, y0 + 4,
                        x0 + stripe_w, y1 - 4,
                        fill=self._lighten(color), outline="",
                    )
                    # Label (rotated text workaround: just show value)
                    label_x = (x0 + x1) / 2
                    label_y = y0 - 14
                    c.create_text(label_x, label_y,
                                  text=str(plate_w), font=("Helvetica", 8, "bold"),
                                  fill=self.TEXT, anchor="center")

                    x_cursor += sign * (width + margin)

        # Weight overlay at top centre
        if self.actual_weight:
            c.create_text(cx, 22,
                          text=f"{self.actual_weight} {unit}",
                          font=("Helvetica", 15, "bold"),
                          fill=self.ACCENT, anchor="center")
            c.create_text(cx, 42,
                          text="loaded on bar",
                          font=("Helvetica", 9),
                          fill=self.TEXT_DIM, anchor="center")

        # Empty bar message
        if not self.plates_result:
            c.create_text(cx, H - 30,
                          text="No plates — just the bar",
                          font=self.FONT_SM, fill=self.TEXT_DIM)

    @staticmethod
    def _lighten(hex_color: str) -> str:
        """Return a slightly lighter shade of a hex color."""
        try:
            r = int(hex_color[1:3], 16)
            g = int(hex_color[3:5], 16)
            b = int(hex_color[5:7], 16)
            r = min(255, r + 50)
            g = min(255, g + 50)
            b = min(255, b + 50)
            return f"#{r:02X}{g:02X}{b:02X}"
        except Exception:
            return hex_color


# ─────────────────────────── ENTRY ───────────────────────────────

def main():
    root = tk.Tk()
    root.geometry("1050x680")
    app = BarbellCalculatorApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()