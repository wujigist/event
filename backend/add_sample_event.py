"""
Add Sample Event to Database
Run this script to populate the database with a sample event
"""

import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app.database import SessionLocal
from app.models.event import Event
from datetime import datetime, timedelta
import uuid


def add_sample_event():
    """Add sample event for testing"""
    db = SessionLocal()
    
    try:
        # Check if events already exist
        existing_count = db.query(Event).count()
        if existing_count > 0:
            print(f"⚠️  Database already has {existing_count} event(s)")
            response = input("Add another event anyway? (yes/no): ")
            if response.lower() != 'yes':
                print("Cancelled.")
                return
        
        print("\n" + "="*60)
        print("Adding Sample Event to Database")
        print("="*60 + "\n")
        
        # Sample event (set for 30 days from now)
        event_date = datetime.utcnow() + timedelta(days=30)
        
        # Schedule data
        schedule_data = {
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
        
        # Amenities data
        amenities_data = {
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
        
        # Create event
        event = Event(
            id=uuid.uuid4(),
            title="Paige's Inner Circle Evening",
            subtitle="An Exclusive Celebration of Excellence",
            description="""Join us for an unforgettable evening of elegance, sophistication, and celebration. 

This exclusive event brings together the most distinguished members of Paige's Inner Circle for a night of luxury experiences, gourmet dining, and meaningful connections.

Immerse yourself in an atmosphere of refined beauty, where every detail has been meticulously curated to create memories that will last a lifetime. From the moment you arrive on the red carpet to the final farewell, you'll be treated to unparalleled hospitality and world-class entertainment.

This is more than an event—it's a celebration of excellence, achievement, and the extraordinary community we've built together.""",
            event_date=event_date,
            event_time="7:00 PM EST",
            venue_name="The Grand Ballroom at Azure Heights",
            venue_address="1250 Luxury Boulevard, Suite 2000, New York, NY 10022",
            dress_code="Black Tie",
            theme="Elegance & Excellence",
            schedule=schedule_data,
            amenities=amenities_data,
            special_instructions="""Please arrive between 6:30 PM and 6:45 PM for check-in. 

Valet parking is available at the main entrance. Your Legacy Pass will be required for entry—please have it ready either on your mobile device or printed.

For any special accommodations or dietary requirements, please contact our concierge team at least 48 hours before the event.

We look forward to celebrating with you!""",
            is_active=True,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )
        
        db.add(event)
        db.commit()
        
        print("✓ Added Event:")
        print(f"  Title: {event.title}")
        print(f"  Date: {event.event_date.strftime('%B %d, %Y')}")
        print(f"  Time: {event.event_time}")
        print(f"  Venue: {event.venue_name}")
        print(f"  ID: {event.id}")
        
        print("\n" + "="*60)
        print("✅ Successfully added sample event")
        print("="*60 + "\n")
        
        print("You can now test event endpoints:")
        print(f"  • GET /api/events/current")
        print(f"  • GET /api/events/{event.id}")
        print(f"  • GET /api/events/{event.id}/schedule")
        print(f"  • GET /api/events/{event.id}/amenities")
        print()
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        db.rollback()
    finally:
        db.close()


if __name__ == "__main__":
    add_sample_event()