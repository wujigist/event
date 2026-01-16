"""
PDF Generator Service
Creates downloadable PDF versions of legacy passes
"""

from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
from PIL import Image
from pathlib import Path
import os
from typing import Optional


def create_legacy_pass_pdf(
    front_image_path: str,
    back_image_path: str,
    output_path: str = None,
    member_name: str = None,
    pass_number: str = None
) -> str:
    """
    Create a PDF combining front and back of legacy pass
    
    Args:
        front_image_path: Path to front pass image
        back_image_path: Path to back pass image
        output_path: Path to save PDF
        member_name: Optional member name for metadata
        pass_number: Optional pass number for metadata
        
    Returns:
        Path to saved PDF
    """
    # Create PDF
    if not output_path:
        output_path = "legacy_pass.pdf"
    
    # Ensure directory exists
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    # Create canvas
    c = canvas.Canvas(output_path, pagesize=letter)
    page_width, page_height = letter
    
    # Set metadata
    c.setTitle(f"Legacy Pass - {pass_number or 'Inner Circle'}")
    c.setAuthor("Paige's Inner Circle")
    c.setSubject(f"Legacy Pass for {member_name or 'VIP Member'}")
    
    # Page 1: Front of pass
    c.setFont("Helvetica-Bold", 16)
    c.drawString(inch, page_height - inch, "Paige's Inner Circle - Legacy Pass")
    
    try:
        # Load and add front image (centered)
        img_front = ImageReader(front_image_path)
        
        # Calculate dimensions to fit page while maintaining aspect ratio
        img_width = 6 * inch  # 6 inches wide
        img_height = img_width * (757 / 1200)  # Maintain aspect ratio
        
        # Center horizontally
        x_position = (page_width - img_width) / 2
        y_position = page_height - 2.5 * inch - img_height
        
        c.drawImage(
            front_image_path,
            x_position,
            y_position,
            width=img_width,
            height=img_height,
            preserveAspectRatio=True
        )
        
    except Exception as e:
        c.setFont("Helvetica", 12)
        c.drawString(inch, page_height - 3 * inch, f"[Front image unavailable: {e}]")
    
    # Instructions at bottom
    c.setFont("Helvetica", 10)
    c.drawString(inch, inch, "Present this pass at the event entrance for verification.")
    
    # Page 2: Back of pass
    c.showPage()
    c.setFont("Helvetica-Bold", 16)
    c.drawString(inch, page_height - inch, "Legacy Pass - Back")
    
    try:
        # Load and add back image
        img_width = 6 * inch
        img_height = img_width * (757 / 1200)
        x_position = (page_width - img_width) / 2
        y_position = page_height - 2.5 * inch - img_height
        
        c.drawImage(
            back_image_path,
            x_position,
            y_position,
            width=img_width,
            height=img_height,
            preserveAspectRatio=True
        )
        
    except Exception as e:
        c.setFont("Helvetica", 12)
        c.drawString(inch, page_height - 3 * inch, f"[Back image unavailable: {e}]")
    
    # Instructions
    c.setFont("Helvetica", 10)
    c.drawString(inch, inch + 0.5 * inch, "Scan the QR code at the event for quick entry.")
    c.drawString(inch, inch, "This pass is non-transferable and valid only for the registered member.")
    
    # Save PDF
    c.save()
    
    return output_path


def add_watermark(
    pdf_path: str,
    watermark_text: str = "VERIFIED",
    output_path: str = None
) -> str:
    """
    Add watermark to PDF (for verified passes)
    
    Args:
        pdf_path: Path to original PDF
        watermark_text: Text to watermark
        output_path: Path to save watermarked PDF
        
    Returns:
        Path to watermarked PDF
    """
    # This is a simplified version - full implementation would use PyPDF2
    # For now, return original path
    return pdf_path


def generate_pass_pdf(
    front_path: str,
    back_path: str,
    pass_number: str,
    member_name: str
) -> str:
    """
    Generate complete PDF for legacy pass
    
    Args:
        front_path: Path to front image
        back_path: Path to back image
        pass_number: Pass number
        member_name: Member name
        
    Returns:
        Path to generated PDF
    """
    # Create PDF directory
    pdf_dir = Path("app/static/legacy_passes/pdf")
    pdf_dir.mkdir(parents=True, exist_ok=True)
    
    # Sanitize filename
    safe_pass_num = pass_number.replace("/", "-").replace("\\", "-").replace("#", "")
    pdf_path = pdf_dir / f"{safe_pass_num}.pdf"
    
    # Generate PDF
    create_legacy_pass_pdf(
        front_image_path=front_path,
        back_image_path=back_path,
        output_path=str(pdf_path),
        member_name=member_name,
        pass_number=pass_number
    )
    
    return str(pdf_path)


def create_wallet_pass_data(
    pass_number: str,
    member_name: str,
    event_name: str,
    event_date: str,
    venue: str,
    qr_data: str
) -> dict:
    """
    Format data for Apple/Google Wallet integration
    
    Args:
        pass_number: Legacy pass number
        member_name: Member's name
        event_name: Event title
        event_date: Event date
        venue: Venue name
        qr_data: QR code data
        
    Returns:
        Dictionary with wallet pass data structure
    """
    # This is a template - actual implementation requires wallet pass libraries
    wallet_data = {
        "formatVersion": 1,
        "passTypeIdentifier": "pass.com.paigeinnercircle.legacy",
        "serialNumber": pass_number,
        "teamIdentifier": "PAIGE",
        "organizationName": "Paige's Inner Circle",
        "description": f"Legacy Pass for {member_name}",
        "logoText": "Paige's Inner Circle",
        "foregroundColor": "rgb(245, 245, 245)",  # Off-white
        "backgroundColor": "rgb(10, 10, 10)",  # Black
        "labelColor": "rgb(212, 175, 55)",  # Gold
        "eventTicket": {
            "primaryFields": [
                {
                    "key": "member",
                    "label": "MEMBER",
                    "value": member_name
                }
            ],
            "secondaryFields": [
                {
                    "key": "event",
                    "label": "EVENT",
                    "value": event_name
                }
            ],
            "auxiliaryFields": [
                {
                    "key": "date",
                    "label": "DATE",
                    "value": event_date
                },
                {
                    "key": "venue",
                    "label": "VENUE",
                    "value": venue
                }
            ],
            "backFields": [
                {
                    "key": "passNumber",
                    "label": "PASS NUMBER",
                    "value": pass_number
                },
                {
                    "key": "terms",
                    "label": "TERMS",
                    "value": "This pass is non-transferable and valid only for the registered member."
                }
            ]
        },
        "barcode": {
            "message": qr_data,
            "format": "PKBarcodeFormatQR",
            "messageEncoding": "iso-8859-1"
        }
    }
    
    return wallet_data


def format_for_wallet(
    pass_data: dict,
    output_format: str = "apple"
) -> Optional[str]:
    """
    Generate Apple/Google Wallet pass file
    
    Args:
        pass_data: Wallet pass data dictionary
        output_format: "apple" or "google"
        
    Returns:
        Path to wallet pass file or None
    """
    # This would require additional libraries:
    # - For Apple: passbook library to create .pkpass files
    # - For Google: Google Pay API
    # Placeholder implementation
    
    print(f"Wallet pass generation ({output_format}) - requires additional setup")
    return None