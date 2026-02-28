import json
import os
from pathlib import Path

from PIL import Image, ImageChops
from playwright.sync_api import sync_playwright

# === PATHS / CONFIG ===
BASE_DIR = Path(__file__).resolve().parent
FIGMA_DIR = BASE_DIR / "slider" / "pngs_for_testing"
OUT_DIR = BASE_DIR / "artifacts_pixel"
URL = os.getenv("PIXEL_COMPARE_URL", "http://127.0.0.1:8000/")
WAIT_MS = int(os.getenv("PIXEL_COMPARE_WAIT_MS", "1200"))

BASELINES = {
    "desktop": FIGMA_DIR / "desktop.png",
    "mobile": FIGMA_DIR / "mobile.png",
}


def _rel(path: Path) -> str:
    return path.relative_to(BASE_DIR).as_posix()


def capture_actual(baseline_path: Path, out_path: Path):
    baseline = Image.open(baseline_path)
    w, h = baseline.size

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            viewport={"width": w, "height": h},
            device_scale_factor=1,
        )
        page = context.new_page()
        page.goto(URL, wait_until="networkidle")
        page.wait_for_timeout(WAIT_MS)
        page.screenshot(path=str(out_path), full_page=False)
        context.close()
        browser.close()


def make_diff(baseline_path: Path, actual_path: Path, diff_path: Path):
    baseline = Image.open(baseline_path).convert("RGBA")
    actual = Image.open(actual_path).convert("RGBA")

    if actual.size != baseline.size:
        actual = actual.resize(baseline.size)

    raw_diff = ImageChops.difference(baseline, actual)
    gray = raw_diff.convert("L")

    mask = gray.point(lambda x: 255 if x > 12 else 0)

    overlay = actual.copy()
    red = Image.new("RGBA", baseline.size, (255, 0, 0, 170))
    overlay.paste(red, (0, 0), mask)
    overlay.save(diff_path)

    hist = gray.histogram()
    total = baseline.size[0] * baseline.size[1]
    changed = total - hist[0]
    percent = round(changed / total * 100, 3)

    return {
        "size": {"width": baseline.size[0], "height": baseline.size[1]},
        "changed_pixels": int(changed),
        "changed_percent": percent,
    }


def main():
    for path in BASELINES.values():
        if not path.exists():
            raise FileNotFoundError(f"Не найден baseline: {path}")

    (OUT_DIR / "actual").mkdir(parents=True, exist_ok=True)
    (OUT_DIR / "diff").mkdir(parents=True, exist_ok=True)

    report = {"url": URL, "cases": {}}

    for name, baseline_path in BASELINES.items():
        actual_path = OUT_DIR / "actual" / f"{name}.png"
        diff_path = OUT_DIR / "diff" / f"{name}.png"

        capture_actual(baseline_path, actual_path)
        metrics = make_diff(baseline_path, actual_path, diff_path)

        report["cases"][name] = {
            "baseline": _rel(baseline_path),
            "actual": _rel(actual_path),
            "diff": _rel(diff_path),
            **metrics,
        }

    report_path = OUT_DIR / "diff" / "report.json"
    report_path.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")

    print("=== DONE ===")
    print(f"Report: {report_path}")
    for n, d in report["cases"].items():
        print(f"{n}: {d['changed_percent']}% ({d['changed_pixels']} px)")


if __name__ == "__main__":
    main()
