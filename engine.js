// Nestbox math engine - pure arithmetic, shared by the page and the tests.
// Every borrowed number is a labeled nest-box norm, not a rule.
(function (root) {
"use strict";

// Labeled norms (common nest-box references):
// - Entrance hole ranges by species (mm): blue tit 25-28, wren 26-30, great tit 28-32,
//   tree sparrow 28-32, house sparrow 32-38, nuthatch 32-35, starling 45-48.
// - Box size: tits want about a 10-12 cm floor and 20 cm depth; up to 14 cm suits sparrows and nuthatches;
//   14 cm and up is starling-sized.
var SPECIES = [
  { name: "blue tit", min: 25, max: 28 },
  { name: "wren", min: 26, max: 30 },
  { name: "great tit", min: 28, max: 32 },
  { name: "tree sparrow", min: 28, max: 32 },
  { name: "house sparrow", min: 32, max: 38 },
  { name: "nuthatch", min: 32, max: 35 },
  { name: "starling", min: 45, max: 48 }
];

function r1(x) { return Math.round(x * 10) / 10; }
function positive() {
  for (var i = 0; i < arguments.length; i++) {
    var v = arguments[i];
    if (typeof v !== "number" || !isFinite(v) || v <= 0) return false;
  }
  return true;
}

function holeMatch(holeMm) {
  if (!positive(holeMm)) return { error: "hole size must be positive" };
  var matches = [];
  for (var i = 0; i < SPECIES.length; i++) {
    var s = SPECIES[i];
    if (holeMm >= s.min && holeMm <= s.max) matches.push(s.name + " (" + s.min + "-" + s.max + ")");
  }
  return { holeMm: r1(holeMm), matches: matches };
}

function renderHole(r) {
  if (r.error) return r.error;
  if (r.matches.length === 0) {
    return "No labeled species takes a " + r.holeMm + " mm hole - under 25 mm excludes garden birds, over 48 mm invites more than starlings (labeled nest-box ranges).";
  }
  return "A " + r.holeMm + " mm hole suits: " + r.matches.join(", ") + " - labeled nest-box ranges.";
}

function boxCheck(floorCm, heightCm) {
  if (!positive(floorCm, heightCm)) return { error: "box dimensions must be positive" };
  var verdict;
  if (floorCm < 10 || heightCm < 20) {
    verdict = "too small for labeled tit boxes (10 cm floor, 20 cm depth)";
  } else if (floorCm <= 12) {
    verdict = "fits blue tit and great tit boxes (labeled 10-12 cm floors)";
  } else if (floorCm <= 14) {
    verdict = "fits sparrows and nuthatches (labeled up to 14 cm floors)";
  } else {
    verdict = "starling-sized or bigger (labeled 14 cm and up)";
  }
  return { floorCm: r1(floorCm), heightCm: r1(heightCm), verdict: verdict };
}

function renderBox(r) {
  if (r.error) return r.error;
  return "A " + r.floorCm + " cm floor with " + r.heightCm + " cm depth: " + r.verdict + ".";
}

function sheetBoxes(sheetW, sheetL, boxW, boxD, boxH) {
  if (!positive(sheetW, sheetL)) return { error: "sheet dimensions must be positive" };
  if (!positive(boxW, boxD, boxH)) return { error: "box dimensions must be positive" };
  var boxArea = r1(2 * boxW * boxH + 2 * boxD * boxH + 2 * boxW * boxD);
  var sheetArea = r1(sheetW * sheetL);
  var boxes = Math.floor(sheetArea / boxArea);
  if (boxes < 1) return { error: "sheet is too small for one box" };
  return { sheetArea: sheetArea, boxArea: boxArea, boxes: boxes, boxW: r1(boxW), boxD: r1(boxD), boxH: r1(boxH) };
}

function renderSheet(r) {
  if (r.error) return r.error;
  return "The sheet holds about " + r.boxes + " simple box" + (r.boxes === 1 ? "" : "es") + " of " +
    r.boxW + " x " + r.boxD + " x " + r.boxH + " cm by area (" + r.boxArea + " cm2 each) - labeled estimate, saw kerfs and layout eat a few.";
}

var api = {
  holeMatch: holeMatch,
  boxCheck: boxCheck,
  sheetBoxes: sheetBoxes,
  renderHole: renderHole,
  renderBox: renderBox,
  renderSheet: renderSheet
};
if (typeof module !== "undefined" && module.exports) module.exports = api;
root.NestboxMath = api;
})(typeof window !== "undefined" ? window : globalThis);
