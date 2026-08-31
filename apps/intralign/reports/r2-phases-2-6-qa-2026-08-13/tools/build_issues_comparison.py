from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parents[1]
REFERENCE = Path(
    r"C:\Users\Hp\AppData\Local\Temp\codex-clipboard-c665c6d3-9831-4281-a592-597149a80b1b.png"
)
IMPLEMENTATION = ROOT / "evidence" / "app-issues-fixed.png"
OUTPUT = ROOT / "evidence" / "issues-prototype-vs-app.png"


def fit(image: Image.Image, width: int, height: int) -> Image.Image:
    copy = image.copy()
    copy.thumbnail((width, height), Image.Resampling.LANCZOS)
    return copy


reference = fit(Image.open(REFERENCE).convert("RGB"), 800, 650)
implementation = fit(Image.open(IMPLEMENTATION).convert("RGB"), 800, 650)
canvas = Image.new("RGB", (1660, 740), "#0b0f12")
draw = ImageDraw.Draw(canvas)
font = ImageFont.load_default(size=22)
draw.text((30, 24), "R2 prototype reference", fill="#e9edf2", font=font)
draw.text((850, 24), "R2 production app", fill="#e9edf2", font=font)
canvas.paste(reference, (30, 70))
canvas.paste(implementation, (850, 70))
draw.rectangle((25, 65, 35 + reference.width, 75 + reference.height), outline="#4b5665", width=2)
draw.rectangle(
    (845, 65, 855 + implementation.width, 75 + implementation.height),
    outline="#4b5665",
    width=2,
)
canvas.save(OUTPUT, quality=95)
print(OUTPUT)
