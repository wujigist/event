"""
Memories Routes
Post-event features: photo galleries, thank you videos, certificates
These routes are used AFTER the event has happened
"""

from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from sqlalchemy.orm import Session
from typing import Dict, Any, List, Optional
from uuid import UUID
from datetime import datetime

from ...database import get_db
from ...models.member import Member
from ...models.event import Event
from ...models.memory import Memory
from ...models.rsvp import RSVP
from ...api.dependencies import get_current_member, require_admin


router = APIRouter(prefix="/memories", tags=["Memories"])


@router.get("/my-memories", response_model=List[Dict[str, Any]])
async def get_my_memories(
    current_member: Member = Depends(get_current_member),
    db: Session = Depends(get_db)
) -> List[Dict[str, Any]]:
    """
    Get all memories for current member
    
    **Protected Route** - Requires authentication
    
    Shows photo galleries, videos, and certificates from past events
    
    Args:
        current_member: Authenticated member
        db: Database session
        
    Returns:
        List of memories from all events attended
    """
    # Get member's memories
    memories = db.query(Memory).filter(
        Memory.member_id == current_member.id
    ).order_by(Memory.created_at.desc()).all()
    
    result = []
    
    for memory in memories:
        event = db.query(Event).filter(Event.id == memory.event_id).first()
        
        result.append({
            "memory_id": str(memory.id),
            "event": {
                "title": event.title if event else "Unknown Event",
                "date": event.event_date.isoformat() if event else None
            },
            "photo_gallery_url": memory.photo_gallery_url,
            "thank_you_video_url": memory.thank_you_video_url,
            "certificate_pdf_path": memory.certificate_pdf_path,
            "badge_number": memory.badge_number,
            "badge_image_path": memory.badge_image_path,
            "created_at": memory.created_at.isoformat()
        })
    
    return result


@router.get("/event/{event_id}", response_model=Dict[str, Any])
async def get_event_memories(
    event_id: UUID,
    current_member: Member = Depends(get_current_member),
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """
    Get memories for a specific event
    
    **Protected Route** - Requires authentication
    
    Member must have attended the event (RSVP accepted)
    
    Args:
        event_id: Event UUID
        current_member: Authenticated member
        db: Database session
        
    Returns:
        Event memories
        
    Raises:
        HTTPException 404: If memories not found
        HTTPException 403: If member didn't attend
    """
    # Check if member attended event
    rsvp = db.query(RSVP).filter(
        RSVP.member_id == current_member.id,
        RSVP.event_id == event_id,
        RSVP.status == "accepted"
    ).first()
    
    if not rsvp:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You must have attended this event to access memories."
        )
    
    # Get memories
    memory = db.query(Memory).filter(
        Memory.member_id == current_member.id,
        Memory.event_id == event_id
    ).first()
    
    if not memory:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Memories for this event are not yet available. Check back soon!"
        )
    
    # Get event details
    event = db.query(Event).filter(Event.id == event_id).first()
    
    return {
        "event": {
            "title": event.title,
            "date": event.event_date.isoformat()
        },
        "photo_gallery_url": memory.photo_gallery_url,
        "thank_you_video_url": memory.thank_you_video_url,
        "certificate_available": memory.certificate_pdf_path is not None,
        "certificate_pdf_url": f"/static/certificates/{memory.certificate_pdf_path}" if memory.certificate_pdf_path else None,
        "badge": {
            "number": memory.badge_number,
            "image_url": f"/static/badges/{memory.badge_image_path}" if memory.badge_image_path else None
        },
        "message": "Thank you for being part of this unforgettable evening. These memories are yours to cherish forever."
    }


