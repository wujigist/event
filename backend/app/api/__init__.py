"""
API Package
FastAPI routes and dependencies
"""

from .dependencies import (
    get_db,
    get_current_member,
    require_admin,
    verify_member_active,
    get_pagination,
    PaginationParams
)

from .routes.auth import router as auth_router
from .routes.events import router as events_router
from .routes.rsvp import router as rsvp_router
from .routes.legacy_pass import router as legacy_pass_router
from .routes.payment import router as payment_router
from .routes.gifts import router as gifts_router
from .routes.memories import router as memories_router
from .routes.admin import router as admin_router

__all__ = [
    # Dependencies
    "get_db",
    "get_current_member",
    "require_admin",
    "verify_member_active",
    "get_pagination",
    "PaginationParams",

    # Routers
    "auth_router",
    "events_router",
    "rsvp_router",
    "legacy_pass_router",
    "payment_router",
    "gifts_router",
    "memories_router",
    "admin_router",
]
