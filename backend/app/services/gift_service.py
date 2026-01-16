"""
Gift Service
Manages gift tiers, assignments, and mystery previews
"""

from typing import List, Dict, Any
from enum import Enum


class GiftTier(str, Enum):
    """Gift tier levels"""
    STANDARD = "standard"
    PREMIUM = "premium"
    ELITE = "elite"


class MembershipTier(str, Enum):
    """Membership tier levels"""
    INNER_CIRCLE = "inner_circle"
    FOUNDING_MEMBER = "founding_member"
    VIP = "vip"


# Gift tier mappings
GIFT_TIER_MAPPING = {
    MembershipTier.FOUNDING_MEMBER: GiftTier.ELITE,
    MembershipTier.VIP: GiftTier.PREMIUM,
    MembershipTier.INNER_CIRCLE: GiftTier.STANDARD,
}


# Detailed gift lists by tier
GIFTS_BY_TIER = {
    GiftTier.STANDARD: {
        "welcome_gift": [
            "Personalized welcome card with Paige's signature",
            "Luxury gift bag with branded items",
            "Commemorative photo frame"
        ],
        "event_gifts": [
            "Premium party favors",
            "Exclusive merchandise",
            "Signature cocktail recipe card",
            "Event photo package (digital)"
        ],
        "farewell_gift": [
            "Thank you note from Paige",
            "Digital photo album access",
            "Certificate of attendance"
        ],
        "raffle_entries": 2
    },
    GiftTier.PREMIUM: {
        "welcome_gift": [
            "Luxury welcome package with Paige's signature",
            "Designer gift bag with premium items",
            "Custom crystal photo frame",
            "Artisan chocolates"
        ],
        "event_gifts": [
            "Premium party favors",
            "Exclusive limited-edition merchandise",
            "Signature cocktail recipe card (printed)",
            "Professional event photo package (print + digital)",
            "Personalized champagne flute",
            "Access to VIP lounge"
        ],
        "farewell_gift": [
            "Handwritten thank you note from Paige",
            "Premium digital photo album",
            "Certificate of attendance (framed)",
            "Exclusive discount code for future events"
        ],
        "raffle_entries": 5
    },
    GiftTier.ELITE: {
        "welcome_gift": [
            "Ultra-luxury welcome package with personal video message from Paige",
            "Designer gift bag with exclusive premium items",
            "Custom engraved crystal photo frame",
            "Artisan chocolates and gourmet treats",
            "Luxury scented candle"
        ],
        "event_gifts": [
            "Premium party favors (double portion)",
            "Exclusive limited-edition merchandise (signed)",
            "Signature cocktail recipe card (leather-bound)",
            "Professional event photo package (premium print + digital)",
            "Personalized engraved champagne flute set",
            "VIP lounge access with concierge service",
            "Backstage/private moment with Paige",
            "Commemorative event medallion"
        ],
        "farewell_gift": [
            "Handwritten thank you letter from Paige (framed)",
            "Premium digital photo album + professional photo book",
            "Certificate of founding membership (museum quality frame)",
            "Lifetime VIP status for all future events",
            "Exclusive merchandise not available to others",
            "Personal Paige hotline for future event RSVP"
        ],
        "raffle_entries": 10,
        "special_perks": [
            "Priority seating at all future events",
            "Annual exclusive gift delivery",
            "Access to private Inner Circle community"
        ]
    }
}


def assign_gift_tier(membership_tier: str) -> str:
    """
    Assign gift tier based on membership level
    
    Args:
        membership_tier: Member's tier level
        
    Returns:
        Gift tier string
    """
    try:
        membership = MembershipTier(membership_tier.lower())
        gift_tier = GIFT_TIER_MAPPING.get(membership, GiftTier.STANDARD)
        return gift_tier.value
    except ValueError:
        return GiftTier.STANDARD.value


def get_gift_details(gift_tier: str) -> Dict[str, Any]:
    """
    Get complete gift list for a tier
    
    Args:
        gift_tier: Gift tier level
        
    Returns:
        Dictionary with all gifts for the tier
    """
    try:
        tier = GiftTier(gift_tier.lower())
        return GIFTS_BY_TIER.get(tier, GIFTS_BY_TIER[GiftTier.STANDARD])
    except ValueError:
        return GIFTS_BY_TIER[GiftTier.STANDARD]


