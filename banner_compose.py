"""
Compose Instagram banners with elegant text overlay.
Source images preserved as _post_src.jpg / _story_src.jpg.
Output: instagram_post.jpg (1080x1350) and instagram_story.jpg (1080x1920).
"""
from PIL import Image, ImageDraw, ImageFont

SERIF_BOLD = "/usr/share/fonts/opentype/noto/NotoSerifCJK-Bold.ttc"
SERIF_REG  = "/usr/share/fonts/opentype/noto/NotoSerifCJK-Regular.ttc"
SANS_BOLD  = "/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc"
SANS_REG   = "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc"

MOSS = (46, 74, 58)
IVORY = (246, 241, 232)
GOLD = (182, 145, 96)
DARK = (28, 36, 30)
WHITE = (255, 255, 255)


def F(path, size):
    return ImageFont.truetype(path, size)


def text_w(draw, text, font):
    bb = draw.textbbox((0, 0), text, font=font)
    return bb[2] - bb[0]


def draw_centered(draw, text, font, fill, y, W):
    w = text_w(draw, text, font)
    draw.text(((W - w) // 2, y), text, font=font, fill=fill)


def compose_post():
    """1080x1350 feed banner."""
    base = Image.open("/home/user/workspace/taishitsugaku-lp/images/_post_src.jpg").convert("RGB")
    base = base.resize((1080, 1350), Image.LANCZOS)

    # Soft ivory veil over upper area for legibility — the upper half is already plain linen, so just slight veil
    overlay = Image.new("RGBA", (1080, 1350), (0, 0, 0, 0))
    od = ImageDraw.Draw(overlay)
    for y in range(0, 700):
        alpha = int(120 * (1 - y / 700) ** 1.4)
        od.rectangle([(0, y), (1080, y + 1)], fill=(246, 241, 232, alpha))
    base = Image.alpha_composite(base.convert("RGBA"), overlay).convert("RGB")

    draw = ImageDraw.Draw(base)
    W = 1080

    # ─── Top: brand + title ───
    eyebrow = "THE HERBS  ·  植物美容学校"
    f_eye = F(SANS_REG, 26)
    draw_centered(draw, eyebrow, f_eye, MOSS, 100, W)

    # gold divider
    draw.rectangle([(W // 2 - 32, 156), (W // 2 + 32, 158)], fill=GOLD)

    f_title = F(SERIF_BOLD, 92)
    draw_centered(draw, "体質を、読む。", f_title, DARK, 200, W)
    draw_centered(draw, "美容を、深める。", f_title, DARK, 320, W)

    f_sub = F(SERIF_REG, 32)
    draw_centered(draw, "外胚葉・中胚葉・内胚葉  ─  体質学講習会", f_sub, MOSS, 460, W)

    f_target = F(SANS_REG, 26)
    draw_centered(draw, "美容師・エステティシャンのための、体質学。", f_target, MOSS, 515, W)

    # ─── Bottom: schedule strip on subtle ivory band ───
    # Draw a soft semi-transparent ivory band at bottom for the date info
    band = Image.new("RGBA", (1080, 200), (246, 241, 232, 230))
    band_pos_y = 1130
    base_rgba = base.convert("RGBA")
    base_rgba.alpha_composite(band, dest=(0, band_pos_y))
    base = base_rgba.convert("RGB")
    draw = ImageDraw.Draw(base)

    # Top hairline
    draw.rectangle([(80, band_pos_y - 1), (1000, band_pos_y + 1)], fill=GOLD)

    f_dates = F(SERIF_BOLD, 46)
    draw_centered(draw, "6.15  /  7.13  /  8.10", f_dates, DARK, 1155, W)

    f_info = F(SANS_REG, 24)
    draw_centered(draw, "全3回 ・ 各回 10:00–16:00 ・ 神戸 灘 ・ 座学のみ", f_info, MOSS, 1230, W)

    f_url = F(SANS_BOLD, 22)
    draw_centered(draw, "the-herbs.co.jp/school/facecare", f_url, GOLD, 1280, W)

    base.save(
        "/home/user/workspace/taishitsugaku-lp/images/instagram_post.jpg",
        quality=92, optimize=True
    )
    print("Saved post: 1080x1350")


def compose_story():
    """1080x1920 story banner.
    Source has 3 horizontal bands: ivory linen / herbs+bottles photo / moss.
    Top band: brand + title. Middle: photo (no text). Bottom: dates + CTA.
    """
    base = Image.open("/home/user/workspace/taishitsugaku-lp/images/_story_src.jpg").convert("RGB")
    base = base.resize((1080, 1920), Image.LANCZOS)

    # Slight ivory veil on top band only
    overlay = Image.new("RGBA", (1080, 1920), (0, 0, 0, 0))
    od = ImageDraw.Draw(overlay)
    for y in range(0, 580):
        alpha = int(110 * (1 - y / 580) ** 1.4)
        od.rectangle([(0, y), (1080, y + 1)], fill=(246, 241, 232, alpha))
    base = Image.alpha_composite(base.convert("RGBA"), overlay).convert("RGB")

    draw = ImageDraw.Draw(base)
    W = 1080

    # ─── Top band (ivory linen, ~0-580) ───
    f_eye = F(SANS_REG, 28)
    draw_centered(draw, "THE HERBS  ·  体質学講習会", f_eye, MOSS, 130, W)
    draw.rectangle([(W // 2 - 36, 188), (W // 2 + 36, 190)], fill=GOLD)

    f_title = F(SERIF_BOLD, 100)
    draw_centered(draw, "体質を、", f_title, DARK, 230, W)
    draw_centered(draw, "読み解く。", f_title, DARK, 360, W)

    f_sub = F(SERIF_REG, 36)
    draw_centered(draw, "外胚葉・中胚葉・内胚葉", f_sub, MOSS, 510, W)

    # ─── Bottom band (deep moss, 1280-1920) ───
    # Title on moss
    f_dates = F(SERIF_BOLD, 56)
    draw_centered(draw, "6.15  /  7.13  /  8.10", f_dates, IVORY, 1430, W)

    f_info = F(SANS_REG, 28)
    draw_centered(draw, "全3回 ・ 各回 10:00–16:00", f_info, (220, 215, 200), 1520, W)
    draw_centered(draw, "神戸 灘 ・ 美容師・エステティシャン向け", f_info, (220, 215, 200), 1565, W)

    # Gold CTA pill
    cta_w, cta_h = 580, 100
    cta_x = (W - cta_w) // 2
    cta_y = 1660
    draw.rounded_rectangle(
        [(cta_x, cta_y), (cta_x + cta_w, cta_y + cta_h)],
        radius=cta_h // 2, fill=GOLD,
    )
    f_cta = F(SANS_BOLD, 32)
    cta_text = "お申し込みはこちら"
    bb = draw.textbbox((0, 0), cta_text, font=f_cta)
    tw = bb[2] - bb[0]
    th = bb[3] - bb[1]
    draw.text(
        (cta_x + (cta_w - tw) // 2, cta_y + (cta_h - th) // 2 - 6),
        cta_text, font=f_cta, fill=WHITE,
    )

    f_url = F(SANS_REG, 22)
    draw_centered(draw, "the-herbs.co.jp/school/facecare", f_url, (220, 215, 200), 1810, W)

    base.save(
        "/home/user/workspace/taishitsugaku-lp/images/instagram_story.jpg",
        quality=92, optimize=True
    )
    print("Saved story: 1080x1920")


if __name__ == "__main__":
    compose_post()
    compose_story()
