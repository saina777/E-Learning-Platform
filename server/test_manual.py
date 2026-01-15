import requests
import json

BASE_URL = "http://localhost:8000"

def test_courses():
    # Test create course
    print("Testing CREATE course...")
    course_data = {
        "title": "Python Basics",
        "description": "Learn Python fundamentals"
    }
    response = requests.post(f"{BASE_URL}/courses/", json=course_data)
    print(f"Status: {response.status_code}")
    if response.status_code == 201:
        course = response.json()
        course_id = course["id"]
        print(f"Created course ID: {course_id}")
        
        # Test get course
        print("\nTesting GET course...")
        response = requests.get(f"{BASE_URL}/courses/{course_id}")
        print(f"Status: {response.status_code}")
        print(f"Course: {response.json()}")
        
        # Test update course
        print("\nTesting UPDATE course...")
        update_data = {
            "title": "Advanced Python",
            "description": "Advanced Python concepts"
        }
        response = requests.put(f"{BASE_URL}/courses/{course_id}", json=update_data)
        print(f"Status: {response.status_code}")
        print(f"Updated course: {response.json()}")
        
        # Test delete course
        print("\nTesting DELETE course...")
        response = requests.delete(f"{BASE_URL}/courses/{course_id}")
        print(f"Status: {response.status_code}")
        
        # Verify deletion
        response = requests.get(f"{BASE_URL}/courses/{course_id}")
        print(f"Get after delete status: {response.status_code}")
    else:
        print(f"Error: {response.text}")

if __name__ == "__main__":
    test_courses()