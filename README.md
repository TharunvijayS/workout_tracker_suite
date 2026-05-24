# 🏋️ Day 1 — Barbell Plate Calculator

Part of the **Workout Tracker Suite** series.

## How to Run

```bash
cd day1_plate_calculator
python plate_calculator.py
```

No installations needed — uses Python standard library only (Tkinter is built-in).

## Features

| Feature | Details |
|---|---|
| Unit toggle | Switch between **lbs** and **kg** instantly |
| Bar selector | Standard 45 lb / Women's 35 lb / Ez-Curl 25 lb / No bar |
| Target weight | Type any weight; real-time visual updates |
| ± buttons | Nudge weight by 2.5 or 5 increments |
| Quick presets | One-click common weights (135, 225, 315…) |
| Visual barbell | Color-coded plates drawn on canvas |
| Save lifts | Name & persist your favourite weights to `saved_lifts.json` |
| Load / delete | Restore or remove any saved lift |

## Plate Colors

### lbs
| Plate | Color |
|---|---|
| 45 lbs | 🔴 Red |
| 35 lbs | 🟡 Yellow |
| 25 lbs | 🟢 Green |
| 10 lbs | ⚪ White |
| 5 lbs  | 🔵 Blue |
| 2.5 lbs | 🔴 Small Red |

### kg
| Plate | Color |
|---|---|
| 25 kg | 🔴 Red |
| 20 kg | 🔵 Blue |
| 15 kg | 🟡 Yellow |
| 10 kg | 🟢 Green |
| 5 kg  | ⚪ White |
| 2.5 kg | 🔴 Small Red |
| 1.25 kg | 🔵 Small Indigo |

## Files

```
day1_plate_calculator/
├── plate_calculator.py   ← Main app (run this)
├── saved_lifts.json      ← Auto-created when you save a lift
└── README.md             ← This file
```

## Algorithm

Uses a **greedy approach**: loads largest plates first, then fills remaining weight with progressively smaller plates. Target is rounded to the nearest achievable increment (smallest plate × 2) before calculation.

## Coming Next

- **Day 2**: Workout Logger — log sets/reps/weight to a local database
- **Day 3**: Progress Dashboard — visualise your strength gains over time