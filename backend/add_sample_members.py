"""
Add Sample Members to Database
Run this script to populate the database with test members
"""

import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app.database import SessionLocal
from app.models.member import Member
from datetime import datetime
import uuid


def add_sample_members():
    """Add sample members for testing"""
    db = SessionLocal()
    
    try:
        # Check if members already exist
        existing_count = db.query(Member).count()
        if existing_count > 0:
            print(f"⚠️  Database already has {existing_count} member(s)")
            response = input("Add more members anyway? (yes/no): ")
            if response.lower() != 'yes':
                print("Cancelled.")
                return
        
        print("\n" + "="*60)
        print("Adding Sample Members to Database")
        print("="*60 + "\n")
        
        # Sample members
        sample_members = [
            {
                "email": "founding@example.com",
                "full_name": "Alexandra Foundation",
                "phone_number": "+1-555-0101",
                "membership_tier": "founding_member",
                "membership_number": "FM-001"
            },
            {
                "email": "vip@example.com",
                "full_name": "Victoria Premier",
                "phone_number": "+1-555-0102",
                "membership_tier": "vip",
                "membership_number": "VIP-001"
            },
            {
                "email": "inner@example.com",
                "full_name": "Isabella Circle",
                "phone_number": "+1-555-0103",
                "membership_tier": "inner_circle",
                "membership_number": "IC-001"
            },
            {
                "email": "test@example.com",
                "full_name": "Test Member",
                "phone_number": "+1-555-0104",
                "membership_tier": "inner_circle",
                "membership_number": "IC-002"
            },
            {
                "email": "admin@paigeinnercircle.com",
                "full_name": "Admin User",
                "phone_number": "+1-555-0100",
                "membership_tier": "admin",
                "membership_number": "ADMIN-001"
            }
        ]
        
        added_count = 0
        
        for member_data in sample_members:
            # Check if member already exists
            existing = db.query(Member).filter(
                Member.email == member_data["email"]
            ).first()
            
            if existing:
                print(f"⚠️  Skipped: {member_data['email']} (already exists)")
                continue
            
            # Create new member
            member = Member(
                id=uuid.uuid4(),
                email=member_data["email"],
                full_name=member_data["full_name"],
                phone_number=member_data["phone_number"],
                membership_tier=member_data["membership_tier"],
                membership_number=member_data["membership_number"],
                is_active=True,
                has_logged_in=False,
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow()
            )
            
            db.add(member)
            added_count += 1
            print(f"✓ Added: {member_data['full_name']} ({member_data['email']})")
        
        # Commit all changes
        db.commit()
        
        print("\n" + "="*60)
        print(f"✅ Successfully added {added_count} member(s)")
        print("="*60 + "\n")
        
        # Display all members
        print("Current Members in Database:")
        print("-" * 60)
        all_members = db.query(Member).all()
        for member in all_members:
            print(f"  • {member.full_name}")
            print(f"    Email: {member.email}")
            print(f"    Tier: {member.membership_tier}")
            print(f"    Number: {member.membership_number}")
            print()
        
        print("\n" + "="*60)
        print("You can now test authentication with these emails:")
        print("="*60)
        for member_data in sample_members:
            print(f"  • {member_data['email']}")
        print()
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        db.rollback()
    finally:
        db.close()


if __name__ == "__main__":
    add_sample_members()