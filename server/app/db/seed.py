from app.db.session import SessionLocal
from app.models.user import User
from app.models.course import Course
from app.models.lesson import Lesson
from app.models.enrollment import Enrollment
from app.core.security import hash_password

def seed_data():
    db = SessionLocal()
    try:
        if db.query(User).first():
            return
        
        # Create instructor
        instructor = User(
            full_name="Dr. Jane Smith",
            email="instructor@learnflow.com",
            password_hash=hash_password("instructor123"),
            role="instructor"
        )
        db.add(instructor)
        db.commit()
        db.refresh(instructor)
        
        # Create student
        student = User(
            full_name="Alice Johnson",
            email="student@learnflow.com",
            password_hash=hash_password("student123"),
            role="student"
        )
        db.add(student)
        db.commit()
        db.refresh(student)
        
        # Create courses
        courses_data = [
            {
                "title": "Introduction to Python Programming",
                "description": "Learn the basics of Python programming from scratch.",
                "category": "Programming",
                "price": 49.99,
                "image_url": "https://example.com/python-course.jpg",
                "learning_outcomes_json": '["Write basic Python scripts", "Understand data types", "Use control structures"]',
                "lessons": [
                    {"title": "Getting Started with Python", "content": "Installation and setup", "video_link": "https://example.com/video1", "order": 1, "section": "Week 1"},
                    {"title": "Variables and Data Types", "content": "Strings, numbers, booleans", "video_link": "https://example.com/video2", "order": 2, "section": "Week 1"},
                    {"title": "Control Structures", "content": "If statements and loops", "video_link": "https://example.com/video3", "order": 3, "section": "Week 2"},
                    {"title": "Functions", "content": "Defining and calling functions", "video_link": "https://example.com/video4", "order": 4, "section": "Week 2"},
                    {"title": "Lists and Dictionaries", "content": "Working with collections", "video_link": "https://example.com/video5", "order": 5, "section": "Week 3"},
                    {"title": "File I/O", "content": "Reading and writing files", "video_link": "https://example.com/video6", "order": 6, "section": "Week 3"},
                ]
            },
            {
                "title": "Web Development with React",
                "description": "Build modern web applications with React.",
                "category": "Web Development",
                "price": 79.99,
                "image_url": "https://example.com/react-course.jpg",
                "learning_outcomes_json": '["Create React components", "Manage state", "Handle events"]',
                "lessons": [
                    {"title": "Introduction to React", "content": "What is React?", "video_link": "https://example.com/video7", "order": 1, "section": "Module 1"},
                    {"title": "JSX and Components", "content": "Writing JSX", "video_link": "https://example.com/video8", "order": 2, "section": "Module 1"},
                    {"title": "State and Props", "content": "Managing data", "video_link": "https://example.com/video9", "order": 3, "section": "Module 2"},
                    {"title": "Event Handling", "content": "User interactions", "video_link": "https://example.com/video10", "order": 4, "section": "Module 2"},
                    {"title": "Hooks", "content": "useState and useEffect", "video_link": "https://example.com/video11", "order": 5, "section": "Module 3"},
                    {"title": "Routing", "content": "React Router", "video_link": "https://example.com/video12", "order": 6, "section": "Module 3"},
                    {"title": "API Integration", "content": "Fetching data", "video_link": "https://example.com/video13", "order": 7, "section": "Module 4"},
                    {"title": "Deployment", "content": "Deploying React apps", "video_link": "https://example.com/video14", "order": 8, "section": "Module 4"},
                ]
            },
            {
                "title": "Data Science Fundamentals",
                "description": "Learn data analysis and visualization.",
                "category": "Data Science",
                "price": 69.99,
                "image_url": "https://example.com/data-course.jpg",
                "learning_outcomes_json": '["Analyze datasets", "Create visualizations", "Build models"]',
                "lessons": [
                    {"title": "Introduction to Data Science", "content": "What is data science?", "video_link": "https://example.com/video15", "order": 1, "section": "Unit 1"},
                    {"title": "Python for Data Analysis", "content": "Pandas basics", "video_link": "https://example.com/video16", "order": 2, "section": "Unit 1"},
                    {"title": "Data Visualization", "content": "Matplotlib and Seaborn", "video_link": "https://example.com/video17", "order": 3, "section": "Unit 2"},
                    {"title": "Statistical Analysis", "content": "Descriptive statistics", "video_link": "https://example.com/video18", "order": 4, "section": "Unit 2"},
                    {"title": "Machine Learning Basics", "content": "Supervised learning", "video_link": "https://example.com/video19", "order": 5, "section": "Unit 3"},
                ]
            }
        ]
        
        for course_data in courses_data:
            course = Course(
                title=course_data["title"],
                description=course_data["description"],
                category=course_data["category"],
                price=course_data["price"],
                image_url=course_data["image_url"],
                learning_outcomes_json=course_data["learning_outcomes_json"],
                instructor_id=instructor.id
            )
            db.add(course)
            db.commit()
            db.refresh(course)
            
            for lesson_data in course_data["lessons"]:
                lesson = Lesson(
                    lesson_title=lesson_data["title"],
                    content_body=lesson_data["content"],
                    video_link=lesson_data["video_link"],
                    order_sequence=lesson_data["order"],
                    section_title=lesson_data["section"],
                    course_id=course.id
                )
                db.add(lesson)
            db.commit()
        
        # Enroll student in first course
        enrollment = Enrollment(
            user_id=student.id,
            course_id=1,
            current_status="Active"
        )
        db.add(enrollment)
        db.commit()
        
    finally:
        db.close()
