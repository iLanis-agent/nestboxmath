# Nestbox math

Nest box planning for the birds you actually want. A static site with three calculators:

- **Hole match** - entrance-hole millimeters become the species that fit through, from labeled ranges.
- **Box check** - interior floor and depth become a size verdict by bird.
- **Sheet yield** - sheet dimensions become a box count by area, with the kerf caveat attached.

Live site: https://ilanis-agent.github.io/nestboxmath/

## Labeled norms

Labeled nest-box references, not rules:

- Hole ranges (mm): blue tit 25-28, wren 26-30, great tit 28-32, tree sparrow 28-32, house sparrow 32-38, nuthatch 32-35, starling 45-48.
- Boxes: tits want about a 10-12 cm floor and 20 cm depth; up to 14 cm suits sparrows and nuthatches; 14 and up is starling-sized.
- Sheet yield is an area estimate - saw kerfs and layout eat a few.

## Layout

- `engine.js` - pure arithmetic and text rendering, shared by the page and the tests.
- `index.html` - landing page. `app.html` - the calculators.
- `oracle.py` - independent Python mirror of the engine's exact float operations.
- `expected.json` - 38 oracle-generated cases. `test.js` - runs every case against the engine plus render checks.

## Tests

```
python3 oracle.py   # regenerate expected.json
node test.js        # 114 checks, 0 failures
```
