"""
Legacy Pass Generator
Creates beautiful, luxury-styled legacy pass images (front and back)
"""

from PIL import Image, ImageDraw, ImageFont, ImageFilter
from pathlib import Path
from typing import Tuple, Optional
import os

from ..config import settings


# Pass dimensions (credit card size ratio, scaled up)
PASS_WIDTH = 1200
PASS_HEIGHT = 757  # Maintains credit card ratio (3.370" x 2.125")

# Colors (luxury palette)
COLOR_BLACK = "#0A0A0A"
COLOR_GOLD = "#D4AF37"
COLOR_CHAMPAGNE = "#F7E7CE"
COLOR_OFF_WHITE = "#F5F5F5"
COLOR_DARK_GOLD = "#8B7328"

# Fonts (fallback to default if custom not available)
FONT_PATH_SERIF = "app/static/assets/fonts"
FONT_PATH_SANS = "app/static/assets/fonts"


def get_font(size: int, bold: bool = False, serif: bool = True):
    """Get font with fallback to default"""
    try:
        if serif:
            if bold:
                return ImageFont.truetype(f"{FONT_PATH_SERIF}/luxury-serif-bold.ttf", size)
            return ImageFont.truetype(f"{FONT_PATH_SERIF}/luxury-serif.ttf", size)
        else:
            if bold:
                return ImageFont.truetype(f"{FONT_PATH_SANS}/elegant-sans-bold.ttf", size)
            return ImageFont.truetype(f"{FONT_PATH_SANS}/elegant-sans.ttf", size)
    except:
        # Fallback to default PIL font
        return ImageFont.load_default()


def create_pass_front(
    member_name: str,
    pass_number: str,
    membership_tier: str = "Inner Circle",
    output_path: str = None
) -> str:
    """
    Generate the front side of the legacy pass
    
    Args:
        member_name: Member's full name
        pass_number: Pass number (e.g., "INNER-CIRCLE-#001")
        membership_tier: Membership tier name
        output_path: Path to save image
        
    Returns:
        Path to saved image
    """
    # Create image with black background
    img = Image.new('RGB', (PASS_WIDTH, PASS_HEIGHT), COLOR_BLACK)
    draw = ImageDraw.Draw(img)
    
    # Add gold border
    border_width = 8
    draw.rectangle(
        [border_width, border_width, PASS_WIDTH - border_width, PASS_HEIGHT - border_width],
        outline=COLOR_GOLD,
        width=border_width
    )
    
    # Add subtle pattern/texture (optional - diagonal lines)
    for i in range(0, PASS_WIDTH + PASS_HEIGHT, 40):
        draw.line(
            [(i, 0), (i - PASS_HEIGHT, PASS_HEIGHT)],
            fill=COLOR_DARK_GOLD,
            width=1
        )
    
    # Title: "PAIGE'S INNER CIRCLE"
    title_font = get_font(48, bold=True, serif=True)
    title_text = "PAIGE'S INNER CIRCLE"
    title_bbox = draw.textbbox((0, 0), title_text, font=title_font)
    title_width = title_bbox[2] - title_bbox[0]
    title_x = (PASS_WIDTH - title_width) // 2
    draw.text((title_x, 80), title_text, fill=COLOR_GOLD, font=title_font)
    
    # Subtitle: "Legacy Pass"
    subtitle_font = get_font(28, bold=False, serif=True)
    subtitle_text = "Legacy Pass"
    subtitle_bbox = draw.textbbox((0, 0), subtitle_text, font=subtitle_font)
    subtitle_width = subtitle_bbox[2] - subtitle_bbox[0]
    subtitle_x = (PASS_WIDTH - subtitle_width) // 2
    draw.text((subtitle_x, 150), subtitle_text, fill=COLOR_CHAMPAGNE, font=subtitle_font)
    
    # Member name (centered, larger)
    name_font = get_font(52, bold=True, serif=False)
    name_bbox = draw.textbbox((0, 0), member_name.upper(), font=name_font)
    name_width = name_bbox[2] - name_bbox[0]
    name_x = (PASS_WIDTH - name_width) // 2
    draw.text((name_x, 320), member_name.upper(), fill=COLOR_OFF_WHITE, font=name_font)
    
    # Pass number (smaller, below name)
    pass_num_font = get_font(24, bold=False, serif=False)
    pass_num_bbox = draw.textbbox((0, 0), pass_number, font=pass_num_font)
    pass_num_width = pass_num_bbox[2] - pass_num_bbox[0]
    pass_num_x = (PASS_WIDTH - pass_num_width) // 2
    draw.text((pass_num_x, 400), pass_number, fill=COLOR_CHAMPAGNE, font=pass_num_font)
    
    # Membership tier badge (bottom)
    badge_font = get_font(20, bold=True, serif=False)
    badge_text = f"∴ {membership_tier.upper()} ∴"
    badge_bbox = draw.textbbox((0, 0), badge_text, font=badge_font)
    badge_width = badge_bbox[2] - badge_bbox[0]
    badge_x = (PASS_WIDTH - badge_width) // 2
    draw.text((badge_x, 520), badge_text, fill=COLOR_GOLD, font=badge_font)
    
    # "Founding Member" text (if applicable)
    if "founding" in membership_tier.lower():
        founding_font = get_font(18, bold=False, serif=True)
        founding_text = "Founding Member"
        founding_bbox = draw.textbbox((0, 0), founding_text, font=founding_font)
        founding_width = founding_bbox[2] - founding_bbox[0]
        founding_x = (PASS_WIDTH - founding_width) // 2
        draw.text((founding_x, 570), founding_text, fill=COLOR_CHAMPAGNE, font=founding_font)
    
    # Signature line at bottom
    signature_font = get_font(22, bold=False, serif=True)
    signature_text = "Paige"
    draw.text((100, 650), signature_text, fill=COLOR_GOLD, font=signature_font)
    
    # Draw signature line
    draw.line([(90, 645), (320, 645)], fill=COLOR_GOLD, width=2)
    
    # Save image
    if output_path:
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        img.save(output_path, quality=95)
        return output_path
    
    return None


