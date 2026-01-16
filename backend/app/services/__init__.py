"""
Services Package
All business logic and service layer functions
"""

from .auth_service import (
    validate_member_email,
    generate_access_token,
    verify_access_token,
    create_member_session,
    get_current_member,
    authenticate_member,
    logout_member
)

from .token_service import (
    generate_unique_token,
    validate_legacy_token,
    check_token_payment_status,
    get_legacy_pass_by_token,
    format_pass_number_preview,
    get_token_access_level,
    deactivate_legacy_pass,
    reactivate_legacy_pass
)

from .qr_code_service import (
    encode_pass_data,
    generate_qr_code,
    save_qr_code_image,
    generate_verification_qr,
    create_test_qr_code,
    decode_qr_data,
    validate_qr_data
)

from .legacy_pass_generator import (
    create_pass_front,
    create_pass_back,
    create_blurred_preview,
    save_pass_assets
)

from .pdf_generator import (
    create_legacy_pass_pdf,
    add_watermark,
    generate_pass_pdf,
    create_wallet_pass_data,
    format_for_wallet
)

from .email_service import (
    send_email,
    send_rsvp_confirmation,
    send_decline_thank_you,
    send_payment_instructions,
    send_payment_verified,
    notify_admin_payment_request,
    send_magic_link
)

from .gift_service import (
    assign_gift_tier,
    get_gift_details,
    format_gift_list,
    format_gift_preview,
    get_gift_categories,
    compare_gift_tiers,
    get_highlighted_gifts,
    validate_gift_tier
)

from .wallet_service import (
    generate_apple_wallet_pass,
    generate_google_pay_pass,
    is_wallet_available
)


__all__ = [
    # Auth service
    "validate_member_email",
    "generate_access_token",
    "verify_access_token",
    "create_member_session",
    "get_current_member",
    "authenticate_member",
    "logout_member",
    
    # Token service
    "generate_unique_token",
    "validate_legacy_token",
    "check_token_payment_status",
    "get_legacy_pass_by_token",
    "format_pass_number_preview",
    "get_token_access_level",
    "deactivate_legacy_pass",
    "reactivate_legacy_pass",
    
    # QR code service
    "encode_pass_data",
    "generate_qr_code",
    "save_qr_code_image",
    "generate_verification_qr",
    "create_test_qr_code",
    "decode_qr_data",
    "validate_qr_data",
    
    # Legacy pass generator
    "create_pass_front",
    "create_pass_back",
    "create_blurred_preview",
    "save_pass_assets",
    
    # PDF generator
    "create_legacy_pass_pdf",
    "add_watermark",
    "generate_pass_pdf",
    "create_wallet_pass_data",
    "format_for_wallet",
    
    # Email service
    "send_email",
    "send_rsvp_confirmation",
    "send_decline_thank_you",
    "send_payment_instructions",
    "send_payment_verified",
    "notify_admin_payment_request",
    "send_magic_link",
    
    # Gift service
    "assign_gift_tier",
    "get_gift_details",
    "format_gift_list",
    "format_gift_preview",
    "get_gift_categories",
    "compare_gift_tiers",
    "get_highlighted_gifts",
    "validate_gift_tier",
    
    # Wallet service
    "generate_apple_wallet_pass",
    "generate_google_pay_pass",
    "is_wallet_available",
]