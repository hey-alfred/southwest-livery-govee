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

## LED color tuning
Screen hexes look wrong on the H618C: LEDs exaggerate small secondary channels
(e.g. screen red #c22b3a shows as pinkish purple). Every `color` in a scheme is an
LED-tuned rgb; the original game hex is kept in `source_hex` (and `contrail` /
`contrail_led` list both). `play.py` sends only the LED values.

Rules: zero minor channels; reds -> (255,0,0); blues -> pure-ish (navy (0,40,255),
lighter (0,90,255)); gold/yellow -> (255,55-60,0), amber (255,35,0), no blue;
rust -> (180,18,0); purple -> (120,0,255); white -> (255,255,255) at 70% brightness (verified in a red/white/blue test).

| source_hex | LED rgb | note |
|---|---|---|
| #c22b3a, #d5152e | 255,0,0 | red |
| #1b3d8f | 0,40,255 | navy |
| #304cb2 | 0,60,255 | Heart bold blue |
| #27488f | 0,70,255 | cobalt |
| #2e5fa3 | 0,90,255 | flag blue |
| #f9b612 | 255,55,0 | gold (hardware-tuned) |
| #f3c317 | 255,60,0 | zia yellow (hardware-tuned) |
| #d9a33c | 255,35,0 | desert gold amber (hardware-tuned) |
| #b34726 | 180,18,0 | copper/rust, dimmer to stay distinct from amber (UNTESTED) |
| #5b3b8f | 120,0,255 | purple |
| #ffffff | 255,255,255 | white @70% |

**Hardware notes (H618C):** green is heavily exaggerated on this strip, so warm
colors use very little green. Red, white, and navy (0,40,255) are verified on
hardware; gold/amber/yellow are hardware-tuned; copper/rust (180,18,0) and all
other blues and purple are untested on hardware.
