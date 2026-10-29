import os
from PIL import Image, ImageDraw, ImageFont

def create_high_res_figure2():
    os.makedirs("figures", exist_ok=True)
    
    # Fonts
    font_bold = "C:/Windows/Fonts/segoeuib.ttf"
    font_reg = "C:/Windows/Fonts/segoeui.ttf"
    font_semi = "C:/Windows/Fonts/segoeuisl.ttf"
    if not os.path.exists(font_semi):
        font_semi = font_reg

    # -------------------------------------------------------------
    # 1. Panel (a) Notification Shade: 2400 x 972 at 300 DPI
    # -------------------------------------------------------------
    W_a, H_a = 2400, 972
    img_a = Image.new("RGBA", (W_a, H_a), (18, 22, 28, 255)) # Dark system shade backdrop
    draw_a = ImageDraw.Draw(img_a)

    # Card dimensions
    card_x0, card_y0 = 60, 140
    card_x1, card_y1 = W_a - 60, H_a - 40
    card_r = 54
    # Card background: Material You surface light
    draw_a.rounded_rectangle([card_x0, card_y0, card_x1, card_y1], radius=card_r, fill=(242, 245, 249, 255))

    # App icon: Teal circle with white lock
    icon_cx, icon_cy = 220, 260
    icon_r = 75
    draw_a.ellipse([icon_cx - icon_r, icon_cy - icon_r, icon_cx + icon_r, icon_cy + icon_r], fill=(0, 104, 122, 255))
    
    # Lock glyph inside icon
    # Shackle
    draw_a.arc([icon_cx - 24, icon_cy - 46, icon_cx + 24, icon_cy - 2], start=180, end=0, fill=(255, 255, 255, 255), width=10)
    # Body
    draw_a.rounded_rectangle([icon_cx - 28, icon_cy - 12, icon_cx + 28, icon_cy + 36], radius=8, fill=(255, 255, 255, 255))
    # Keyhole
    draw_a.ellipse([icon_cx - 7, icon_cy + 2, icon_cx + 7, icon_cy + 16], fill=(0, 104, 122, 255))
    draw_a.rectangle([icon_cx - 4, icon_cy + 10, icon_cx + 4, icon_cy + 24], fill=(0, 104, 122, 255))

    # Text headers
    f_app = ImageFont.truetype(font_reg, 54)
    f_title = ImageFont.truetype(font_bold, 78)
    f_body = ImageFont.truetype(font_reg, 62)

    # App name + bell
    draw_a.text((340, 225), "SecretHandle", fill=(70, 75, 80, 255), font=f_app)
    # Bell icon next to app name
    bell_x = 700
    bell_y = 245
    draw_a.arc([bell_x, bell_y, bell_x + 30, bell_y + 34], start=180, end=0, fill=(70, 75, 80, 255), width=6)
    draw_a.rectangle([bell_x - 3, bell_y + 26, bell_x + 33, bell_y + 32], fill=(70, 75, 80, 255))
    draw_a.ellipse([bell_x + 10, bell_y + 34, bell_x + 20, bell_y + 42], fill=(70, 75, 80, 255))

    # Chevron expand arrow on right
    ch_x = card_x1 - 180
    ch_y = 250
    draw_a.line([(ch_x - 24, ch_y + 12), (ch_x, ch_y - 12), (ch_x + 24, ch_y + 12)], fill=(40, 45, 50, 255), width=10)

    # Title: SecretHandle: code protected
    draw_a.text((340, 390), "SecretHandle: code protected", fill=(20, 24, 28, 255), font=f_title)

    # Body: SH-B9B564 from SMS Messenger - open
    draw_a.text((340, 520), "SH-B9B564 from SMS Messenger - open", fill=(55, 60, 68, 255), font=f_body)
    draw_a.text((340, 620), "SecretHandle to use it", fill=(55, 60, 68, 255), font=f_body)

    # Save shade with 300 DPI metadata
    img_a.save("figures/b3_redacted_shade.png", dpi=(300, 300))
    print("[+] Exported figures/b3_redacted_shade.png (2400x972 @ 300 DPI)")

    # -------------------------------------------------------------
    # 2. Panel (b) Conversation Overlay: 1800 x 1650 at 300 DPI
    # -------------------------------------------------------------
    W_b, H_b = 1800, 1650
    img_b = Image.new("RGBA", (W_b, H_b), (255, 255, 255, 255)) # Clean white messenger background
    draw_b = ImageDraw.Draw(img_b)

    # Bubble dimensions
    b_margin_x = 40
    b_w = W_b - 2 * b_margin_x
    b_h = 600

    # Overlay Bubble 1 (Top)
    b1_y0 = 60
    b1_y1 = b1_y0 + b_h
    # Non-touchable overlay color (#1E222B)
    draw_b.rounded_rectangle([b_margin_x, b1_y0, b_margin_x + b_w, b1_y1], radius=32, fill=(30, 34, 43, 255))
    
    # Overlay Bubble 2 (Bottom)
    b2_y0 = b1_y1 + 330
    b2_y1 = b2_y0 + b_h
    draw_b.rounded_rectangle([b_margin_x, b2_y0, b_margin_x + b_w, b2_y1], radius=32, fill=(30, 34, 43, 255))

    # Timestamp in between: 16:32
    f_time = ImageFont.truetype(font_reg, 82)
    time_str = "16:32"
    t_bbox = draw_b.textbbox((0, 0), time_str, font=f_time)
    t_w = t_bbox[2] - t_bbox[0]
    draw_b.text(((W_b - t_w) // 2, b1_y1 + 110), time_str, fill=(28, 41, 56, 255), font=f_time)

    # Overlay Text: "SecretHandle: protected"
    f_prot = ImageFont.truetype(font_reg, 68)
    prot_str = "SecretHandle: protected"
    p_bbox = draw_b.textbbox((0, 0), prot_str, font=f_prot)
    p_w = p_bbox[2] - p_bbox[0]
    p_h = p_bbox[3] - p_bbox[1]

    # Center in Bubble 1
    draw_b.text(((W_b - p_w) // 2, b1_y0 + (b_h - p_h) // 2 - 10), prot_str, fill=(255, 255, 255, 255), font=f_prot)
    # Center in Bubble 2
    draw_b.text(((W_b - p_w) // 2, b2_y0 + (b_h - p_h) // 2 - 10), prot_str, fill=(255, 255, 255, 255), font=f_prot)

    # Save SMS overlay with 300 DPI metadata
    img_b.save("figures/b3_masked_sms.png", dpi=(300, 300))
    print("[+] Exported figures/b3_masked_sms.png (1800x1650 @ 300 DPI)")

if __name__ == "__main__":
    create_high_res_figure2()