def create_pass_back(
    pass_number: str,
    event_name: str,
    event_date: str,
    venue_name: str,
    token: str,
    qr_code_path: str,
    output_path: str = None
) -> str:
    """
    Generate the back side of the legacy pass
    
    Args:
        pass_number: Pass number
        event_name: Event title
        event_date: Event date string
        venue_name: Venue name
        token: Legacy pass token
        qr_code_path: Path to QR code image
        output_path: Path to save image
        
    Returns:
        Path to saved image
    """
    # Create image with black background
    img = Image.new('RGB', (PASS_WIDTH, PASS_HEIGHT), COLOR_BLACK)
    draw = ImageDraw.Draw(img)
    
    # Add gold border
    border_width = 8
    draw.rectangle(
        [border_width, border_width, PASS_WIDTH - border_width, PASS_HEIGHT - border_width],
        outline=COLOR_GOLD,
        width=border_width
    )
    
    # Load and paste QR code (centered, top portion)
    try:
        qr_img = Image.open(qr_code_path)
        qr_size = 280
        qr_img = qr_img.resize((qr_size, qr_size), Image.Resampling.LANCZOS)
        qr_x = (PASS_WIDTH - qr_size) // 2
        qr_y = 60
        img.paste(qr_img, (qr_x, qr_y))
    except:
        pass  # Skip if QR code not available
    
    # "SCAN FOR ENTRY" text
    scan_font = get_font(24, bold=True, serif=False)
    scan_text = "SCAN FOR ENTRY"
    scan_bbox = draw.textbbox((0, 0), scan_text, font=scan_font)
    scan_width = scan_bbox[2] - scan_bbox[0]
    scan_x = (PASS_WIDTH - scan_width) // 2
    draw.text((scan_x, 360), scan_text, fill=COLOR_GOLD, font=scan_font)
    
    # Event details (bottom portion)
    details_y = 430
    details_font = get_font(20, bold=False, serif=False)
    details_font_bold = get_font(20, bold=True, serif=False)
    
    # Event name
    draw.text((100, details_y), "EVENT:", fill=COLOR_GOLD, font=details_font_bold)
    draw.text((100, details_y + 30), event_name, fill=COLOR_OFF_WHITE, font=details_font)
    
    # Event date
    draw.text((100, details_y + 80), "DATE:", fill=COLOR_GOLD, font=details_font_bold)
    draw.text((100, details_y + 110), event_date, fill=COLOR_OFF_WHITE, font=details_font)
    
    # Venue
    draw.text((100, details_y + 160), "VENUE:", fill=COLOR_GOLD, font=details_font_bold)
    draw.text((100, details_y + 190), venue_name, fill=COLOR_OFF_WHITE, font=details_font)
    
    # Pass number and token (very small, bottom right)
    small_font = get_font(12, bold=False, serif=False)
    draw.text((PASS_WIDTH - 350, PASS_HEIGHT - 50), f"Pass: {pass_number}", fill=COLOR_CHAMPAGNE, font=small_font)
    draw.text((PASS_WIDTH - 350, PASS_HEIGHT - 30), f"Token: {str(token)[:16]}...", fill=COLOR_CHAMPAGNE, font=small_font)
    
    # "Not Transferable" notice
    notice_font = get_font(14, bold=True, serif=False)
    notice_text = "NOT TRANSFERABLE"
    notice_bbox = draw.textbbox((0, 0), notice_text, font=notice_font)
    notice_width = notice_bbox[2] - notice_bbox[0]
    notice_x = (PASS_WIDTH - notice_width) // 2
    draw.text((notice_x, PASS_HEIGHT - 35), notice_text, fill=COLOR_GOLD, font=notice_font)
    
    # Save image
    if output_path:
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        img.save(output_path, quality=95)
        return output_path
    
    return None


