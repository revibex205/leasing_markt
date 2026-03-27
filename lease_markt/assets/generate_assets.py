"""
assets/generate_assets.py
Generate placeholder machine images using Pillow.
Run once before starting the app: python assets/generate_assets.py
"""

import os
from PIL import Image, ImageDraw, ImageFont

# Output directory
OUT_DIR = os.path.join(os.path.dirname(__file__), "machines")
os.makedirs(OUT_DIR, exist_ok=True)

# Machine definitions: (filename, category_color, category_name, brand_model, icon_char)
MACHINES = [
    ("cat_320d.png",        "#E8A020", "CONSTRUCTION",       "Caterpillar\n320D Excavator",        "⚙"),
    ("liebherr_crane.png",  "#E8E020", "CONSTRUCTION",       "Liebherr\nLTM 1060-3.1 Crane",       "🏗"),
    ("jd_6130m.png",        "#367C2A", "AGRICULTURAL",       "John Deere\n6130M Tractor",           "🌾"),
    ("mazak_integrex.png",  "#1A3A6B", "MANUFACTURING",      "Mazak INTEGREX\ni-400S CNC",          "⚙"),
    ("toyota_forklift.png", "#D44000", "MATERIAL HANDLING",  "Toyota 8FBE18\nElectric Forklift",    "🏭"),
    ("komatsu_pc210.png",   "#FFCC00", "CONSTRUCTION",       "Komatsu\nPC210LC-11 Excavator",       "⚙"),
    ("heidelberg_press.png","#003366", "PRINTING",           "Heidelberg\nSpeedmaster XL 75",       "🖨"),
    ("nh_cr990.png",        "#0052A5", "AGRICULTURAL",       "New Holland\nCR9.90 Harvester",       "🌾"),
    ("atlasc_gen.png",      "#3A3A3A", "ENERGY",             "Atlas Copco\nQAC 800 Generator",      "⚡"),
    ("mb_actros.png",       "#00305B", "TRANSPORT",          "Mercedes-Benz\nActros 1848 LS Truck", "🚛"),
]

WIDTH, HEIGHT = 600, 400


def draw_machine_image(filename: str, bg_color: str, category: str,
                        name: str, icon: str):
    """Create a gradient placeholder image for a machine."""
    img = Image.new("RGB", (WIDTH, HEIGHT), bg_color)
    draw = ImageDraw.Draw(img)

    # Gradient overlay (darker bottom half)
    for y in range(HEIGHT):
        alpha = int(80 * (y / HEIGHT))
        draw.line([(0, y), (WIDTH, y)], fill=(0, 0, 0, alpha))

    # Background grid pattern
    for x in range(0, WIDTH, 40):
        draw.line([(x, 0), (x, HEIGHT)], fill=(255, 255, 255, 15), width=1)
    for y in range(0, HEIGHT, 40):
        draw.line([(0, y), (WIDTH, y)], fill=(255, 255, 255, 15), width=1)

    # Category badge
    draw.rounded_rectangle([(20, 20), (180, 50)], radius=8, fill=(0, 0, 0, 120))
    try:
        font_small = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 11)
        font_large = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 22)
        font_name = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 18)
    except Exception:
        font_small = ImageFont.load_default()
        font_large = font_small
        font_name = font_small

    draw.text((30, 28), category, fill="white", font=font_small)

    # Large icon text in center
    draw.text((WIDTH // 2 - 30, HEIGHT // 2 - 60), icon, fill=(255, 255, 255, 200), font=font_large)

    # Machine name
    lines = name.split("\n")
    y_start = HEIGHT - 80
    for line in lines:
        draw.text((20, y_start), line, fill="white", font=(font_large if y_start > HEIGHT - 65 else font_name))
        y_start += 26

    # Bank stamp in corner
    draw.rounded_rectangle([(WIDTH - 160, HEIGHT - 45), (WIDTH - 10, HEIGHT - 10)],
                             radius=6, fill=(17, 71, 204, 200))
    draw.text((WIDTH - 150, HEIGHT - 36), "BANK APPROVED", fill="white", font=font_small)

    img.save(os.path.join(OUT_DIR, filename))
    print(f"  ✓ {filename}")


if __name__ == "__main__":
    print("Generating machine placeholder images...")
    for args in MACHINES:
        draw_machine_image(*args)
    print(f"Done. {len(MACHINES)} images saved to assets/machines/")
