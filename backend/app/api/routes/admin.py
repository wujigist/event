"""
Admin Routes
Administrative functions for managing members, events, RSVPs, and payments
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import Dict, Any, List, Optional
from uuid import UUID
from datetime import datetime

from ...database import get_db
from ...models.member import Member
from ...models.event import Event
from ...models.rsvp import RSVP
from ...models.legacy_pass import LegacyPass
from ...models.payment import Payment
from ...schemas.member import MemberCreate, MemberResponse, MemberUpdate
from ...schemas.event import EventCreate, EventResponse, EventUpdate
from ...api.dependencies import get_current_member, require_admin, get_pagination, PaginationParams


router = APIRouter(prefix="/admin", tags=["Admin"])


# ============================================================================
# DASHBOARD & STATISTICS
# ============================================================================

@router.get("/dashboard", response_model=Dict[str, Any])
async def get_admin_dashboard(
    current_admin: Member = Depends(require_admin),
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """
    Get admin dashboard with key statistics
    
    **Protected Route** - Requires admin authentication
    
    Returns:
    - Total members count
    - Active event info
    - RSVP statistics
    - Payment statistics
    - Recent activity
    
    Args:
        current_admin: Authenticated admin
        db: Database session
        
    Returns:
        Dashboard statistics
    """
    # Get counts
    total_members = db.query(Member).filter(Member.is_active == True).count()
    total_events = db.query(Event).count()
    active_events = db.query(Event).filter(Event.is_active == True).count()
    
    # Get current event
    current_event = db.query(Event).filter(Event.is_active == True).first()
    
    # RSVP stats for current event
    rsvp_stats = {
        "total": 0,
        "accepted": 0,
        "declined": 0,
        "pending": 0
    }
    
    if current_event:
        rsvps = db.query(RSVP).filter(RSVP.event_id == current_event.id).all()
        rsvp_stats["total"] = len(rsvps)
        rsvp_stats["accepted"] = len([r for r in rsvps if r.status == "accepted"])
        rsvp_stats["declined"] = len([r for r in rsvps if r.status == "declined"])
        rsvp_stats["pending"] = total_members - len(rsvps)
    
    # Payment stats
    payment_stats = {
        "total": db.query(Payment).count(),
        "pending": db.query(Payment).filter(Payment.status == "pending").count(),
        "verified": db.query(Payment).filter(Payment.status == "verified").count(),
        "failed": db.query(Payment).filter(Payment.status == "failed").count()
    }
    
    # Recent activity (last 10 RSVPs)
    recent_rsvps = db.query(RSVP).order_by(RSVP.created_at.desc()).limit(10).all()
    recent_activity = []
    
    for rsvp in recent_rsvps:
        member = db.query(Member).filter(Member.id == rsvp.member_id).first()
        event = db.query(Event).filter(Event.id == rsvp.event_id).first()
        
        recent_activity.append({
            "type": "rsvp",
            "member_name": member.full_name if member else "Unknown",
            "event_name": event.title if event else "Unknown",
            "status": rsvp.status,
            "timestamp": rsvp.created_at.isoformat()
        })
    
    return {
        "overview": {
            "total_members": total_members,
            "total_events": total_events,
            "active_events": active_events
        },
        "current_event": {
            "id": str(current_event.id) if current_event else None,
            "title": current_event.title if current_event else None,
            "date": current_event.event_date.isoformat() if current_event else None
        },
        "rsvp_stats": rsvp_stats,
        "payment_stats": payment_stats,
        "recent_activity": recent_activity,
        "admin": {
            "name": current_admin.full_name,
            "email": current_admin.email
        }
    }


# ============================================================================
# MEMBER MANAGEMENT
# ============================================================================

@router.get("/members", response_model=List[MemberResponse])
async def list_members(
    current_admin: Member = Depends(require_admin),
    db: Session = Depends(get_db),
    pagination: PaginationParams = Depends(get_pagination),
    tier: Optional[str] = None,
    active_only: bool = True
) -> List[MemberResponse]:
    """
    List all members with optional filters
    
    **Protected Route** - Requires admin authentication
    
    Args:
        current_admin: Authenticated admin
        db: Database session
        pagination: Pagination parameters
        tier: Optional membership tier filter
        active_only: Only show active members
        
    Returns:
        List of members
    """
    # Build query
    query = db.query(Member)
    
    if active_only:
        query = query.filter(Member.is_active == True)
    
    if tier:
        query = query.filter(Member.membership_tier == tier)
    
    # Apply pagination
    members = query.offset(pagination.skip).limit(pagination.limit).all()
    
    return [MemberResponse.model_validate(member) for member in members]


@router.get("/members/{member_id}", response_model=Dict[str, Any])
async def get_member_details(
    member_id: UUID,
    current_admin: Member = Depends(require_admin),
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """
    Get detailed member information
    
    **Protected Route** - Requires admin authentication
    
    Returns member with their RSVPs, legacy passes, and payment history
    
    Args:
        member_id: Member UUID
        current_admin: Authenticated admin
        db: Database session
        
    Returns:
        Complete member details
        
    Raises:
        HTTPException 404: If member not found
    """
    # Get member
    member = db.query(Member).filter(Member.id == member_id).first()
    
    if not member:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Member not found."
        )
    
    # Get RSVPs
    rsvps = db.query(RSVP).filter(RSVP.member_id == member_id).all()
    rsvp_list = []
    
    for rsvp in rsvps:
        event = db.query(Event).filter(Event.id == rsvp.event_id).first()
        rsvp_list.append({
            "rsvp_id": str(rsvp.id),
            "event_name": event.title if event else "Unknown",
            "event_date": event.event_date.isoformat() if event else None,
            "status": rsvp.status,
            "responded_at": rsvp.responded_at.isoformat() if rsvp.responded_at else None
        })
    
    # Get Legacy Passes
    passes = db.query(LegacyPass).filter(LegacyPass.member_id == member_id).all()
    pass_list = []
    
    for legacy_pass in passes:
        payment = db.query(Payment).filter(
            Payment.legacy_pass_id == legacy_pass.id
        ).first()
        
        pass_list.append({
            "pass_number": legacy_pass.pass_number,
            "token": str(legacy_pass.unique_token),
            "access_level": legacy_pass.access_level,
            "gift_tier": legacy_pass.gift_tier,
            "payment_status": payment.status if payment else "no_payment",
            "created_at": legacy_pass.created_at.isoformat()
        })
    
    # Get Payments
    payments = db.query(Payment).filter(Payment.member_id == member_id).all()
    payment_list = []
    
    for payment in payments:
        payment_list.append({
            "payment_id": str(payment.id),
            "amount": float(payment.amount),
            "method": payment.payment_method,
            "status": payment.status,
            "created_at": payment.created_at.isoformat(),
            "verified_at": payment.verified_at.isoformat() if payment.verified_at else None
        })
    
    return {
        "member": MemberResponse.model_validate(member),
        "rsvps": rsvp_list,
        "legacy_passes": pass_list,
        "payments": payment_list,
        "total_rsvps": len(rsvp_list),
        "total_payments": len(payment_list)
    }


@router.post("/members", response_model=MemberResponse, status_code=status.HTTP_201_CREATED)
async def create_member(
    member_data: MemberCreate,
    current_admin: Member = Depends(require_admin),
    db: Session = Depends(get_db)
) -> MemberResponse:
    """
    Create a new member (add to VIP list)
    
    **Protected Route** - Requires admin authentication
    
    Args:
        member_data: New member information
        current_admin: Authenticated admin
        db: Database session
        
    Returns:
        Created member
        
    Raises:
        HTTPException 400: If email already exists
    """
    # Check if email already exists
    existing = db.query(Member).filter(Member.email == member_data.email).first()
    
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="A member with this email already exists."
        )
    
    # Generate membership number if not provided
    if not member_data.membership_number:
        member_count = db.query(Member).count()
        tier_prefix = {
            "founding_member": "FM",
            "vip": "VIP",
            "inner_circle": "IC",
            "admin": "ADMIN"
        }.get(member_data.membership_tier, "IC")
        
        member_data.membership_number = f"{tier_prefix}-{str(member_count + 1).zfill(3)}"
    
    # Create member
    member = Member(
        email=member_data.email,
        full_name=member_data.full_name,
        phone_number=member_data.phone_number,
        membership_tier=member_data.membership_tier,
        membership_number=member_data.membership_number,
        is_active=True,
        has_logged_in=False
    )
    
    db.add(member)
    db.commit()
    db.refresh(member)
    
    return MemberResponse.model_validate(member)


@router.put("/members/{member_id}", response_model=MemberResponse)
async def update_member(
    member_id: UUID,
    member_update: MemberUpdate,
    current_admin: Member = Depends(require_admin),
    db: Session = Depends(get_db)
) -> MemberResponse:
    """
    Update member information
    
    **Protected Route** - Requires admin authentication
    
    Args:
        member_id: Member UUID
        member_update: Updated member data
        current_admin: Authenticated admin
        db: Database session
        
    Returns:
        Updated member
        
    Raises:
        HTTPException 404: If member not found
    """
    # Get member
    member = db.query(Member).filter(Member.id == member_id).first()
    
    if not member:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Member not found."
        )
    
    # Update fields
    if member_update.full_name is not None:
        member.full_name = member_update.full_name
    
    if member_update.phone_number is not None:
        member.phone_number = member_update.phone_number
    
    if member_update.membership_tier is not None:
        member.membership_tier = member_update.membership_tier
    
    member.updated_at = datetime.utcnow()
    
    db.commit()
    db.refresh(member)
    
    return MemberResponse.model_validate(member)


@router.delete("/members/{member_id}")
async def deactivate_member(
    member_id: UUID,
    current_admin: Member = Depends(require_admin),
    db: Session = Depends(get_db)
) -> Dict[str, str]:
    """
    Deactivate a member (soft delete)
    
    **Protected Route** - Requires admin authentication
    
    Args:
        member_id: Member UUID
        current_admin: Authenticated admin
        db: Database session
        
    Returns:
        Success message
        
    Raises:
        HTTPException 404: If member not found
    """
    # Get member
    member = db.query(Member).filter(Member.id == member_id).first()
    
    if not member:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Member not found."
        )
    
    # Soft delete (deactivate)
    member.is_active = False
    member.updated_at = datetime.utcnow()
    
    db.commit()
    
    return {
        "message": f"Member {member.full_name} has been deactivated.",
        "status": "success"
    }


# ============================================================================
# EVENT MANAGEMENT
# ============================================================================

@router.post("/events", response_model=EventResponse, status_code=status.HTTP_201_CREATED)
async def create_event(
    event_data: EventCreate,
    current_admin: Member = Depends(require_admin),
    db: Session = Depends(get_db)
) -> EventResponse:
    """
    Create a new event
    
    **Protected Route** - Requires admin authentication
    
    Args:
        event_data: New event information
        current_admin: Authenticated admin
        db: Database session
        
    Returns:
        Created event
    """
    # Create event
    event = Event(
        title=event_data.title,
        subtitle=event_data.subtitle,
        description=event_data.description,
        event_date=event_data.event_date,
        event_time=event_data.event_time,
        venue_name=event_data.venue_name,
        venue_address=event_data.venue_address,
        dress_code=event_data.dress_code,
        theme=event_data.theme,
        schedule=event_data.schedule,
        amenities=event_data.amenities,
        special_instructions=event_data.special_instructions,
        is_active=True
    )
    
    db.add(event)
    db.commit()
    db.refresh(event)
    
    return EventResponse.model_validate(event)


@router.put("/events/{event_id}", response_model=EventResponse)
async def update_event(
    event_id: UUID,
    event_update: EventUpdate,
    current_admin: Member = Depends(require_admin),
    db: Session = Depends(get_db)
) -> EventResponse:
    """
    Update event information
    
    **Protected Route** - Requires admin authentication
    
    Args:
        event_id: Event UUID
        event_update: Updated event data
        current_admin: Authenticated admin
        db: Database session
        
    Returns:
        Updated event
        
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
    
    # Update fields (only if provided)
    update_data = event_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(event, field, value)
    
    event.updated_at = datetime.utcnow()
    
    db.commit()
    db.refresh(event)
    
    return EventResponse.model_validate(event)


