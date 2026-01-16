from app.database import engine, SessionLocal
from app.config import settings
from sqlalchemy import text

print("="*50)
print("Testing Database Connection")
print("="*50)

# Test connection
try:
    with engine.connect() as connection:
        result = connection.execute(text("SELECT version();"))
        version = result.fetchone()
        print(f"✅ Database connected successfully!")
        print(f"PostgreSQL version: {version[0]}")
        print(f"Database URL: {settings.DATABASE_URL.split('@')[1]}")  # Hide password
        
    # Test session creation
    db = SessionLocal()
    print("✅ Database session created successfully!")
    db.close()
    print("✅ Database session closed successfully!")
    
    print("\n" + "="*50)
    print("All database tests passed! ✅")
    print("="*50)
    
except Exception as e:
    print(f"❌ Database connection failed: {e}")