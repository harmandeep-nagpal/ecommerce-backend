from app.db.database import SessionLocal
from app.services import user_service


def make_admin(email: str):
    db = SessionLocal()

    try:
        user = user_service.get_user_by_email(email, db)

        if user is None:
            print("User not found.")
            return

        if user.role == "admin":
            print("User is already an admin.")
            return

        user.role = "admin"
        db.commit()
        db.refresh(user)

        print(f"{user.email} is now an admin.")

    finally:
        db.close()


if __name__ == "__main__":
    email = input("Enter user email to promote: ")
    make_admin(email)