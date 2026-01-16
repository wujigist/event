"""
QR Code Service
Generates and manages QR codes for legacy passes
"""

import qrcode
from qrcode.image.styledpil import StyledPilImage
from qrcode.image.styles.moduledrawers import RoundedModuleDrawer
from qrcode.image.styles.colormasks import SolidFillColorMask
import json
from pathlib import Path
from typing import Dict, Any
import os

from ..config import settings


# QR Code configuration
QR_VERSION = 1  # Controls size (1-40)
QR_ERROR_CORRECTION = qrcode.constants.ERROR_CORRECT_H  # High error correction
QR_BOX_SIZE = 10  # Size of each box in pixels
QR_BORDER = 4  # Border size in boxes

# Luxury color scheme
QR_FOREGROUND_COLOR = "#D4AF37"  # Gold
QR_BACKGROUND_COLOR = "#0A0A0A"  # Black


def encode_pass_data(
    pass_number: str,
    member_name: str,
    event_id: str,
    token: str,
    event_date: str = None
) -> str:
    """
    Format pass data into JSON string for QR code
    
    Args:
        pass_number: Legacy pass number
        member_name: Member's full name
        event_id: Event UUID
        token: Legacy pass token
        event_date: Optional event date
        
    Returns:
        JSON string with pass data
    """
    data = {
        "pass_number": pass_number,
        "member": member_name,
        "event_id": str(event_id),
        "token": str(token),
        "type": "paige_inner_circle_pass",
        "version": "1.0"
    }
    
    if event_date:
        data["event_date"] = event_date
    
    return json.dumps(data, separators=(',', ':'))


def generate_qr_code(
    data: str,
    output_path: str = None,
    luxury_style: bool = True
) -> str:
    """
    Generate QR code from pass data
    
    Args:
        data: Data to encode in QR code (JSON string)
        output_path: Path to save QR code image
        luxury_style: If True, uses luxury styling (rounded, gold)
        
    Returns:
        Path to saved QR code image
    """
    # Create QR code instance
    qr = qrcode.QRCode(
        version=QR_VERSION,
        error_correction=QR_ERROR_CORRECTION,
        box_size=QR_BOX_SIZE,
        border=QR_BORDER,
    )
    
    # Add data
    qr.add_data(data)
    qr.make(fit=True)
    
    if luxury_style:
        # Create styled QR code with luxury aesthetics
        img = qr.make_image(
            image_factory=StyledPilImage,
            module_drawer=RoundedModuleDrawer(),
            color_mask=SolidFillColorMask(
                back_color=QR_BACKGROUND_COLOR,
                front_color=QR_FOREGROUND_COLOR
            )
        )
    else:
        # Standard QR code
        img = qr.make_image(
            fill_color=QR_FOREGROUND_COLOR,
            back_color=QR_BACKGROUND_COLOR
        )
    
    # Save QR code
    if output_path:
        # Ensure directory exists
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        img.save(output_path)
        return output_path
    
    return None


def save_qr_code_image(
    pass_number: str,
    member_name: str,
    event_id: str,
    token: str,
    event_date: str = None
) -> Dict[str, str]:
    """
    Generate and save QR code for a legacy pass
    
    Args:
        pass_number: Legacy pass number
        member_name: Member's full name
        event_id: Event UUID
        token: Legacy pass token
        event_date: Optional event date
        
    Returns:
        Dictionary with QR code data and image path
    """
    # Encode pass data
    qr_data = encode_pass_data(
        pass_number=pass_number,
        member_name=member_name,
        event_id=event_id,
        token=token,
        event_date=event_date
    )
    
    # Define output path
    # Format: static/qr_codes/{pass_number}.png
    static_dir = Path("app/static/qr_codes")
    static_dir.mkdir(parents=True, exist_ok=True)
    
    # Sanitize filename
    safe_pass_number = pass_number.replace("/", "-").replace("\\", "-")
    output_filename = f"{safe_pass_number}.png"
    output_path = static_dir / output_filename
    
    # Generate QR code
    generate_qr_code(
        data=qr_data,
        output_path=str(output_path),
        luxury_style=True
    )
    
    return {
        "qr_data": qr_data,
        "qr_image_path": str(output_path),
        "qr_image_url": f"/static/qr_codes/{output_filename}"
    }


def generate_verification_qr(
    token: str,
    verification_url: str = None
) -> str:
    """
    Generate QR code for pass verification (simpler format)
    
    Args:
        token: Legacy pass token
        verification_url: Optional custom verification URL
        
    Returns:
        Path to saved QR code image
    """
    if not verification_url:
        # Default verification URL
        verification_url = f"{settings.FRONTEND_URL}/verify/{token}"
    
    # Define output path
    static_dir = Path("app/static/qr_codes/verification")
    static_dir.mkdir(parents=True, exist_ok=True)
    output_path = static_dir / f"{token}.png"
    
    # Generate simple QR code with URL
    generate_qr_code(
        data=verification_url,
        output_path=str(output_path),
        luxury_style=True
    )
    
    return str(output_path)


def create_test_qr_code(test_data: str = "Paige's Inner Circle - Test QR Code") -> str:
    """
    Create a test QR code for development/testing
    
    Args:
        test_data: Data to encode
        
    Returns:
        Path to test QR code
    """
    static_dir = Path("app/static/qr_codes/test")
    static_dir.mkdir(parents=True, exist_ok=True)
    output_path = static_dir / "test_qr.png"
    
    return generate_qr_code(
        data=test_data,
        output_path=str(output_path),
        luxury_style=True
    )


def decode_qr_data(qr_data_string: str) -> Dict[str, Any]:
    """
    Decode QR code data string back to dictionary
    
    Args:
        qr_data_string: JSON string from QR code
        
    Returns:
        Dictionary with pass data
    """
    try:
        return json.loads(qr_data_string)
    except json.JSONDecodeError:
        return {"error": "Invalid QR data format"}


def validate_qr_data(qr_data: Dict[str, Any]) -> bool:
    """
    Validate that QR code data contains required fields
    
    Args:
        qr_data: Decoded QR data dictionary
        
    Returns:
        True if valid, False otherwise
    """
    required_fields = ["pass_number", "member", "event_id", "token", "type"]
    
    for field in required_fields:
        if field not in qr_data:
            return False
    
    # Check type
    if qr_data.get("type") != "paige_inner_circle_pass":
        return False
    
    return True