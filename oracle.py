#!/usr/bin/env python3
"""Independent oracle for Nestbox math. Mirrors engine.js float ops exactly."""
import json, math

SPECIES = [
    ("blue tit", 25, 28), ("wren", 26, 30), ("great tit", 28, 32), ("tree sparrow", 28, 32),
    ("house sparrow", 32, 38), ("nuthatch", 32, 35), ("starling", 45, 48),
]

def r1(x): return math.floor(x * 10 + 0.5) / 10

def num(x):
    if x == int(x) and abs(x) < 1e15:
        return str(int(x))
    return repr(x)

def hole_match(hole_mm):
    if not (isinstance(hole_mm, (int, float)) and math.isfinite(hole_mm) and hole_mm > 0):
        return {"error": "hole size must be positive"}
    matches = [f"{n} ({lo}-{hi})" for n, lo, hi in SPECIES if lo <= hole_mm <= hi]
    return {"holeMm": r1(hole_mm), "matches": matches}

def render_hole(r):
    if "error" in r: return r["error"]
    if not r["matches"]:
        return (f"No labeled species takes a {num(r['holeMm'])} mm hole - under 25 mm excludes garden birds, "
                "over 48 mm invites more than starlings (labeled nest-box ranges).")
    return f"A {num(r['holeMm'])} mm hole suits: {', '.join(r['matches'])} - labeled nest-box ranges."

def box_check(floor_cm, height_cm):
    if not all(isinstance(v, (int, float)) and math.isfinite(v) and v > 0 for v in (floor_cm, height_cm)):
        return {"error": "box dimensions must be positive"}
    if floor_cm < 10 or height_cm < 20:
        verdict = "too small for labeled tit boxes (10 cm floor, 20 cm depth)"
    elif floor_cm <= 12:
        verdict = "fits blue tit and great tit boxes (labeled 10-12 cm floors)"
    elif floor_cm <= 14:
        verdict = "fits sparrows and nuthatches (labeled up to 14 cm floors)"
    else:
        verdict = "starling-sized or bigger (labeled 14 cm and up)"
    return {"floorCm": r1(floor_cm), "heightCm": r1(height_cm), "verdict": verdict}

def render_box(r):
    if "error" in r: return r["error"]
    return f"A {num(r['floorCm'])} cm floor with {num(r['heightCm'])} cm depth: {r['verdict']}."

def sheet_boxes(sheet_w, sheet_l, box_w, box_d, box_h):
    if not all(isinstance(v, (int, float)) and math.isfinite(v) and v > 0 for v in (sheet_w, sheet_l)):
        return {"error": "sheet dimensions must be positive"}
    if not all(isinstance(v, (int, float)) and math.isfinite(v) and v > 0 for v in (box_w, box_d, box_h)):
        return {"error": "box dimensions must be positive"}
    box_area = r1(2 * box_w * box_h + 2 * box_d * box_h + 2 * box_w * box_d)
    sheet_area = r1(sheet_w * sheet_l)
    boxes = math.floor(sheet_area / box_area)
    if boxes < 1:
        return {"error": "sheet is too small for one box"}
    return {"sheetArea": sheet_area, "boxArea": box_area, "boxes": boxes,
            "boxW": r1(box_w), "boxD": r1(box_d), "boxH": r1(box_h)}

def render_sheet(r):
    if "error" in r: return r["error"]
    s = "" if r["boxes"] == 1 else "es"
    return (f"The sheet holds about {r['boxes']} simple box{s} of {num(r['boxW'])} x {num(r['boxD'])} x "
            f"{num(r['boxH'])} cm by area ({num(r['boxArea'])} cm2 each) - labeled estimate, saw kerfs and layout eat a few.")

cases = []
for mm in [32, 27, 50, 25, 28, 30, 38, 45, 48, 20, 24.9, 33.5, 0, -5, 46]:
    res = hole_match(mm)
    cases.append({"fn": "holeMatch", "args": [mm], "result": res, "render": render_hole(res)})
for f, h in [(11, 25), (14, 25), (9, 25), (12, 20), (15, 30), (10, 18), (12.5, 22),
             (13.9, 25), (20, 40), (0, 25), (11, 0), (10, 19.9)]:
    res = box_check(f, h)
    cases.append({"fn": "boxCheck", "args": [f, h], "result": res, "render": render_box(res)})
for sw, sl, w, d, h in [(122, 244, 12, 12, 25), (60, 120, 12, 12, 25), (100, 200, 14, 14, 30),
                        (50, 100, 10, 10, 20), (200, 300, 15, 12, 28), (30, 40, 12, 12, 25),
                        (0, 244, 12, 12, 25), (122, -5, 12, 12, 25), (122, 244, 0, 12, 25),
                        (122, 244, 12, 12, 0), (80, 160, 11, 11, 22)]:
    res = sheet_boxes(sw, sl, w, d, h)
    cases.append({"fn": "sheetBoxes", "args": [sw, sl, w, d, h], "result": res, "render": render_sheet(res)})

with open("expected.json", "w") as f:
    json.dump(cases, f, separators=(",", ":"))
    f.write("\n")
print(len(cases), "cases written")
