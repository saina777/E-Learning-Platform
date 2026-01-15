from sqlalchemy.orm import Session
from app.db.session import SessionLocal
from app.models.user import User
from app.models.course import Course
from app.models.lesson import Lesson

def create_sample_data():
    db: Session = SessionLocal()
    
    try:
        # Create sample users (instructors and students)
        if not db.query(User).first():
            users = [
                User(
                    full_name="Dr. Sarah Johnson",
                    email="sarah@example.com",
                    password_hash="$2b$12$dummy_hash",
                    role="instructor"
                ),
                User(
                    full_name="Prof. Michael Chen",
                    email="michael@example.com", 
                    password_hash="$2b$12$dummy_hash",
                    role="instructor"
                ),
                User(
                    full_name="Emily Rodriguez",
                    email="emily@example.com",
                    password_hash="$2b$12$dummy_hash",
                    role="instructor"
                ),
                User(
                    full_name="John Student",
                    email="student@example.com",
                    password_hash="$2b$12$dummy_hash",
                    role="student"
                )
            ]
            db.add_all(users)
            db.commit()
            print("Created sample users")

        # Create sample courses
        if not db.query(Course).first():
            courses = [
                Course(
                    title="Python Programming Fundamentals",
                    description="Master Python from basics to advanced concepts. Learn variables, functions, OOP, file handling, and more.",
                    category="Programming",
                    price=99.99,
                    instructor_id=1
                ),
                Course(
                    title="Web Development with React",
                    description="Build modern, responsive web applications using React, hooks, routing, and state management.",
                    category="Web Development", 
                    price=149.99,
                    instructor_id=2
                ),
                Course(
                    title="Data Science and Machine Learning",
                    description="Learn data analysis, visualization, and machine learning algorithms using Python and popular libraries.",
                    category="Data Science",
                    price=199.99,
                    instructor_id=1
                ),
                Course(
                    title="JavaScript ES6+ Mastery",
                    description="Deep dive into modern JavaScript including async/await, promises, modules, and advanced patterns.",
                    category="Programming",
                    price=89.99,
                    instructor_id=3
                ),
                Course(
                    title="Database Design and SQL",
                    description="Learn database design principles, normalization, SQL queries, joins, and optimization techniques.",
                    category="Database",
                    price=119.99,
                    instructor_id=2
                ),
                Course(
                    title="Cloud Computing with AWS",
                    description="Master AWS services including EC2, S3, Lambda, and learn to build scalable cloud applications.",
                    category="Cloud",
                    price=179.99,
                    instructor_id=1
                ),
                Course(
                    title="Mobile App Development with Flutter",
                    description="Build cross-platform mobile apps for iOS and Android using Flutter and Dart.",
                    category="Mobile Development",
                    price=159.99,
                    instructor_id=3
                ),
                Course(
                    title="Cybersecurity Essentials",
                    description="Learn security fundamentals, encryption, network security, and ethical hacking basics.",
                    category="Security",
                    price=139.99,
                    instructor_id=2
                )
            ]
            db.add_all(courses)
            db.commit()
            print("Created sample courses")

        # Create sample lessons with detailed content
        if not db.query(Lesson).first():
            lessons = [
                # Python course lessons (Course 1)
                Lesson(
                    lesson_title="Introduction to Python",
                    content_body="""Welcome to Python Programming! Python is a versatile, high-level programming language known for its simplicity and readability.

In this lesson, you'll learn:
- What makes Python special
- Installing Python on your system
- Running your first Python program
- Understanding the Python interpreter

Python is used in web development, data science, automation, AI, and more. Its clean syntax makes it perfect for beginners while being powerful enough for experts.""",
                    video_link="",
                    order_sequence=1,
                    course_id=1
                ),
                Lesson(
                    lesson_title="Variables and Data Types",
                    content_body="""Variables are containers for storing data values. Python has several built-in data types:

1. Numbers (int, float)
2. Strings (text)
3. Booleans (True/False)
4. Lists (ordered collections)
5. Dictionaries (key-value pairs)

Example:
name = "Alice"  # String
age = 25  # Integer
height = 5.6  # Float
is_student = True  # Boolean

Python is dynamically typed, meaning you don't need to declare variable types explicitly.""",
                    video_link="",
                    order_sequence=2,
                    course_id=1
                ),
                Lesson(
                    lesson_title="Control Flow and Loops",
                    content_body="""Control flow statements let you control the execution of your code based on conditions.

IF Statements:
if condition:
    # code block
elif another_condition:
    # code block
else:
    # code block

Loops:
FOR loop - iterate over sequences
for item in list:
    print(item)

WHILE loop - repeat while condition is true
while condition:
    # code block

These are fundamental building blocks for creating logic in your programs.""",
                    video_link="",
                    order_sequence=3,
                    course_id=1
                ),
                Lesson(
                    lesson_title="Functions and Modules",
                    content_body="""Functions are reusable blocks of code that perform specific tasks.

Defining a function:
def greet(name):
    return f"Hello, {name}!"

Modules are files containing Python code that you can import and use:
import math
result = math.sqrt(16)

Benefits:
- Code reusability
- Better organization
- Easier testing and debugging
- Modular design

Python has a rich standard library with many built-in modules.""",
                    video_link="",
                    order_sequence=4,
                    course_id=1
                ),
                Lesson(
                    lesson_title="Object-Oriented Programming",
                    content_body="""OOP is a programming paradigm based on objects and classes.

Class definition:
class Dog:
    def __init__(self, name, age):
        self.name = name
        self.age = age
    
    def bark(self):
        return "Woof!"

Key concepts:
- Classes and Objects
- Inheritance
- Encapsulation
- Polymorphism

OOP helps organize complex programs and promotes code reuse.""",
                    video_link="",
                    order_sequence=5,
                    course_id=1
                ),
                
                # React course lessons (Course 2)
                Lesson(
                    lesson_title="Getting Started with React",
                    content_body="""React is a JavaScript library for building user interfaces, developed by Facebook.

Key features:
- Component-based architecture
- Virtual DOM for performance
- Declarative syntax
- Rich ecosystem

Setting up:
npx create-react-app my-app
cd my-app
npm start

Your first component:
function Welcome() {
    return <h1>Hello, React!</h1>;
}

React makes building interactive UIs simple and efficient.""",
                    video_link="",
                    order_sequence=1,
                    course_id=2
                ),
                Lesson(
                    lesson_title="JSX and Components",
                    content_body="""JSX is a syntax extension that lets you write HTML-like code in JavaScript.

JSX Example:
const element = <h1>Hello, {name}!</h1>;

Components are the building blocks of React apps:

Function Component:
function Button({ text, onClick }) {
    return <button onClick={onClick}>{text}</button>;
}

Components can be composed to build complex UIs:
<App>
  <Header />
  <MainContent />
  <Footer />
</App>

Props let you pass data to components.""",
                    video_link="",
                    order_sequence=2,
                    course_id=2
                ),
                Lesson(
                    lesson_title="State and Hooks",
                    content_body="""State allows components to manage and respond to changing data.

useState Hook:
const [count, setCount] = useState(0);

function increment() {
    setCount(count + 1);
}

useEffect Hook:
useEffect(() => {
    // Side effects here
    document.title = `Count: ${count}`;
}, [count]);

Hooks let you use state and lifecycle features in function components. They make code cleaner and more reusable.""",
                    video_link="",
                    order_sequence=3,
                    course_id=2
                ),
                Lesson(
                    lesson_title="React Router and Navigation",
                    content_body="""React Router enables navigation between different views in your app.

Setup:
import { BrowserRouter, Routes, Route, Link } from 'react-router-dom';

<BrowserRouter>
  <Routes>
    <Route path="/" element={<Home />} />
    <Route path="/about" element={<About />} />
  </Routes>
</BrowserRouter>

Navigation:
<Link to="/about">About</Link>

Programmatic navigation:
const navigate = useNavigate();
navigate('/dashboard');

Router enables building single-page applications with multiple views.""",
                    video_link="",
                    order_sequence=4,
                    course_id=2
                ),
                
                # Data Science course lessons (Course 3)
                Lesson(
                    lesson_title="Introduction to Data Science",
                    content_body="""Data Science combines statistics, programming, and domain expertise to extract insights from data.

Key areas:
- Data collection and cleaning
- Exploratory data analysis
- Statistical modeling
- Machine learning
- Data visualization

Tools:
- Python (NumPy, Pandas, Scikit-learn)
- Jupyter Notebooks
- Matplotlib, Seaborn

Data science is transforming industries from healthcare to finance.""",
                    video_link="",
                    order_sequence=1,
                    course_id=3
                ),
                Lesson(
                    lesson_title="Data Analysis with Pandas",
                    content_body="""Pandas is a powerful library for data manipulation and analysis.

import pandas as pd

# Load data
df = pd.read_csv('data.csv')

# Explore data
df.head()
df.describe()
df.info()

# Filter data
filtered = df[df['age'] > 25]

# Group and aggregate
grouped = df.groupby('category').mean()

Pandas makes working with structured data intuitive and efficient.""",
                    video_link="",
                    order_sequence=2,
                    course_id=3
                ),
                Lesson(
                    lesson_title="Machine Learning Basics",
                    content_body="""Machine Learning enables computers to learn from data without explicit programming.

Types:
1. Supervised Learning (labeled data)
   - Classification
   - Regression

2. Unsupervised Learning (unlabeled data)
   - Clustering
   - Dimensionality reduction

3. Reinforcement Learning

Simple example with Scikit-learn:
from sklearn.linear_model import LinearRegression

model = LinearRegression()
model.fit(X_train, y_train)
predictions = model.predict(X_test)

ML is the foundation of AI applications.""",
                    video_link="",
                    order_sequence=3,
                    course_id=3
                ),
                
                # JavaScript course lessons (Course 4)
                Lesson(
                    lesson_title="Modern JavaScript Features",
                    content_body="""ES6+ introduced powerful features that make JavaScript more expressive and efficient.

Arrow Functions:
const add = (a, b) => a + b;

Destructuring:
const { name, age } = person;
const [first, second] = array;

Template Literals:
const message = `Hello, ${name}!`;

Spread Operator:
const newArray = [...oldArray, newItem];

These features make code cleaner and more maintainable.""",
                    video_link="",
                    order_sequence=1,
                    course_id=4
                ),
                Lesson(
                    lesson_title="Async JavaScript",
                    content_body="""Asynchronous programming is essential for handling operations that take time.

Promises:
fetch(url)
  .then(response => response.json())
  .then(data => console.log(data))
  .catch(error => console.error(error));

Async/Await:
async function getData() {
  try {
    const response = await fetch(url);
    const data = await response.json();
    return data;
  } catch (error) {
    console.error(error);
  }
}

Async/await makes asynchronous code look synchronous and easier to read.""",
                    video_link="",
                    order_sequence=2,
                    course_id=4
                ),
                
                # Database course lessons (Course 5)
                Lesson(
                    lesson_title="Database Design Principles",
                    content_body="""Good database design is crucial for application performance and maintainability.

Key principles:
1. Normalization - reduce redundancy
2. Primary keys - unique identifiers
3. Foreign keys - relationships
4. Indexes - improve query performance

Entity-Relationship Diagrams help visualize database structure.

Normalization forms:
- 1NF: Atomic values
- 2NF: No partial dependencies
- 3NF: No transitive dependencies

Proper design prevents data anomalies and improves efficiency.""",
                    video_link="",
                    order_sequence=1,
                    course_id=5
                ),
                Lesson(
                    lesson_title="SQL Queries and Joins",
                    content_body="""SQL is the standard language for relational databases.

Basic queries:
SELECT * FROM users WHERE age > 25;

Joins combine data from multiple tables:

INNER JOIN:
SELECT orders.id, users.name
FROM orders
INNER JOIN users ON orders.user_id = users.id;

LEFT JOIN:
SELECT users.name, orders.total
FROM users
LEFT JOIN orders ON users.id = orders.user_id;

Aggregation:
SELECT category, COUNT(*), AVG(price)
FROM products
GROUP BY category;

Mastering SQL is essential for working with data.""",
                    video_link="",
                    order_sequence=2,
                    course_id=5
                ),
                
                # AWS course lessons (Course 6)
                Lesson(
                    lesson_title="Introduction to AWS",
                    content_body="""Amazon Web Services (AWS) is the world's leading cloud platform.

Core services:
- EC2: Virtual servers
- S3: Object storage
- RDS: Managed databases
- Lambda: Serverless computing
- CloudFront: Content delivery

Benefits:
- Scalability
- Pay-as-you-go pricing
- Global infrastructure
- Security and compliance

AWS powers millions of applications worldwide.""",
                    video_link="",
                    order_sequence=1,
                    course_id=6
                ),
                
                # Flutter course lessons (Course 7)
                Lesson(
                    lesson_title="Flutter Fundamentals",
                    content_body="""Flutter is Google's UI toolkit for building natively compiled applications.

Key features:
- Single codebase for iOS and Android
- Hot reload for fast development
- Rich widget library
- High performance

Basic widget:
class MyApp extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      home: Scaffold(
        appBar: AppBar(title: Text('My App')),
        body: Center(child: Text('Hello Flutter!')),
      ),
    );
  }
}

Flutter makes mobile development fast and enjoyable.""",
                    video_link="",
                    order_sequence=1,
                    course_id=7
                ),
                
                # Cybersecurity course lessons (Course 8)
                Lesson(
                    lesson_title="Security Fundamentals",
                    content_body="""Cybersecurity protects systems, networks, and data from digital attacks.

Key concepts:
- Confidentiality: Data privacy
- Integrity: Data accuracy
- Availability: System accessibility

Common threats:
- Malware
- Phishing
- SQL injection
- Cross-site scripting (XSS)
- DDoS attacks

Best practices:
- Strong passwords
- Regular updates
- Encryption
- Access control
- Security awareness

Security is everyone's responsibility.""",
                    video_link="",
                    order_sequence=1,
                    course_id=8
                ),
                Lesson(
                    lesson_title="Encryption and Cryptography",
                    content_body="""Encryption protects data by converting it into unreadable format.

Types:
1. Symmetric encryption (same key)
   - AES, DES

2. Asymmetric encryption (public/private keys)
   - RSA, ECC

Hashing:
- One-way function
- Used for passwords
- SHA-256, bcrypt

SSL/TLS:
- Secure web communication
- HTTPS protocol

Cryptography is the foundation of digital security.""",
                    video_link="",
                    order_sequence=2,
                    course_id=8
                )
            ]
            db.add_all(lessons)
            db.commit()
            print("Created sample lessons")
            
        print("Sample data created successfully!")
        
    except Exception as e:
        print(f"Error creating sample data: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    create_sample_data()