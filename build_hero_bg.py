"""
Compose hero background using the full 3x3 typology grid PDF as the source.
The grid (3 types × 3 views: front/side/back) sits on the right portion of a
wide canvas, with an ivory wash on the left for hero text legibility.

Output: images/hero_typology.jpg (1920x1200)
"""
from PIL import Image, ImageDraw, ImageFilter

W, H = 1920, 1200
IVORY = (246, 241, 232)
IVORY_DEEP = (236, 229, 215)


def make_background():
    bg = Image.new("RGB", (W, H), IVORY)
    # Subtle diagonal vignette deeper toward bottom-right
    grad = Image.new("L", (W, H), 0)
    gd = ImageDraw.Draw(grad)
    for y in range(H):
        for x_step in range(0, W, 6):
            d = ((x_step / W) + (y / H)) / 2
            v = int(50 * d)
            gd.point((x_step, y), fill=v)
    grad = grad.filter(ImageFilter.GaussianBlur(80))
    deep = Image.new("RGB", (W, H), IVORY_DEEP)
    bg = Image.composite(deep, bg, grad)
    return bg


def place_grid(bg):
    """Place full grid PDF render on right portion."""
    base = bg.convert("RGBA")

    grid = Image.open(
        "/home/user/workspace/taishitsugaku-lp/images/typology_full-1.jpg"
    ).convert("RGB")

    # Convert near-white pixels to transparent to drop the white background
    grid = grid.convert("RGBA")
    px = grid.load()
    gw, gh = grid.size
    for y in range(gh):
        for x in range(gw):
            r, g, b, a = px[x, y]
            # If close to white, fade to transparent. Use min channel.
            m = min(r, g, b)
            if m > 240:
                # very white -> fully transparent
                px[x, y] = (r, g, b, 0)
            elif m > 220:
                # slightly off-white -> partial transparency
                px[x, y] = (r, g, b, int((255 - m) * 8))

    # Crop tight bounding box to remove fully-transparent margins
    bbox = grid.getbbox()
    if bbox:
        grid = grid.crop(bbox)

    # Resize so the grid width fits roughly the right ~52% of the canvas.
    # The grid is portrait (1654x2756 -> 0.6 ratio). We want it visible without cropping the rows,
    # so scale by HEIGHT to fit canvas with margins, then place anchored to right.
    target_h = H - 80  # 1120px tall
    ratio = target_h / grid.height
    new_w = int(grid.width * ratio)
    new_h = target_h
    grid_resized = grid.resize((new_w, new_h), Image.LANCZOS)

    # Soften alpha so illustrations sit as background
    r, g, b, a = grid_resized.split()
    a = a.point(lambda v: int(v * 0.62))  # softer overall
    grid_resized = Image.merge("RGBA", (r, g, b, a))

    # Anchor to right side, vertical center
    x = W - new_w - 50
    y = (H - new_h) // 2
    base.alpha_composite(grid_resized, (x, y))
    return base.convert("RGB")


def add_text_overlay(img):
    """Ivory wash on left so hero text remains legible."""
    overlay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    od = ImageDraw.Draw(overlay)
    # Heavy ivory wash up to ~58% width so the title/lead area stays totally clean,
    # then a soft tail to ~75% so the grid emerges gradually
    for x in range(0, int(W * 0.58)):
        od.rectangle([(x, 0), (x + 1, H)], fill=(246, 241, 232, 250))
    for x in range(int(W * 0.58), int(W * 0.78)):
        ratio = 1 - ((x - W * 0.58) / (W * 0.20))
        alpha = int(250 * ratio)
        od.rectangle([(x, 0), (x + 1, H)], fill=(246, 241, 232, alpha))
    # Tiny top fade for header
    for y in range(0, 180):
        a = int(60 * (1 - y / 180))
        od.rectangle([(0, y), (W, y + 1)], fill=(246, 241, 232, a))
    return Image.alpha_composite(img.convert("RGBA"), overlay).convert("RGB")


def main():
    bg = make_background()
    composed = place_grid(bg)
    final = add_text_overlay(composed)
    out = "/home/user/workspace/taishitsugaku-lp/images/hero_typology.jpg"
    final.save(out, quality=92, optimize=True)
    print(f"Saved: {out} {final.size}")


if __name__ == "__main__":
    main()
