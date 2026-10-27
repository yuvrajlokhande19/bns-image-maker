from PIL import Image, ImageDraw, ImageFont, ImageFilter
from pathlib import Path

def create_story_graphic(post_img_path: Path, output_story_path: Path):
    """
    Creates a 1080x1920 Story image with the 1080x1350 post card centered,
    mimicking Instagram's native 'Share Post to Story' sticker.
    """
    story_w, story_h = 1080, 1920
    post_img = Image.open(post_img_path).convert("RGBA")
    
    # 1. Create Background: Dark Navy #0B1D2F
    bg = Image.new("RGBA", (story_w, story_h), (11, 29, 47, 255))
    
    # Optional: Soft background blur from the original image
    bg_blur = post_img.resize((story_w, story_h)).filter(ImageFilter.GaussianBlur(radius=35))
    # Dim the blur slightly so the card pops
    dim_overlay = Image.new("RGBA", (story_w, story_h), (11, 29, 47, 180))
    bg_composite = Image.alpha_composite(bg_blur, dim_overlay)
    
    # 2. Scale Post Card to fit nicely in 9:16 frame (width: 940, height: 1175)
    card_w = 940
    card_h = int(card_w * (1350 / 1080)) # 1175
    post_resized = post_img.resize((card_w, card_h), Image.Resampling.LANCZOS)
    
    # Rounded corners mask
    corner_radius = 24
    mask = Image.new("L", (card_w, card_h), 0)
    draw_mask = ImageDraw.Draw(mask)
    draw_mask.rounded_rectangle([0, 0, card_w, card_h], radius=corner_radius, fill=255)
    
    # Card position (centered vertically)
    card_x = (story_w - card_w) // 2
    card_y = (story_h - card_h) // 2
    
    # 3. Soft drop shadow behind card
    shadow_pad = 20
    shadow = Image.new("RGBA", (card_w + shadow_pad * 2, card_h + shadow_pad * 2), (0, 0, 0, 0))
    draw_shadow = ImageDraw.Draw(shadow)
    draw_shadow.rounded_rectangle([shadow_pad, shadow_pad, card_w + shadow_pad, card_h + shadow_pad], radius=corner_radius, fill=(0, 0, 0, 120))
    shadow = shadow.filter(ImageFilter.GaussianBlur(radius=16))
    
    # Paste shadow then card
    bg_composite.paste(shadow, (card_x - shadow_pad, card_y - shadow_pad), shadow)
    bg_composite.paste(post_resized, (card_x, card_y), mask)
    
    # 4. Draw Header & Footer Sticker Badges
    draw = ImageDraw.Draw(bg_composite)
    
    # Top "NEW POST ⚖️" Pill Sticker
    pill_w, pill_h = 240, 56
    pill_x = (story_w - pill_w) // 2
    pill_y = card_y - 85
    draw.rounded_rectangle([pill_x, pill_y, pill_x + pill_w, pill_y + pill_h], radius=28, fill=(244, 196, 78, 255))
    
    # Try system fonts or default
    try:
        font_pill = ImageFont.truetype("arialbd.ttf", 24)
        font_sub = ImageFont.truetype("arial.ttf", 26)
    except Exception:
        font_pill = ImageFont.load_default()
        font_sub = ImageFont.load_default()
        
    draw.text((story_w // 2, pill_y + pill_h // 2), "NEW POST ⚖️", fill=(15, 41, 66), anchor="mm", font=font_pill)
    
    # Bottom callout: "Tap to read full post on feed 👆"
    bottom_y = card_y + card_h + 45
    draw.text((story_w // 2, bottom_y), "Tap to read full breakdown on feed 👆", fill=(255, 255, 255, 240), anchor="mm", font=font_sub)
    draw.text((story_w // 2, bottom_y + 40), "@linpane_legal_services", fill=(244, 196, 78, 240), anchor="mm", font=font_sub)
    
    # Convert to RGB JPEG
    final_rgb = bg_composite.convert("RGB")
    final_rgb.save(output_story_path, "JPEG", quality=95)
    print(f"Saved 1080x1920 Story to: {output_story_path}")

if __name__ == "__main__":
    src = Path("v2/output/BNS_post-01.jpg")
    dst = Path("v2/output/BNS_story-01.jpg")
    create_story_graphic(src, dst)
