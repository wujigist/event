"""
Event Routes
Handles event information, details, amenities, and schedules
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Dict, Any
from uuid import UUID

from ...database import get_db
from ...models.event import Event
from ...models.member import Member
from ...schemas.event import (
    EventResponse,
    EventDetail,
    EventTeaser
)
from ...api.dependencies import get_current_member


router = APIRouter(prefix="/events", tags=["Events"])


@router.get("/current", response_model=EventTeaser)
async def get_current_event(
    db: Session = Depends(get_db)
) -> EventTeaser:
    """
    Get current active event (public teaser)
    Returns limited information for landing page
    
    **Public Endpoint** - No authentication required
    
    This endpoint shows just enough to intrigue visitors
    without revealing exclusive details
    
    Args:
        db: Database session
        
    Returns:
        Event teaser with limited information
        
    Raises:
        HTTPException 404: If no active event found
    """
    # Get current active event
    event = db.query(Event).filter(Event.is_active == True).first()
    
    if not event:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No active event at this moment. Stay tuned for future exclusive experiences."
        )
    
    # Return limited teaser information
    return EventTeaser.model_validate(event)


@router.get("/{event_id}", response_model=EventDetail)
async def get_event_details(
    event_id: UUID,
    current_member: Member = Depends(get_current_member),
    db: Session = Depends(get_db)
) -> EventDetail:
    """
    Get complete event details
    Returns full luxury experience information
    
    **Protected Route** - Requires authentication
    
    Members who have accessed their invitation can view:
    - Complete event description
    - Venue details and ambiance
    - Full schedule timeline
    - Luxury amenities list
    - Dress code and theme
    - Special instructions
    
    Args:
        event_id: Event UUID
        current_member: Authenticated member
        db: Database session
        
    Returns:
        Complete event details
        
    Raises:
        HTTPException 404: If event not found
        HTTPException 403: If event is inactive
    """
    # Get event
    event = db.query(Event).filter(Event.id == event_id).first()
    
    if not event:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="This event could not be found. Please contact support if you believe this is an error."
        )
    
    if not event.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="This event is no longer active. Thank you for your interest in past experiences."
        )
    
    # Return full event details
    return EventDetail.model_validate(event)


@router.get("/{event_id}/amenities", response_model=Dict[str, Any])
async def get_event_amenities(
    event_id: UUID,
    current_member: Member = Depends(get_current_member),
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """
    Get detailed amenities list
    Organized by category for elegant presentation
    
    **Protected Route** - Requires authentication
    
    Returns luxury amenities including:
    - VIP Lounge Access
    - Culinary Experience
    - Services & Comfort
    - Exclusive Access Areas
    - Entertainment & Activities
    
    Args:
        event_id: Event UUID
        current_member: Authenticated member
        db: Database session
        
    Returns:
        Categorized amenities list
        
    Raises:
        HTTPException 404: If event not found
    """
    # Get event
    event = db.query(Event).filter(
        Event.id == event_id,
        Event.is_active == True
    ).first()
    
    if not event:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Event not found."
        )
    
    # Get amenities from event (stored as JSON)
    amenities = event.amenities or {}
    
    # If amenities is empty, provide default luxury amenities
    if not amenities:
        amenities = {
            "vip_lounge": [
                "Private VIP lounge with premium seating",
                "Dedicated concierge service",
                "Complimentary coat check",
                "Premium bar with signature cocktails"
            ],
            "culinary": [
                "Gourmet hors d'oeuvres stations",
                "Artisan dessert bar",
                "Premium wine and champagne selection",
                "Custom dietary accommodations"
            ],
            "services": [
                "Professional photography",
                "Valet parking service",
                "On-site event coordinator",
                "Express bag check"
            ],
            "exclusive_access": [
                "Backstage tour opportunity",
                "Meet & greet with Paige",
                "Priority seating assignment",
                "Access to private viewing areas"
            ],
            "entertainment": [
                "Live musical performance",
                "Interactive experiences",
                "Photo booth with luxury props",
                "Surprise entertainment acts"
            ]
        }
    
    return {
        "event_id": str(event_id),
        "event_name": event.title,
        "amenities": amenities,
        "total_categories": len(amenities),
        "description": "Every detail has been carefully curated to ensure an unforgettable luxury experience."
    }


@router.get("/{event_id}/schedule", response_model=Dict[str, Any])
async def get_event_schedule(
    event_id: UUID,
    current_member: Member = Depends(get_current_member),
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """
    Get detailed event schedule timeline
    Shows time slots with activities
    
    **Protected Route** - Requires authentication
    
    Returns the complete event timeline from arrival to departure
    
    Args:
        event_id: Event UUID
        current_member: Authenticated member
        db: Database session
        
    Returns:
        Event schedule with timeline
        
    Raises:
        HTTPException 404: If event not found
    """
    # Get event
    event = db.query(Event).filter(
        Event.id == event_id,
        Event.is_active == True
    ).first()
    
    if not event:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Event not found."
        )
    
    # Get schedule from event (stored as JSON)
    schedule = event.schedule or {}
    
    # If schedule is empty, provide default luxury event schedule
    if not schedule:
        schedule = {
            "timeline": [
                {
                    "time": "6:30 PM",
                    "title": "Red Carpet Arrival",
                    "description": "VIP check-in and welcome cocktails",
                    "duration": "30 minutes",
                    "type": "arrival"
                },
                {
                    "time": "7:00 PM",
                    "title": "Cocktail Hour",
                    "description": "Networking and hors d'oeuvres in the VIP lounge",
                    "duration": "60 minutes",
                    "type": "social"
                },
                {
                    "time": "8:00 PM",
                    "title": "Formal Program Begins",
                    "description": "Welcome address and special presentations",
                    "duration": "45 minutes",
                    "type": "program"
                },
                {
                    "time": "8:45 PM",
                    "title": "Dinner Service",
                    "description": "Five-course gourmet dinner experience",
                    "duration": "90 minutes",
                    "type": "dining"
                },
                {
                    "time": "10:15 PM",
                    "title": "Entertainment & Dancing",
                    "description": "Live performance and celebration",
                    "duration": "75 minutes",
                    "type": "entertainment"
                },
                {
                    "time": "11:30 PM",
                    "title": "Farewell & Gift Distribution",
                    "description": "Thank you remarks and commemorative gifts",
                    "duration": "30 minutes",
                    "type": "closing"
                }
            ],
            "notes": [
                "Schedule is subject to minor adjustments",
                "All times are in Eastern Standard Time",
                "Please arrive no later than 6:45 PM"
            ]
        }
    
    return {
        "event_id": str(event_id),
        "event_name": event.title,
        "event_date": event.event_date.strftime("%B %d, %Y"),
        "event_time": event.event_time,
        "schedule": schedule,
        "venue": {
            "name": event.venue_name,
            "address": event.venue_address
        }
    }


@router.get("/", response_model=List[EventResponse])
async def list_events(
    current_member: Member = Depends(get_current_member),
    db: Session = Depends(get_db),
    include_inactive: bool = False
) -> List[EventResponse]:
    """
    List all events
    Optionally include inactive events
    
    **Protected Route** - Requires authentication
    
    Args:
        current_member: Authenticated member
        db: Database session
        include_inactive: Whether to include inactive events
        
    Returns:
        List of events
    """
    # Build query
    query = db.query(Event)
    
    if not include_inactive:
        query = query.filter(Event.is_active == True)
    
    # Get all events
    events = query.order_by(Event.event_date.desc()).all()
    
    return [EventResponse.model_validate(event) for event in events]


@router.get("/{event_id}/summary", response_model=Dict[str, Any])
async def get_event_summary(
    event_id: UUID,
    current_member: Member = Depends(get_current_member),
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """
    Get event summary for dashboard
    Quick overview of essential details
    
    **Protected Route** - Requires authentication
    
    Args:
        event_id: Event UUID
        current_member: Authenticated member
        db: Database session
        
    Returns:
        Event summary
        
    Raises:
        HTTPException 404: If event not found
    """
    # Get event
    event = db.query(Event).filter(
        Event.id == event_id,
        Event.is_active == True
    ).first()
    
    if not event:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Event not found."
        )
    
    # Create summary
    summary = {
        "id": str(event.id),
        "title": event.title,
        "subtitle": event.subtitle,
        "date": event.event_date.strftime("%B %d, %Y"),
        "time": event.event_time,
        "venue": event.venue_name,
        "dress_code": event.dress_code,
        "theme": event.theme,
        "preview": event.description[:200] + "..." if len(event.description) > 200 else event.description
    }
    
    return summary