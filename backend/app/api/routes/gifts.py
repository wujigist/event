"""
Gifts Routes
Handles gift tier information and entitlements for members
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import Dict, Any, List

from ...database import get_db
from ...models.member import Member
from ...models.legacy_pass import LegacyPass
from ...api.dependencies import get_current_member
from ...services import (
    assign_gift_tier,
    get_gift_details,
    format_gift_list,
    format_gift_preview,
    get_gift_categories,
    compare_gift_tiers,
    get_highlighted_gifts,
    validate_gift_tier
)


router = APIRouter(prefix="/gifts", tags=["Gifts"])


@router.get("/tiers", response_model=Dict[str, Any])
async def get_all_gift_tiers() -> Dict[str, Any]:
    """
    Get information about all gift tiers
    
    **Public Endpoint** - No authentication required
    
    Returns comparison of Standard, Premium, and Elite tiers
    Shows what members can expect at each level
    
    Returns:
        Gift tier comparison
    """
    tier_comparison = compare_gift_tiers()
    
    return {
        "tiers": tier_comparison,
        "description": "Gift tiers are automatically assigned based on membership level",
        "tier_mapping": {
            "inner_circle": "Standard",
            "vip": "Premium",
            "founding_member": "Elite"
        }
    }


@router.get("/my-tier", response_model=Dict[str, Any])
async def get_my_gift_tier(
    current_member: Member = Depends(get_current_member),
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """
    Get current member's gift tier assignment
    
    **Protected Route** - Requires authentication
    
    Shows which tier the member is in and what they'll receive
    
    Args:
        current_member: Authenticated member
        db: Database session
        
    Returns:
        Member's gift tier information
    """
    # Assign gift tier based on membership
    gift_tier = assign_gift_tier(current_member.membership_tier)
    
    # Get gift details
    gift_details = get_gift_details(gift_tier)
    
    # Get formatted list
    gift_list = format_gift_list(gift_tier)
    
    return {
        "member_tier": current_member.membership_tier,
        "gift_tier": gift_tier,
        "total_items": len(gift_list),
        "gift_details": gift_details,
        "message": f"As a {current_member.membership_tier.replace('_', ' ').title()} member, you're entitled to our {gift_tier.title()} gift tier."
    }


@router.get("/preview", response_model=Dict[str, Any])
async def get_gift_preview(
    current_member: Member = Depends(get_current_member),
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """
    Get mystery-style preview of gifts
    
    **Protected Route** - Requires authentication
    
    Shows teaser of what's to come without revealing everything
    Perfect for building anticipation before RSVP
    
    Args:
        current_member: Authenticated member
        db: Database session
        
    Returns:
        Gift preview with teasers
    """
    # Assign gift tier
    gift_tier = assign_gift_tier(current_member.membership_tier)
    
    # Get mystery preview
    preview = format_gift_preview(gift_tier)
    
    return preview


@router.get("/{token}", response_model=Dict[str, Any])
async def get_gifts_by_token(
    token: str,
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """
    Get complete gift list using legacy pass token
    
    **No Authentication Required** - Uses token only
    
    Shows complete gift entitlements for a legacy pass holder
    Available after RSVP acceptance
    
    Args:
        token: Legacy pass token
        db: Database session
        
    Returns:
        Complete gift information
        
    Raises:
        HTTPException 404: If token not found
    """
    from ...services import validate_legacy_token
    
    # Validate token
    legacy_pass = validate_legacy_token(db, token)
    
    # Get gift details
    gift_list = format_gift_list(legacy_pass.gift_tier)
    gift_categories = get_gift_categories(legacy_pass.gift_tier)
    gift_details = get_gift_details(legacy_pass.gift_tier)
    
    return {
        "pass_number": legacy_pass.pass_number,
        "gift_tier": legacy_pass.gift_tier,
        "complete_list": gift_list,
        "by_category": gift_categories,
        "details": gift_details,
        "total_items": len(gift_list),
        "raffle_entries": gift_details.get("raffle_entries", 0),
        "message": "These exclusive gifts await you at the event."
    }


@router.get("/categories/{tier}", response_model=Dict[str, Any])
async def get_gifts_by_category(
    tier: str,
    current_member: Member = Depends(get_current_member)
) -> Dict[str, Any]:
    """
    Get gifts organized by category for a specific tier
    
    **Protected Route** - Requires authentication
    
    Args:
        tier: Gift tier (standard, premium, elite)
        current_member: Authenticated member
        
    Returns:
        Categorized gift list
        
    Raises:
        HTTPException 400: If invalid tier
    """
    # Validate tier
    if not validate_gift_tier(tier):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid gift tier. Must be: standard, premium, or elite"
        )
    
    # Get categorized gifts
    categories = get_gift_categories(tier)
    
    return {
        "tier": tier,
        "categories": categories,
        "total_categories": len(categories)
    }


@router.get("/highlights/{tier}", response_model=List[str])
async def get_highlighted_gifts_for_tier(
    tier: str,
    limit: int = 5,
    current_member: Member = Depends(get_current_member)
) -> List[str]:
    """
    Get top highlighted gifts for a tier
    
    **Protected Route** - Requires authentication
    
    Perfect for showcasing on landing pages or dashboards
    
    Args:
        tier: Gift tier (standard, premium, elite)
        limit: Number of items to return (default 5)
        current_member: Authenticated member
        
    Returns:
        List of highlighted gift items
        
    Raises:
        HTTPException 400: If invalid tier
    """
    # Validate tier
    if not validate_gift_tier(tier):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid gift tier. Must be: standard, premium, or elite"
        )
    
    # Get highlighted gifts
    highlights = get_highlighted_gifts(tier, limit)
    
    return highlights


@router.get("/member/{member_id}", response_model=Dict[str, Any])
async def get_member_gifts_admin(
    member_id: str,
    current_admin: Member = Depends(get_current_member),
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """
    Get gift information for a specific member (Admin view)
    
    **Protected Route** - Requires authentication
    
    Note: In production, you may want to add admin-only check here
    
    Args:
        member_id: Member UUID
        current_admin: Authenticated user
        db: Database session
        
    Returns:
        Member's gift information
        
    Raises:
        HTTPException 404: If member not found
    """
    from uuid import UUID
    
    # Get member
    member = db.query(Member).filter(Member.id == UUID(member_id)).first()
    
    if not member:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Member not found."
        )
    
    # Get gift tier
    gift_tier = assign_gift_tier(member.membership_tier)
    gift_list = format_gift_list(gift_tier)
    
    # Check if they have a legacy pass
    legacy_pass = db.query(LegacyPass).filter(
        LegacyPass.member_id == member.id
    ).first()
    
    return {
        "member": {
            "name": member.full_name,
            "email": member.email,
            "tier": member.membership_tier
        },
        "gift_tier": gift_tier,
        "gifts": gift_list,
        "total_items": len(gift_list),
        "has_legacy_pass": legacy_pass is not None,
        "pass_number": legacy_pass.pass_number if legacy_pass else None
    }