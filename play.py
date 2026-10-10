#!/usr/bin/env python3
"""Play a livery scheme on a Govee H618C over the LAN API (UDP 4003).
Usage: play.py <slug> --ip 192.168.1.83 [--loops N] [--primary] [--dry-run] [--stripes [--segments N]]"""
import argparse, base64, json, socket, time, pathlib
ROOT = pathlib.Path(__file__).parent

def segment_packet(rgb, mask):
    """20-byte ptReal segment color packet; mask bit0 = segment 1."""
    b = [0x33, 0x05, 0x15, 0x01, rgb["r"], rgb["g"], rgb["b"], 0, 0, 0, 0, 0,
         mask & 0xFF, (mask >> 8) & 0xFF, 0, 0, 0, 0, 0]
    x = 0
    for v in b: x ^= v
    return bytes(b + [x])

def stripe_masks(n_colors, segments):
    """Mask per color for a repeating c1,c2,... pattern; color 0 gets ALL segments."""
    masks = [0] * n_colors
    for seg in range(segments):
        masks[seg % n_colors] |= 1 << seg
    masks[0] = (1 << segments) - 1
    return masks
def main():
    a = argparse.ArgumentParser(); a.add_argument("slug"); a.add_argument("--ip", required=True)
    a.add_argument("--loops", type=int, default=1); a.add_argument("--primary", action="store_true")
    a.add_argument("--dry-run", action="store_true")
    a.add_argument("--stripes", action="store_true", help="paint per-segment stripes via ptReal")
    a.add_argument("--segments", type=int, help="segment count (default: scheme's, assumed 15)")
    o = a.parse_args()
    s = json.loads((ROOT / "schemes" / f"{o.slug}.json").read_text())
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    def send(cmd, data):
        msg = json.dumps({"msg": {"cmd": cmd, "data": data}})
        print(msg) if o.dry_run else sock.sendto(msg.encode(), (o.ip, 4003))
    def color(c): send("colorwc", {"color": c, "colorTemInKelvin": 0})
    def bright(v): send("brightness", {"value": max(1, min(100, int(v)))})
    sleep = (lambda s: None) if o.dry_run else time.sleep
    send("turn", {"value": 1})
    if o.stripes:
        st = s["stripes"]; segs = o.segments or st["segment_count"]
        gap = st.get("gap_ms", 500) / 1000
        bright(s["primary"]["brightness"])
        # Reliable recipe: paint ALL segments with color 1, then each further
        # color on its own mask, one packet at a time with a gap.
        for c, m in zip(st["colors"], stripe_masks(len(st["colors"]), segs)):
            pkt = segment_packet(c, m)
            if o.dry_run: print("# ptReal", pkt.hex(), "mask %04x" % m)
            send("ptReal", {"command": [base64.b64encode(pkt).decode()]})
            sleep(gap)
        return
    if o.primary:
        color(s["primary"]["color"]); bright(s["primary"]["brightness"]); return
    for _ in range(o.loops):
        for st in s["steps"]:
            color(st["color"]); bright(st["brightness"])
            if p := st.get("pulse"):
                for _ in range(p["count"]):
                    bright(p["toBrightness"]); sleep(p["periodMs"] / 2000)
                    bright(st["brightness"]); sleep(p["periodMs"] / 2000)
            if f := st.get("strobe"):
                for _ in range(f["count"]):
                    send("turn", {"value": 0}); sleep(f["offMs"] / 1000)
                    send("turn", {"value": 1}); sleep(f["onMs"] / 1000)
            sleep(st["holdMs"] / 1000)
    color(s["primary"]["color"]); bright(s["primary"]["brightness"])
if __name__ == "__main__": main()