@router.delete("/events/{event_id}")
async def deactivate_event(
    event_id: UUID,
    current_admin: Member = Depends(require_admin),
    db: Session = Depends(get_db)
) -> Dict[str, str]:
    """
    Deactivate an event
    
    **Protected Route** - Requires admin authentication
    
    Args:
        event_id: Event UUID
        current_admin: Authenticated admin
        db: Database session
        
    Returns:
        Success message
        
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
    
    # Deactivate
    event.is_active = False
    event.updated_at = datetime.utcnow()
    
    db.commit()
    
    return {
        "message": f"Event '{event.title}' has been deactivated.",
        "status": "success"
    }


# ============================================================================
# RSVP MANAGEMENT
# ============================================================================

@router.get("/rsvps", response_model=List[Dict[str, Any]])
async def list_all_rsvps(
    current_admin: Member = Depends(require_admin),
    db: Session = Depends(get_db),
    event_id: Optional[UUID] = None,
    status_filter: Optional[str] = None
) -> List[Dict[str, Any]]:
    """
    List all RSVPs with filters
    
    **Protected Route** - Requires admin authentication
    
    Args:
        current_admin: Authenticated admin
        db: Database session
        event_id: Optional event filter
        status_filter: Optional status filter (accepted, declined)
        
    Returns:
        List of RSVPs with member and event details
    """
    # Build query
    query = db.query(RSVP)
    
    if event_id:
        query = query.filter(RSVP.event_id == event_id)
    
    if status_filter:
        query = query.filter(RSVP.status == status_filter)
    
    rsvps = query.order_by(RSVP.created_at.desc()).all()
    
    result = []
    
    for rsvp in rsvps:
        member = db.query(Member).filter(Member.id == rsvp.member_id).first()
        event = db.query(Event).filter(Event.id == rsvp.event_id).first()
        
        result.append({
            "rsvp_id": str(rsvp.id),
            "member": {
                "name": member.full_name if member else "Unknown",
                "email": member.email if member else "Unknown",
                "tier": member.membership_tier if member else "Unknown"
            },
            "event": {
                "title": event.title if event else "Unknown",
                "date": event.event_date.isoformat() if event else None
            },
            "status": rsvp.status,
            "response_message": rsvp.response_message,
            "responded_at": rsvp.responded_at.isoformat() if rsvp.responded_at else None
        })
    
    return result


@router.get("/rsvps/summary")
async def get_rsvp_summary(
    current_admin: Member = Depends(require_admin),
    db: Session = Depends(get_db),
    event_id: Optional[UUID] = None
) -> Dict[str, Any]:
    """
    Get RSVP summary statistics
    
    **Protected Route** - Requires admin authentication
    
    Args:
        current_admin: Authenticated admin
        db: Database session
        event_id: Optional event filter
        
    Returns:
        RSVP statistics
    """
    # Build query
    query = db.query(RSVP)
    
    if event_id:
        query = query.filter(RSVP.event_id == event_id)
    
    rsvps = query.all()
    
    total = len(rsvps)
    accepted = len([r for r in rsvps if r.status == "accepted"])
    declined = len([r for r in rsvps if r.status == "declined"])
    
    return {
        "total_responses": total,
        "accepted": accepted,
        "declined": declined,
        "acceptance_rate": (accepted / total * 100) if total > 0 else 0,
        "decline_rate": (declined / total * 100) if total > 0 else 0
    }


# ============================================================================
# STATISTICS & REPORTS
# ============================================================================

@router.get("/statistics")
async def get_statistics(
    current_admin: Member = Depends(require_admin),
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """
    Get comprehensive platform statistics
    
    **Protected Route** - Requires admin authentication
    
    Returns:
        Complete platform statistics
    """
    # Member statistics
    total_members = db.query(Member).filter(Member.is_active == True).count()
    members_by_tier = {}
    
    for tier in ["founding_member", "vip", "inner_circle"]:
        count = db.query(Member).filter(
            Member.membership_tier == tier,
            Member.is_active == True
        ).count()
        members_by_tier[tier] = count
    
    # Event statistics
    total_events = db.query(Event).count()
    active_events = db.query(Event).filter(Event.is_active == True).count()
    
    # RSVP statistics
    total_rsvps = db.query(RSVP).count()
    accepted_rsvps = db.query(RSVP).filter(RSVP.status == "accepted").count()
    declined_rsvps = db.query(RSVP).filter(RSVP.status == "declined").count()
    
    # Payment statistics
    total_payments = db.query(Payment).count()
    verified_payments = db.query(Payment).filter(Payment.status == "verified").count()
    pending_payments = db.query(Payment).filter(Payment.status == "pending").count()
    
    # Revenue (verified payments only)
    verified_payment_records = db.query(Payment).filter(Payment.status == "verified").all()
    total_revenue = sum(float(p.amount) for p in verified_payment_records)
    
    # Legacy Pass statistics
    total_passes = db.query(LegacyPass).count()
    active_passes = db.query(LegacyPass).filter(LegacyPass.is_active == True).count()
    
    return {
        "members": {
            "total": total_members,
            "by_tier": members_by_tier
        },
        "events": {
            "total": total_events,
            "active": active_events
        },
        "rsvps": {
            "total": total_rsvps,
            "accepted": accepted_rsvps,
            "declined": declined_rsvps,
            "acceptance_rate": (accepted_rsvps / total_rsvps * 100) if total_rsvps > 0 else 0
        },
        "payments": {
            "total": total_payments,
            "verified": verified_payments,
            "pending": pending_payments,
            "total_revenue": total_revenue
        },
        "legacy_passes": {
            "total": total_passes,
            "active": active_passes
        }
    }