@router.get("/certificate/{event_id}")
async def download_certificate(
    event_id: UUID,
    current_member: Member = Depends(get_current_member),
    db: Session = Depends(get_db)
):
    """
    Download event attendance certificate
    
    **Protected Route** - Requires authentication
    
    Args:
        event_id: Event UUID
        current_member: Authenticated member
        db: Database session
        
    Returns:
        PDF file download
        
    Raises:
        HTTPException 404: If certificate not found
        HTTPException 403: If member didn't attend
    """
    from fastapi.responses import FileResponse
    from pathlib import Path
    
    # Get memory record
    memory = db.query(Memory).filter(
        Memory.member_id == current_member.id,
        Memory.event_id == event_id
    ).first()
    
    if not memory:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Certificate not found."
        )
    
    if not memory.certificate_pdf_path:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Certificate not yet generated. Please check back later."
        )
    
    # Check file exists
    cert_path = Path(f"app/static/certificates/{memory.certificate_pdf_path}")
    if not cert_path.exists():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Certificate file not found on server."
        )
    
    # Get event for filename
    event = db.query(Event).filter(Event.id == event_id).first()
    
    return FileResponse(
        path=str(cert_path),
        media_type="application/pdf",
        filename=f"Certificate_{event.title.replace(' ', '_')}_{current_member.full_name.replace(' ', '_')}.pdf"
    )


@router.get("/gallery/{event_id}", response_model=Dict[str, Any])
async def get_photo_gallery(
    event_id: UUID,
    current_member: Member = Depends(get_current_member),
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """
    Get photo gallery link for event
    
    **Protected Route** - Requires authentication
    
    Args:
        event_id: Event UUID
        current_member: Authenticated member
        db: Database session
        
    Returns:
        Photo gallery information
        
    Raises:
        HTTPException 404: If gallery not available
    """
    # Get memory record
    memory = db.query(Memory).filter(
        Memory.member_id == current_member.id,
        Memory.event_id == event_id
    ).first()
    
    if not memory or not memory.photo_gallery_url:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Photo gallery not yet available for this event."
        )
    
    # Get event
    event = db.query(Event).filter(Event.id == event_id).first()
    
    return {
        "event_title": event.title,
        "event_date": event.event_date.isoformat(),
        "gallery_url": memory.photo_gallery_url,
        "message": "Relive the magic of our evening together through these beautiful moments."
    }


# ============================================================================
# ADMIN ROUTES - Create/Manage Memories
# ============================================================================

@router.post("/create/{event_id}", status_code=status.HTTP_201_CREATED)
async def create_event_memories(
    event_id: UUID,
    photo_gallery_url: Optional[str] = None,
    thank_you_video_url: Optional[str] = None,
    current_admin: Member = Depends(require_admin),
    db: Session = Depends(get_db)
) -> Dict[str, str]:
    """
    Create memory records for all attendees of an event (Admin Only)
    
    **Protected Route** - Requires admin authentication
    
    Run this after an event to create memory records for all who attended
    
    Args:
        event_id: Event UUID
        photo_gallery_url: Optional URL to photo gallery
        thank_you_video_url: Optional URL to thank you video
        current_admin: Authenticated admin
        db: Database session
        
    Returns:
        Success message with count of memories created
        
    Raises:
        HTTPException 404: If event not found
    """
    # Get event
    event = db.query(Event).filter(Event.id == event_id).first()
    
    if not event:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Event not found."
        )
    
    # Get all attendees (accepted RSVPs)
    attendees = db.query(RSVP).filter(
        RSVP.event_id == event_id,
        RSVP.status == "accepted"
    ).all()
    
    memories_created = 0
    badge_counter = 1
    
    for rsvp in attendees:
        # Check if memory already exists
        existing = db.query(Memory).filter(
            Memory.member_id == rsvp.member_id,
            Memory.event_id == event_id
        ).first()
        
        if existing:
            continue  # Skip if already exists
        
        # Create memory record
        memory = Memory(
            member_id=rsvp.member_id,
            event_id=event_id,
            photo_gallery_url=photo_gallery_url,
            thank_you_video_url=thank_you_video_url,
            badge_number=badge_counter
        )
        
        db.add(memory)
        memories_created += 1
        badge_counter += 1
    
    db.commit()
    
    return {
        "message": f"Created {memories_created} memory records for {event.title}",
        "event_id": str(event_id),
        "total_attendees": len(attendees),
        "memories_created": memories_created
    }