def create_blurred_preview(
    original_image_path: str,
    output_path: str = None,
    blur_radius: int = 25
) -> str:
    """
    Create blurred preview of legacy pass for pre-payment view
    
    Args:
        original_image_path: Path to original pass image
        output_path: Path to save blurred image
        blur_radius: Blur intensity (default 25)
        
    Returns:
        Path to blurred image
    """
    try:
        # Open original image
        img = Image.open(original_image_path)
        
        # Apply Gaussian blur
        blurred = img.filter(ImageFilter.GaussianBlur(radius=blur_radius))
        
        # Add watermark overlay
        overlay = Image.new('RGBA', blurred.size, (0, 0, 0, 128))
        blurred_rgba = blurred.convert('RGBA')
        blurred_with_overlay = Image.alpha_composite(blurred_rgba, overlay)
        
        # Add "PAYMENT REQUIRED" text
        draw = ImageDraw.Draw(blurred_with_overlay)
        watermark_font = get_font(60, bold=True, serif=False)
        watermark_text = "PAYMENT REQUIRED"
        
        # Get text size
        bbox = draw.textbbox((0, 0), watermark_text, font=watermark_font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        
        # Center text
        text_x = (PASS_WIDTH - text_width) // 2
        text_y = (PASS_HEIGHT - text_height) // 2
        
        # Draw text with outline for visibility
        outline_color = (10, 10, 10, 255)
        fill_color = (212, 175, 55, 255)  # Gold
        
        # Draw outline
        for adj in range(-3, 4):
            for adj2 in range(-3, 4):
                draw.text((text_x + adj, text_y + adj2), watermark_text, font=watermark_font, fill=outline_color)
        
        # Draw main text
        draw.text((text_x, text_y), watermark_text, font=watermark_font, fill=fill_color)
        
        # Convert back to RGB
        final_image = blurred_with_overlay.convert('RGB')
        
        # Save
        if output_path:
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            final_image.save(output_path, quality=95)
            return output_path
        
    except Exception as e:
        print(f"Error creating blurred preview: {e}")
        return None
    
    return None


def save_pass_assets(
    member_name: str,
    pass_number: str,
    membership_tier: str,
    event_name: str,
    event_date: str,
    venue_name: str,
    token: str,
    qr_code_path: str
) -> dict:
    """
    Generate and save all legacy pass assets
    
    Args:
        member_name: Member's full name
        pass_number: Pass number
        membership_tier: Membership tier
        event_name: Event title
        event_date: Event date string
        venue_name: Venue name
        token: Legacy pass token
        qr_code_path: Path to QR code image
        
    Returns:
        Dictionary with all asset paths
    """
    # Create static directory
    static_dir = Path("app/static/legacy_passes")
    static_dir.mkdir(parents=True, exist_ok=True)
    
    # Sanitize pass number for filename
    safe_pass_num = pass_number.replace("/", "-").replace("\\", "-").replace("#", "")
    
    # Generate front
    front_path = static_dir / f"{safe_pass_num}_front.png"
    create_pass_front(
        member_name=member_name,
        pass_number=pass_number,
        membership_tier=membership_tier,
        output_path=str(front_path)
    )
    
    # Generate back
    back_path = static_dir / f"{safe_pass_num}_back.png"
    create_pass_back(
        pass_number=pass_number,
        event_name=event_name,
        event_date=event_date,
        venue_name=venue_name,
        token=token,
        qr_code_path=qr_code_path,
        output_path=str(back_path)
    )
    
    # Generate blurred previews
    front_blurred_path = static_dir / f"{safe_pass_num}_front_blurred.png"
    back_blurred_path = static_dir / f"{safe_pass_num}_back_blurred.png"
    
    create_blurred_preview(str(front_path), str(front_blurred_path))
    create_blurred_preview(str(back_path), str(back_blurred_path))
    
    return {
        "front_path": str(front_path),
        "back_path": str(back_path),
        "front_blurred_path": str(front_blurred_path),
        "back_blurred_path": str(back_blurred_path),
        "front_url": f"/static/legacy_passes/{safe_pass_num}_front.png",
        "back_url": f"/static/legacy_passes/{safe_pass_num}_back.png",
        "front_blurred_url": f"/static/legacy_passes/{safe_pass_num}_front_blurred.png",
        "back_blurred_url": f"/static/legacy_passes/{safe_pass_num}_back_blurred.png"
    }