def format_gift_list(gift_tier: str) -> List[str]:
    """
    Format complete gift list as flat array
    
    Args:
        gift_tier: Gift tier level
        
    Returns:
        List of all gift items
    """
    gifts = get_gift_details(gift_tier)
    gift_list = []
    
    # Welcome gifts
    gift_list.extend(gifts.get("welcome_gift", []))
    
    # Event gifts
    gift_list.extend(gifts.get("event_gifts", []))
    
    # Farewell gifts
    gift_list.extend(gifts.get("farewell_gift", []))
    
    # Add raffle entry info
    raffle_entries = gifts.get("raffle_entries", 0)
    if raffle_entries > 0:
        gift_list.append(f"{raffle_entries} exclusive raffle entries")
    
    # Add special perks if elite
    special_perks = gifts.get("special_perks", [])
    if special_perks:
        gift_list.extend(special_perks)
    
    return gift_list


def format_gift_preview(gift_tier: str) -> Dict[str, Any]:
    """
    Create mystery-style preview of gifts
    
    Args:
        gift_tier: Gift tier level
        
    Returns:
        Dictionary with teaser information
    """
    gifts = get_gift_details(gift_tier)
    
    # Count total items
    total_items = (
        len(gifts.get("welcome_gift", [])) +
        len(gifts.get("event_gifts", [])) +
        len(gifts.get("farewell_gift", []))
    )
    
    # Create mystery preview
    preview = {
        "tier": gift_tier.upper(),
        "total_items": total_items,
        "categories": {
            "welcome": len(gifts.get("welcome_gift", [])),
            "event": len(gifts.get("event_gifts", [])),
            "farewell": len(gifts.get("farewell_gift", []))
        },
        "raffle_entries": gifts.get("raffle_entries", 0),
        "teaser_items": [
            "Personalized welcome package from Paige",
            "Exclusive event merchandise",
            "Premium party favors",
            "Commemorative keepsakes",
            "...and more surprises!"
        ],
        "mystery_message": "✨ The complete gift experience will be revealed after payment verification"
    }
    
    # Add tier-specific teasers
    if gift_tier == GiftTier.ELITE.value:
        preview["special_highlight"] = "🌟 Includes exclusive founding member perks and lifetime VIP status"
    elif gift_tier == GiftTier.PREMIUM.value:
        preview["special_highlight"] = "💎 Includes VIP lounge access and personalized items"
    
    return preview


def get_gift_categories(gift_tier: str) -> Dict[str, List[str]]:
    """
    Get gifts organized by category
    
    Args:
        gift_tier: Gift tier level
        
    Returns:
        Dictionary with gifts organized by category
    """
    gifts = get_gift_details(gift_tier)
    
    return {
        "Welcome Package": gifts.get("welcome_gift", []),
        "Event Gifts & Amenities": gifts.get("event_gifts", []),
        "Farewell & Commemorative": gifts.get("farewell_gift", []),
        "Special Perks": gifts.get("special_perks", []) if "special_perks" in gifts else []
    }


def compare_gift_tiers() -> Dict[str, Any]:
    """
    Create comparison of all gift tiers
    
    Returns:
        Dictionary comparing all tiers
    """
    comparison = {}
    
    for tier in [GiftTier.STANDARD, GiftTier.PREMIUM, GiftTier.ELITE]:
        gifts = get_gift_details(tier.value)
        comparison[tier.value] = {
            "name": tier.value.title(),
            "welcome_items": len(gifts.get("welcome_gift", [])),
            "event_items": len(gifts.get("event_gifts", [])),
            "farewell_items": len(gifts.get("farewell_gift", [])),
            "total_items": (
                len(gifts.get("welcome_gift", [])) +
                len(gifts.get("event_gifts", [])) +
                len(gifts.get("farewell_gift", []))
            ),
            "raffle_entries": gifts.get("raffle_entries", 0),
            "has_special_perks": "special_perks" in gifts and len(gifts["special_perks"]) > 0
        }
    
    return comparison


def get_highlighted_gifts(gift_tier: str, limit: int = 5) -> List[str]:
    """
    Get top highlighted gifts for showcase
    
    Args:
        gift_tier: Gift tier level
        limit: Maximum number of items to return
        
    Returns:
        List of highlighted gift items
    """
    all_gifts = format_gift_list(gift_tier)
    
    # Return top N items
    return all_gifts[:limit]


def validate_gift_tier(tier: str) -> bool:
    """
    Validate if gift tier is valid
    
    Args:
        tier: Gift tier string
        
    Returns:
        True if valid, False otherwise
    """
    try:
        GiftTier(tier.lower())
        return True
    except ValueError:
        return False