@router.put("/{memory_id}", response_model=Dict[str, str])
async def update_memory(
    memory_id: UUID,
    photo_gallery_url: Optional[str] = None,
    thank_you_video_url: Optional[str] = None,
    certificate_pdf_path: Optional[str] = None,
    badge_image_path: Optional[str] = None,
    current_admin: Member = Depends(require_admin),
    db: Session = Depends(get_db)
) -> Dict[str, str]:
    """
    Update memory record (Admin Only)
    
    **Protected Route** - Requires admin authentication
    
    Args:
        memory_id: Memory UUID
        photo_gallery_url: Optional new gallery URL
        thank_you_video_url: Optional new video URL
        certificate_pdf_path: Optional certificate path
        badge_image_path: Optional badge image path
        current_admin: Authenticated admin
        db: Database session
        
    Returns:
        Success message
        
    Raises:
        HTTPException 404: If memory not found
    """
    # Get memory
    memory = db.query(Memory).filter(Memory.id == memory_id).first()
    
    if not memory:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Memory record not found."
        )
    
    # Update fields if provided
    if photo_gallery_url is not None:
        memory.photo_gallery_url = photo_gallery_url
    
    if thank_you_video_url is not None:
        memory.thank_you_video_url = thank_you_video_url
    
    if certificate_pdf_path is not None:
        memory.certificate_pdf_path = certificate_pdf_path
    
    if badge_image_path is not None:
        memory.badge_image_path = badge_image_path
    
    db.commit()
    
    return {
        "message": "Memory record updated successfully",
        "memory_id": str(memory_id)
    }


@router.get("/admin/event/{event_id}/all", response_model=List[Dict[str, Any]])
async def get_all_event_memories_admin(
    event_id: UUID,
    current_admin: Member = Depends(require_admin),
    db: Session = Depends(get_db)
) -> List[Dict[str, Any]]:
    """
    Get all memory records for an event (Admin Only)
    
    **Protected Route** - Requires admin authentication
    
    Args:
        event_id: Event UUID
        current_admin: Authenticated admin
        db: Database session
        
    Returns:
        List of all memories for the event
    """
    # Get all memories for event
    memories = db.query(Memory).filter(
        Memory.event_id == event_id
    ).all()
    
    result = []
    
    for memory in memories:
        member = db.query(Member).filter(Member.id == memory.member_id).first()
        
        result.append({
            "memory_id": str(memory.id),
            "member": {
                "name": member.full_name if member else "Unknown",
                "email": member.email if member else "Unknown"
            },
            "photo_gallery_url": memory.photo_gallery_url,
            "thank_you_video_url": memory.thank_you_video_url,
            "has_certificate": memory.certificate_pdf_path is not None,
            "badge_number": memory.badge_number,
            "has_badge_image": memory.badge_image_path is not None,
            "created_at": memory.created_at.isoformat()
        })
    
    return result


@router.delete("/{memory_id}")
async def delete_memory(
    memory_id: UUID,
    current_admin: Member = Depends(require_admin),
    db: Session = Depends(get_db)
) -> Dict[str, str]:
    """
    Delete memory record (Admin Only)
    
    **Protected Route** - Requires admin authentication
    
    Args:
        memory_id: Memory UUID
        current_admin: Authenticated admin
        db: Database session
        
    Returns:
        Success message
        
    Raises:
        HTTPException 404: If memory not found
    """
    # Get memory
    memory = db.query(Memory).filter(Memory.id == memory_id).first()
    
    if not memory:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Memory record not found."
        )
    
    db.delete(memory)
    db.commit()
    
    return {
        "message": "Memory record deleted successfully",
        "memory_id": str(memory_id)
    }