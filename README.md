# Southwest Livery Govee Schemes

Govee H618C LED strip color schemes for each Southwest special-livery jet in the
[jaysplanes](https://github.com/mark-winters/jaysplanes) game. Contrail colors come
straight from `web/src/game/core/liveries.ts` there.

## Files
- `index.json` — all planes (slug, name, registration, contrail hexes, file).
- `schemes/<slug>.json` — one scheme per plane; validated by `scheme.schema.json`.
- `play.py` — sends a scheme to a strip over the Govee LAN API.

## Scheme format
- `contrail`: the game's contrail colors (hex).
- `primary`: static color + brightness for a "just show this plane" state.
- `steps`: ordered, looped. Each step sets `color` (rgb) and `brightness` (1-100), then holds `holdMs`.
  The H618C fades color/brightness changes, so steps cross-fade naturally.
  - `pulse` (optional): breathe between `brightness` and `toBrightness`, `count` times over `periodMs`.
  - `strobe` (optional): sharp flashes via `turn` off/on (keep >= 250 ms; fades make color strobes mushy).

## LAN commands (UDP port 4003)
```
{"msg":{"cmd":"turn","data":{"value":1}}}
{"msg":{"cmd":"brightness","data":{"value":80}}}
{"msg":{"cmd":"colorwc","data":{"color":{"r":255,"g":0,"b":0},"colorTemInKelvin":0}}}
```

## Usage
```
python3 play.py liberty-one --ip 192.168.1.83            # play once, end on primary
python3 play.py liberty-one --ip 192.168.1.83 --primary  # static primary
python3 play.py liberty-one --ip 192.168.1.83 --dry-run  # print commands only
```
Warrior One (N8301J) wears standard Heart paint in the game, so use `heart`.
