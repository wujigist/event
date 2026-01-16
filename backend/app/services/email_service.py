"""
Email Service
Sends beautifully crafted emails for various member interactions
"""

import aiosmtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import Optional
from jinja2 import Template
from pathlib import Path

from ..config import settings


# Email templates (can be moved to separate HTML files later)
MAGIC_LINK_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <style>
        body {
            font-family: 'Georgia', serif;
            background-color: #0A0A0A;
            color: #F5F5F5;
            padding: 40px;
        }
        .container {
            max-width: 600px;
            margin: 0 auto;
            background-color: #1A1A1A;
            border: 2px solid #D4AF37;
            padding: 40px;
        }
        .header {
            text-align: center;
            color: #D4AF37;
            font-size: 28px;
            margin-bottom: 30px;
        }
        .content {
            line-height: 1.8;
            font-size: 16px;
        }
        .button {
            display: inline-block;
            background-color: #D4AF37;
            color: #0A0A0A;
            padding: 15px 40px;
            text-decoration: none;
            font-weight: bold;
            border-radius: 5px;
            margin: 20px 0;
        }
        .signature {
            margin-top: 40px;
            font-style: italic;
            color: #D4AF37;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">Paige's Inner Circle</div>
        <div class="content">
            <p>Dear {{ member_name }},</p>
            <p>{{ message }}</p>
            <div style="text-align: center;">
                <a href="{{ link }}" class="button">{{ button_text }}</a>
            </div>
            <p>We look forward to celebrating with you.</p>
            <div class="signature">
                <p>With warm regards,<br>Paige</p>
            </div>
        </div>
    </div>
</body>
</html>
"""


RSVP_CONFIRMATION_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <style>
        body {
            font-family: 'Georgia', serif;
            background-color: #0A0A0A;
            color: #F5F5F5;
            padding: 40px;
        }
        .container {
            max-width: 600px;
            margin: 0 auto;
            background-color: #1A1A1A;
            border: 2px solid #D4AF37;
            padding: 40px;
        }
        .header {
            text-align: center;
            color: #D4AF37;
            font-size: 28px;
            margin-bottom: 30px;
        }
        .content {
            line-height: 1.8;
            font-size: 16px;
        }
        .token-box {
            background-color: #2A2A2A;
            border: 1px solid #D4AF37;
            padding: 20px;
            margin: 20px 0;
            text-align: center;
            font-family: monospace;
            font-size: 18px;
            color: #D4AF37;
        }
        .signature {
            margin-top: 40px;
            font-style: italic;
            color: #D4AF37;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">Your Presence is Confirmed ✨</div>
        <div class="content">
            <p>Dear {{ member_name }},</p>
            <p>I'm absolutely delighted you'll be joining us! Your confirmation means the world to me.</p>
            <p>Your exclusive Legacy Pass has been created. Here is your unique access token:</p>
            <div class="token-box">{{ token }}</div>
            <p>This token grants you access to your personalized Legacy Pass, which includes all the details and luxury amenities planned for our evening together.</p>
            <p><strong>Next Step:</strong> Complete your $1,000 investment to unlock full access to your Legacy Pass and all its exclusive benefits.</p>
            <div class="signature">
                <p>I can't wait to share this special moment with you.<br><br>With love and excitement,<br>Paige</p>
            </div>
        </div>
    </div>
</body>
</html>
"""


DECLINE_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <style>
        body {
            font-family: 'Georgia', serif;
            background-color: #0A0A0A;
            color: #F5F5F5;
            padding: 40px;
        }
        .container {
            max-width: 600px;
            margin: 0 auto;
            background-color: #1A1A1A;
            border: 2px solid #D4AF37;
            padding: 40px;
        }
        .header {
            text-align: center;
            color: #D4AF37;
            font-size: 28px;
            margin-bottom: 30px;
        }
        .content {
            line-height: 1.8;
            font-size: 16px;
        }
        .signature {
            margin-top: 40px;
            font-style: italic;
            color: #D4AF37;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">You'll Be Missed 💛</div>
        <div class="content">
            <p>Dear {{ member_name }},</p>
            <p>While I'm saddened you won't be able to join us in person, I completely understand. Your support and presence in my journey means everything, regardless of physical distance.</p>
            <p>Even though you won't be there, you'll remain in my thoughts throughout the evening. This is just one chapter, and I look forward to many more moments we'll share together.</p>
            <p>Thank you for being part of my Inner Circle. You'll have priority access to all future exclusive events.</p>
            <div class="signature">
                <p>Until we meet again,<br><br>With gratitude and love,<br>Paige</p>
            </div>
        </div>
    </div>
</body>
</html>
"""


PAYMENT_INSTRUCTIONS_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <style>
        body {
            font-family: 'Georgia', serif;
            background-color: #0A0A0A;
            color: #F5F5F5;
            padding: 40px;
        }
        .container {
            max-width: 600px;
            margin: 0 auto;
            background-color: #1A1A1A;
            border: 2px solid #D4AF37;
            padding: 40px;
        }
        .header {
            text-align: center;
            color: #D4AF37;
            font-size: 28px;
            margin-bottom: 30px;
        }
        .content {
            line-height: 1.8;
            font-size: 16px;
        }
        .info-box {
            background-color: #2A2A2A;
            border-left: 4px solid #D4AF37;
            padding: 20px;
            margin: 20px 0;
        }
        .signature {
            margin-top: 40px;
            font-style: italic;
            color: #D4AF37;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">Payment Request Received</div>
        <div class="content">
            <p>Dear {{ member_name }},</p>
            <p>Thank you for your payment request. Our team has received your information and will contact you within 24 hours with payment instructions for your chosen method:</p>
            <div class="info-box">
                <strong>Selected Payment Method:</strong> {{ payment_method }}<br>
                <strong>Contact Email:</strong> {{ contact_email }}<br>
                <strong>Amount:</strong> $1,000.00 USD
            </div>
            <p>Once your payment is verified, you'll receive immediate access to your complete Legacy Pass with all exclusive benefits unlocked.</p>
            <p>If you have any questions in the meantime, don't hesitate to reach out.</p>
            <div class="signature">
                <p>Thank you for your investment in this experience,<br><br>The Paige's Inner Circle Team</p>
            </div>
        </div>
    </div>
</body>
</html>
"""


PAYMENT_VERIFIED_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <style>
        body {
            font-family: 'Georgia', serif;
            background-color: #0A0A0A;
            color: #F5F5F5;
            padding: 40px;
        }
        .container {
            max-width: 600px;
            margin: 0 auto;
            background-color: #1A1A1A;
            border: 2px solid #D4AF37;
            padding: 40px;
        }
        .header {
            text-align: center;
            color: #D4AF37;
            font-size: 28px;
            margin-bottom: 30px;
        }
        .content {
            line-height: 1.8;
            font-size: 16px;
        }
        .button {
            display: inline-block;
            background-color: #D4AF37;
            color: #0A0A0A;
            padding: 15px 40px;
            text-decoration: none;
            font-weight: bold;
            border-radius: 5px;
            margin: 20px 0;
        }
        .signature {
            margin-top: 40px;
            font-style: italic;
            color: #D4AF37;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">Payment Verified - Welcome! 🎉</div>
        <div class="content">
            <p>Dear {{ member_name }},</p>
            <p>Wonderful news! Your payment has been verified and your full Legacy Pass is now unlocked.</p>
            <p>You now have complete access to:</p>
            <ul>
                <li>Your personalized Legacy Pass with QR code</li>
                <li>Detailed event schedule and venue information</li>
                <li>Complete list of exclusive gifts and amenities</li>
                <li>VIP seating assignment</li>
                <li>Downloadable pass for your mobile device</li>
            </ul>
            <div style="text-align: center;">
                <a href="{{ pass_link }}" class="button">View Your Legacy Pass</a>
            </div>
            <p>I'm so excited to welcome you to this exclusive experience!</p>
            <div class="signature">
                <p>See you soon,<br><br>Paige</p>
            </div>
        </div>
    </div>
</body>
</html>
"""


async def send_email(
    to_email: str,
    subject: str,
    html_content: str,
    from_email: str = None
) -> bool:
    """
    Send HTML email using SMTP
    
    Args:
        to_email: Recipient email address
        subject: Email subject
        html_content: HTML email body
        from_email: Sender email (defaults to settings)
        
    Returns:
        True if sent successfully, False otherwise
    """
    if not from_email:
        from_email = settings.EMAIL_FROM
    
    try:
        # Create message
        message = MIMEMultipart("alternative")
        message["Subject"] = subject
        message["From"] = f"Paige's Inner Circle <{from_email}>"
        message["To"] = to_email
        
        # Add HTML content
        html_part = MIMEText(html_content, "html")
        message.attach(html_part)
        
        # Send email
        await aiosmtplib.send(
            message,
            hostname=settings.EMAIL_HOST,
            port=settings.EMAIL_PORT,
            username=settings.EMAIL_USER,
            password=settings.EMAIL_PASSWORD,
            start_tls=True
        )
        
        return True
        
    except Exception as e:
        print(f"Email sending failed: {e}")
        return False


async def send_rsvp_confirmation(
    to_email: str,
    member_name: str,
    token: str
) -> bool:
    """Send RSVP confirmation email with legacy pass token"""
    template = Template(RSVP_CONFIRMATION_TEMPLATE)
    html_content = template.render(
        member_name=member_name,
        token=token
    )
    
    return await send_email(
        to_email=to_email,
        subject="✨ Your Presence is Confirmed - Legacy Pass Created",
        html_content=html_content
    )


async def send_decline_thank_you(
    to_email: str,
    member_name: str
) -> bool:
    """Send graceful decline acknowledgment"""
    template = Template(DECLINE_TEMPLATE)
    html_content = template.render(member_name=member_name)
    
    return await send_email(
        to_email=to_email,
        subject="💛 You'll Be Missed - Thank You",
        html_content=html_content
    )


async def send_payment_instructions(
    to_email: str,
    member_name: str,
    payment_method: str,
    contact_email: str
) -> bool:
    """Send payment instructions after contact form submission"""
    template = Template(PAYMENT_INSTRUCTIONS_TEMPLATE)
    html_content = template.render(
        member_name=member_name,
        payment_method=payment_method,
        contact_email=contact_email
    )
    
    return await send_email(
        to_email=to_email,
        subject="Payment Request Received - Next Steps",
        html_content=html_content
    )


async def send_payment_verified(
    to_email: str,
    member_name: str,
    pass_token: str
) -> bool:
    """Send notification when payment is verified"""
    pass_link = f"{settings.FRONTEND_URL}/legacy-pass/{pass_token}"
    
    template = Template(PAYMENT_VERIFIED_TEMPLATE)
    html_content = template.render(
        member_name=member_name,
        pass_link=pass_link
    )
    
    return await send_email(
        to_email=to_email,
        subject="🎉 Payment Verified - Full Access Granted!",
        html_content=html_content
    )


async def notify_admin_payment_request(
    admin_email: str,
    member_name: str,
    member_email: str,
    payment_method: str,
    contact_email: str,
    pass_number: str
) -> bool:
    """Notify admin of new payment request"""
    html_content = f"""
    <html>
    <body style="font-family: Arial, sans-serif;">
        <h2>New Payment Request</h2>
        <p><strong>Member:</strong> {member_name} ({member_email})</p>
        <p><strong>Pass Number:</strong> {pass_number}</p>
        <p><strong>Payment Method:</strong> {payment_method}</p>
        <p><strong>Contact Email:</strong> {contact_email}</p>
        <p><strong>Amount:</strong> $1,000.00 USD</p>
        <p>Please process this payment request and verify in the admin panel.</p>
    </body>
    </html>
    """
    
    return await send_email(
        to_email=admin_email,
        subject=f"💳 New Payment Request - {member_name}",
        html_content=html_content
    )


async def send_magic_link(
    to_email: str,
    member_name: str,
    access_link: str
) -> bool:
    """Send magic link for email-based access (optional feature)"""
    template = Template(MAGIC_LINK_TEMPLATE)
    html_content = template.render(
        member_name=member_name,
        message="Click the button below to access your exclusive invitation.",
        link=access_link,
        button_text="Access Your Invitation"
    )
    
    return await send_email(
        to_email=to_email,
        subject="🔑 Access Your Exclusive Invitation",
        html_content=html_content
    )