from app import app
from models import db, User, Task

with app.app_context():
    print("Clearing Database...")
    Task.query.delete()
    User.query.delete()

    print("Seeding Users...")
    user1 = User(username="Alice")
    user1.set_password("password123")

    user2 = User(username="Don")
    user2.set_password("password123")

    db.session.add_all([user1, user2])
    db.session.commit()

    print("Seeding tasks...")
    task1 = Task(title="Finish Flask API Lab", description="Implement pagination and authentication",
                 status="In Progress", priority="High", user_id=user1.id)
    task2 = Task(title="Review Database Migrations", description="Run flask db init and upgrade",
                 status="Pending", priority="Medium", user_id=user1.id)
    task3 = Task(title="Prepare Presentation", description="Slides for project review",
                 status="Pending", priority="Low", user_id=user2.id)

    db.session.add_all([task1, task2, task3])
    db.session.commit()

    print("Database seeded successfully!")
