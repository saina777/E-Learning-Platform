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
        
        # Create courses with lessons
        courses_data = [
            {
                "title": "Introduction to Python",
                "description": "Learn Python programming from scratch.",
                "category": "Programming",
                "price": 49.99,
                "lessons": [
                    {"title": "Python Basics", "content": "Learn what Python is and why it's powerful. Python is a versatile language used for web development, data science, and more.", "order": 1, "section": "Week 1", "duration": 25},
                    {"title": "Variables and Types", "content": "Understand variables, data types (int, str, float, bool), and type conversions in Python.", "order": 2, "section": "Week 1", "duration": 30},
                    {"title": "Control Flow", "content": "Master if statements, loops (for, while), and conditional logic.", "order": 3, "section": "Week 2", "duration": 35},
                    {"title": "Functions", "content": "Learn to write reusable functions with parameters and return values.", "order": 4, "section": "Week 2", "duration": 40},
                    {"title": "Lists and Dictionaries", "content": "Work with collections: lists, tuples, sets, and dictionaries.", "order": 5, "section": "Week 3", "duration": 45},
                ]
            },
            {
                "title": "Web Development with React",
                "description": "Build modern web applications.",
                "category": "Web Development",
                "price": 79.99,
                "lessons": [
                    {"title": "React Basics", "content": "Introduction to React and component-based architecture. Learn JSX syntax.", "order": 1, "section": "Module 1", "duration": 35},
                    {"title": "Components", "content": "Create functional and class components, understand props and composition.", "order": 2, "section": "Module 1", "duration": 40},
                    {"title": "State Management", "content": "Use useState hook to manage component state and handle user interactions.", "order": 3, "section": "Module 2", "duration": 45},
                    {"title": "Hooks Deep Dive", "content": "Learn useEffect, useContext, and custom hooks for advanced state management.", "order": 4, "section": "Module 2", "duration": 50},
                    {"title": "Routing", "content": "Implement client-side routing with React Router for multi-page applications.", "order": 5, "section": "Module 3", "duration": 40},
                ]
            },
            {
                "title": "Data Science Fundamentals",
                "description": "Learn data analysis and visualization.",
                "category": "Data Science",
                "price": 69.99,
                "lessons": [
                    {"title": "Data Science Intro", "content": "Overview of data science, types of analytics, and real-world applications.", "order": 1, "section": "Unit 1", "duration": 30},
                    {"title": "Pandas Basics", "content": "Data manipulation with pandas: DataFrames, cleaning, and transformations.", "order": 2, "section": "Unit 1", "duration": 50},
                    {"title": "Data Visualization", "content": "Create compelling visualizations with matplotlib and seaborn.", "order": 3, "section": "Unit 2", "duration": 45},
                    {"title": "Statistical Analysis", "content": "Learn descriptive statistics, distributions, and hypothesis testing.", "order": 4, "section": "Unit 2", "duration": 55},
                    {"title": "Working with Real Data", "content": "Handle missing data, outliers, and perform exploratory data analysis.", "order": 5, "section": "Unit 3", "duration": 60},
                ]
            },
            {
                "title": "JavaScript Mastery",
                "description": "Master JavaScript for web development.",
                "category": "Programming",
                "price": 59.99,
                "lessons": [
                    {"title": "JS Fundamentals", "content": "Core JavaScript concepts: variables, types, operators, and control flow.", "order": 1, "section": "Part 1", "duration": 40},
                    {"title": "ES6 Features", "content": "Modern JavaScript: arrow functions, destructuring, template literals, and spread operator.", "order": 2, "section": "Part 1", "duration": 45},
                    {"title": "Async Programming", "content": "Promises, async/await, callbacks, and handling asynchronous operations.", "order": 3, "section": "Part 2", "duration": 50},
                    {"title": "DOM Manipulation", "content": "Interact with the DOM: selecting elements, events, and dynamic updates.", "order": 4, "section": "Part 2", "duration": 35},
                    {"title": "APIs and Fetch", "content": "Make HTTP requests with fetch API and handle responses.", "order": 5, "section": "Part 3", "duration": 40},
                ]
            },
            {
                "title": "Machine Learning with Python",
                "description": "Build machine learning models.",
                "category": "Data Science",
                "price": 89.99,
                "lessons": [
                    {"title": "ML Fundamentals", "content": "Introduction to machine learning: supervised vs unsupervised learning.", "order": 1, "section": "Basics", "duration": 35},
                    {"title": "Supervised Learning", "content": "Classification and regression: Decision Trees, Random Forests, Logistic Regression.", "order": 2, "section": "Algorithms", "duration": 60},
                    {"title": "Model Evaluation", "content": "Metrics: accuracy, precision, recall, F1-score, and cross-validation.", "order": 3, "section": "Evaluation", "duration": 45},
                    {"title": "Feature Engineering", "content": "Prepare data: scaling, encoding, and feature selection techniques.", "order": 4, "section": "Advanced", "duration": 55},
                    {"title": "Unsupervised Learning", "content": "Clustering with K-Means, hierarchical clustering, and dimensionality reduction.", "order": 5, "section": "Advanced", "duration": 50},
                ]
            },
            {
                "title": "Advanced CSS & Animations",
                "description": "Create beautiful responsive designs.",
                "category": "Web Development",
                "price": 39.99,
                "lessons": [
                    {"title": "CSS Fundamentals", "content": "CSS syntax, selectors, specificity, and the cascade.", "order": 1, "section": "Basics", "duration": 30},
                    {"title": "Flexbox & Grid", "content": "Modern layouts with CSS Flexbox and CSS Grid for responsive design.", "order": 2, "section": "Layouts", "duration": 45},
                    {"title": "Animations", "content": "Create smooth animations with CSS transitions and keyframe animations.", "order": 3, "section": "Advanced", "duration": 40},
                    {"title": "Responsive Design", "content": "Media queries, mobile-first approach, and accessible responsive layouts.", "order": 4, "section": "Advanced", "duration": 50},
                    {"title": "Advanced Selectors", "content": "Pseudo-classes, pseudo-elements, and CSS custom properties (variables).", "order": 5, "section": "Advanced", "duration": 35},
                ]
            },
            {
                "title": "SQL Database Design",
                "description": "Master relational databases.",
                "category": "Programming",
                "price": 54.99,
                "lessons": [
                    {"title": "SQL Basics", "content": "SELECT queries, WHERE clauses, and basic filtering with SQL.", "order": 1, "section": "Fundamentals", "duration": 35},
                    {"title": "Joins", "content": "INNER JOIN, LEFT JOIN, RIGHT JOIN, and FULL OUTER JOIN operations.", "order": 2, "section": "Fundamentals", "duration": 45},
                    {"title": "Advanced Queries", "content": "Subqueries, aggregations, GROUP BY, HAVING, and window functions.", "order": 3, "section": "Advanced", "duration": 55},
                    {"title": "Data Modification", "content": "INSERT, UPDATE, DELETE operations and transaction management.", "order": 4, "section": "Advanced", "duration": 40},
                    {"title": "Indexing and Performance", "content": "Database optimization: indexes, query optimization, and execution plans.", "order": 5, "section": "Advanced", "duration": 50},
                ]
            },
            {
                "title": "Mobile App Development",
                "description": "Build cross-platform mobile apps.",
                "category": "Mobile",
                "price": 74.99,
                "lessons": [
                    {"title": "Mobile Basics", "content": "Getting started with mobile development and native vs cross-platform.", "order": 1, "section": "Intro", "duration": 30},
                    {"title": "UI Design", "content": "Create beautiful mobile interfaces following platform guidelines.", "order": 2, "section": "Design", "duration": 45},
                    {"title": "Navigation", "content": "Implement navigation patterns: stack, tab, and drawer navigation.", "order": 3, "section": "Development", "duration": 40},
                    {"title": "State Management", "content": "Manage app state in mobile applications efficiently.", "order": 4, "section": "Development", "duration": 50},
                    {"title": "API Integration", "content": "Connect mobile apps to backend services and APIs.", "order": 5, "section": "Development", "duration": 45},
                ]
            },
            {
                "title": "DevOps Essentials",
                "description": "Master deployment and infrastructure.",
                "category": "DevOps",
                "price": 84.99,
                "lessons": [
                    {"title": "Docker Basics", "content": "Containerization with Docker: images, containers, and best practices.", "order": 1, "section": "Containers", "duration": 40},
                    {"title": "Docker Compose", "content": "Orchestrate multi-container applications with Docker Compose.", "order": 2, "section": "Containers", "duration": 35},
                    {"title": "Kubernetes", "content": "Container orchestration with Kubernetes: pods, deployments, and services.", "order": 3, "section": "Orchestration", "duration": 60},
                    {"title": "CI/CD Pipelines", "content": "Build continuous integration and deployment pipelines.", "order": 4, "section": "DevOps", "duration": 50},
                    {"title": "Monitoring", "content": "Monitor applications and infrastructure with logging and metrics.", "order": 5, "section": "DevOps", "duration": 45},
                ]
            },
            {
                "title": "Cloud Computing with AWS",
                "description": "Build scalable cloud applications.",
                "category": "Cloud",
                "price": 94.99,
                "lessons": [
                    {"title": "AWS Basics", "content": "AWS fundamentals: regions, availability zones, and core services.", "order": 1, "section": "Intro", "duration": 35},
                    {"title": "EC2 and Compute", "content": "Elastic Compute Cloud: instances, security groups, and autoscaling.", "order": 2, "section": "Services", "duration": 50},
                    {"title": "Storage and Databases", "content": "S3, DynamoDB, RDS: AWS storage and database solutions.", "order": 3, "section": "Services", "duration": 55},
                    {"title": "Networking", "content": "VPC, subnets, route tables, and load balancing in AWS.", "order": 4, "section": "Advanced", "duration": 60},
                    {"title": "Serverless Computing", "content": "Lambda, API Gateway, and serverless architecture patterns.", "order": 5, "section": "Advanced", "duration": 50},
                ]
            }
        ]
        
        # Add all courses to database
        for idx, course_data in enumerate(courses_data):
            course = Course(
                title=course_data["title"],
                description=course_data["description"],
                category=course_data["category"],
                price=course_data["price"],
                instructor_id=instructor.id
            )
            db.add(course)
            db.flush()  # Flush to get the course ID
            
            # Add lessons for this course
            for lesson_data in course_data["lessons"]:
                lesson = Lesson(
                    lesson_title=lesson_data["title"],
                    content_body=lesson_data["content"],
                    order_sequence=lesson_data["order"],
                    section_title=lesson_data["section"],
                    duration_minutes=lesson_data.get("duration", 30),
                    course_id=course.id
                )
                db.add(lesson)
        
        db.commit()
        
        # Enroll student in first few courses
        for course_id in [1, 2, 3]:
            enrollment = Enrollment(
                user_id=student.id,
                course_id=course_id,
                current_status="Active"
            )
            db.add(enrollment)
        
        db.commit()
        print("✅ Database seeded successfully with 10 courses!")
        
    except Exception as e:
        db.rollback()
        print(f"❌ Error seeding database: {e}")
    finally:
        db.close()
