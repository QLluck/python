#!/usr/bin/env python3
"""Batch process images to CSV + saved PNGs (no browser)."""

from __future__ import annotations

import argparse
import csv
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from app.core.pipeline import ProcessRequest, run  # noqa: E402


def main() -> None:
    p = argparse.ArgumentParser(description="Batch lesion segmentation")
    p.add_argument("--input", type=Path, required=True, help="Folder of images")
    p.add_argument("--out", type=Path, required=True, help="Output folder")
    p.add_argument("--max-side", type=int, default=1280)
    p.add_argument("--segment-method", default="otsu_roi")
    args = p.parse_args()

    args.out.mkdir(parents=True, exist_ok=True)
    exts = {".png", ".jpg", ".jpeg", ".bmp"}
    rows = []
    files = sorted([f for f in args.input.iterdir() if f.suffix.lower() in exts])
    for fp in files:
        rel = fp.name
        row = {"file": rel, "ok": False, "error": "", "elapsed_ms": "", "roi": ""}
        try:
            data = fp.read_bytes()
            req = ProcessRequest(
                stage="full",
                max_side=args.max_side,
                segment_method=args.segment_method,  # type: ignore[arg-type]
                min_component_area=50,
            )
            out = run(data, fp.name, req, log_dir=args.out)
            row["ok"] = out.get("ok", False)
            row["error"] = out.get("error") or ""
            meta = out.get("meta") or {}
            row["elapsed_ms"] = meta.get("elapsed_ms", "")
            row["roi"] = str(meta.get("roi"))
            if out.get("ok"):
                import base64

                if out.get("mask_png_b64"):
                    (args.out / f"{fp.stem}_mask.png").write_bytes(
                        base64.b64decode(out["mask_png_b64"])
                    )
                if out.get("overlay_png_b64"):
                    (args.out / f"{fp.stem}_overlay.png").write_bytes(
                        base64.b64decode(out["overlay_png_b64"])
                    )
        except OSError as e:
            row["error"] = str(e)
        rows.append(row)

    csv_path = args.out / "batch_summary.csv"
    with csv_path.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=["file", "ok", "error", "elapsed_ms", "roi"])
        w.writeheader()
        w.writerows(rows)
    print(f"Wrote {csv_path} ({len(rows)} rows)")


if __name__ == "__main__":
    main()
