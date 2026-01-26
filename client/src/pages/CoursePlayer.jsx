import { useEffect, useState } from "react";

export default function CoursePlayer({ courseId, userId }) {
  const [lessons, setLessons] = useState([]);
  const [completed, setCompleted] = useState([]);

  useEffect(() => {
    fetch(`/api/progress/${courseId}?user_id=${userId}`)
      .then(res => res.json())
      .then(data => {
        setLessons(data.lessons);
        setCompleted(data.completed_lessons);
      });
  }, [courseId, userId]);

  const markComplete = async (lessonId) => {
    await fetch(`/api/progress/${courseId}`, {
      method: "PATCH",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        user_id: userId,
        lesson_id: lessonId
      })
    });

    setCompleted(prev => [...prev, lessonId]);
  };

  return (
    <div>
      <h2>Course Lessons</h2>
      <ul>
        {lessons.map(lesson => (
          <li key={lesson.id}>
            {lesson.title}
            {completed.includes(lesson.id) ? (
              <span> ✅</span>
            ) : (
              <button onClick={() => markComplete(lesson.id)}>
                Mark complete
              </button>
            )}
          </li>
        ))}
      </ul>
    </div>
  );
}
