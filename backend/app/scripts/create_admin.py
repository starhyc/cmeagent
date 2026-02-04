from app.core.database import SessionLocal
from app.models.database import User, UserRole
from app.core.security import hash_password
import getpass

def create_admin():
    db = SessionLocal()
    try:
        username = input("Admin username: ")
        password = getpass.getpass("Admin password: ")

        existing = db.query(User).filter(User.username == username).first()
        if existing:
            print(f"User {username} already exists!")
            return

        admin = User(
            username=username,
            password_hash=hash_password(password),
            role=UserRole.admin
        )
        db.add(admin)
        db.commit()
        print(f"Admin user {username} created successfully!")
    finally:
        db.close()

if __name__ == "__main__":
    create_admin()
