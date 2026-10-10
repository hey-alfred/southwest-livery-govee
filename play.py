#!/usr/bin/env python3
"""Play a livery scheme on a Govee H618C over the LAN API (UDP 4003).
Usage: play.py <slug> --ip 192.168.1.83 [--loops N] [--primary] [--dry-run]"""
import argparse, json, socket, time, pathlib
ROOT = pathlib.Path(__file__).parent
def main():
    a = argparse.ArgumentParser(); a.add_argument("slug"); a.add_argument("--ip", required=True)
    a.add_argument("--loops", type=int, default=1); a.add_argument("--primary", action="store_true")
    a.add_argument("--dry-run", action="store_true"); o = a.parse_args()
    s = json.loads((ROOT / "schemes" / f"{o.slug}.json").read_text())
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    def send(cmd, data):
        msg = json.dumps({"msg": {"cmd": cmd, "data": data}})
        print(msg) if o.dry_run else sock.sendto(msg.encode(), (o.ip, 4003))
    def color(c): send("colorwc", {"color": c, "colorTemInKelvin": 0})
    def bright(v): send("brightness", {"value": max(1, min(100, int(v)))})
    sleep = (lambda s: None) if o.dry_run else time.sleep
    send("turn", {"value": 1})
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
