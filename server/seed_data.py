#!/usr/bin/env python3
"""
Seed script to populate the database with sample data
"""
import asyncio
from sqlalchemy.orm import Session
from app.db.session import engine
from app.models.user import User
from app.models.course import Course
from app.models.lesson import Lesson
from app.core.security import get_password_hash

def seed_database():
    with Session(engine) as db:
        # Check if data already exists
        if db.query(User).first():
            print("Database already has data. Skipping seed.")
            return

        # Create sample users
        users = [
            User(
                full_name="John Instructor",
                email="instructor@example.com",
                hashed_password=get_password_hash("password123"),
                role="Instructor"
            ),
            User(
                full_name="Jane Student",
                email="student@example.com", 
                hashed_password=get_password_hash("password123"),
                role="Student"
            ),
            User(
                full_name="Mike Teacher",
                email="mike@example.com",
                hashed_password=get_password_hash("password123"),
                role="Instructor"
            )
        ]
        
        for user in users:
            db.add(user)
        db.commit()
        
        # Refresh to get IDs
        for user in users:
            db.refresh(user)

        # Create sample courses
        courses = [
            Course(
                title="Introduction to Python Programming",
                description="Learn Python from scratch with hands-on projects and real-world examples. Perfect for beginners who want to start their programming journey.",
                instructor_id=users[0].id
            ),
            Course(
                title="Web Development with React",
                description="Master modern web development using React, JavaScript, and CSS. Build responsive and interactive web applications.",
                instructor_id=users[0].id
            ),
            Course(
                title="Data Science Fundamentals", 
                description="Explore data analysis, visualization, and machine learning concepts using Python and popular libraries like pandas and scikit-learn.",
                instructor_id=users[2].id
            ),
            Course(
                title="Digital Marketing Essentials",
                description="Learn the fundamentals of digital marketing including SEO, social media marketing, and content strategy.",
                instructor_id=users[2].id
            ),
            Course(
                title="Mobile App Development",
                description="Create mobile applications for iOS and Android using React Native. Build cross-platform apps efficiently.",
                instructor_id=users[0].id
            )
        ]
        
        for course in courses:
            db.add(course)
        db.commit()
        
        # Refresh to get IDs
        for course in courses:
            db.refresh(course)

        # Create sample lessons
        lessons = [
            # Python course lessons
            Lesson(title="Getting Started with Python", content="Introduction to Python syntax and basic concepts", course_id=courses[0].id, order_index=1),
            Lesson(title="Variables and Data Types", content="Understanding Python variables, strings, numbers, and booleans", course_id=courses[0].id, order_index=2),
            Lesson(title="Control Structures", content="If statements, loops, and conditional logic in Python", course_id=courses[0].id, order_index=3),
            Lesson(title="Functions and Modules", content="Creating reusable code with functions and importing modules", course_id=courses[0].id, order_index=4),
            
            # React course lessons  
            Lesson(title="React Fundamentals", content="Components, JSX, and the virtual DOM", course_id=courses[1].id, order_index=1),
            Lesson(title="State and Props", content="Managing component state and passing data between components", course_id=courses[1].id, order_index=2),
            Lesson(title="Event Handling", content="Handling user interactions and form submissions", course_id=courses[1].id, order_index=3),
            
            # Data Science lessons
            Lesson(title="Introduction to Data Science", content="Overview of data science workflow and tools", course_id=courses[2].id, order_index=1),
            Lesson(title="Data Analysis with Pandas", content="Loading, cleaning, and analyzing data using pandas", course_id=courses[2].id, order_index=2),
            Lesson(title="Data Visualization", content="Creating charts and graphs with matplotlib and seaborn", course_id=courses[2].id, order_index=3),
            
            # Digital Marketing lessons
            Lesson(title="Marketing Strategy Basics", content="Understanding target audiences and marketing goals", course_id=courses[3].id, order_index=1),
            Lesson(title="SEO Fundamentals", content="Search engine optimization techniques and best practices", course_id=courses[3].id, order_index=2),
            
            # Mobile App lessons
            Lesson(title="React Native Setup", content="Setting up development environment for mobile apps", course_id=courses[4].id, order_index=1),
            Lesson(title="Building Your First App", content="Creating a simple mobile application with navigation", course_id=courses[4].id, order_index=2)
        ]
        
        for lesson in lessons:
            db.add(lesson)
        db.commit()

        print("✅ Database seeded successfully!")
        print(f"Created {len(users)} users, {len(courses)} courses, and {len(lessons)} lessons")
        print("\nSample login credentials:")
        print("Instructor: instructor@example.com / password123")
        print("Student: student@example.com / password123")

if __name__ == "__main__":
    seed_database()