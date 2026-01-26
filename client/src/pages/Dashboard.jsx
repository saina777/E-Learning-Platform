import { useEffect, useState } from "react";

export default function Dashboard({ userId }) {
  const [summary, setSummary] = useState([]);

  useEffect(() => {
    fetch(`/api/progress/summary?user_id=${userId}`)
      .then(res => res.json())
      .then(setSummary);
  }, [userId]);

  return (
    <div>
      <h2>My Progress</h2>
      <ul>
        {summary.map(course => (
          <li key={course.course_id}>
            Course {course.course_id}: {course.completed}/{course.total}
          </li>
        ))}
      </ul>
    </div>
  );
}
