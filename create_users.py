from app.db.database import SessionLocal
from app.models.user import User
from app.utils.security import hash_password

db = SessionLocal()

try:
    for i in range(4, 16):

        email = f"user{i}@example.com"

        existing_user = (
            db.query(User)
            .filter(User.email == email)
            .first()
        )

        if existing_user:
            continue

        user = User(
            username=f"User{i}",
            email=email,
            hashed_password=hash_password("Admin@123"),
            role="user",
            is_active=True,
        )

        db.add(user)

    db.commit()

    print("Users created successfully!")

except Exception as e:
    db.rollback()
    print(e)

finally:
    db.close()