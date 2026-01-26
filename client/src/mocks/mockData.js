export const mockUsers = {
  student: {
    id: 2,
    full_name: "Student Demo",
    email: "student@example.com",
    role: "student",
  },
  instructor: {
    id: 1,
    full_name: "Instructor Demo",
    email: "instructor@example.com",
    role: "instructor",
  },
};

export const mockCourses = [
  {
    id: 101,
    title: "Web Development Foundations",
    description:
      "Learn the building blocks of modern web apps with practical projects and clear explanations.",
    category: "Web Development",
    price: 0,
    instructor_id: 1,
    image_url:
      "https://images.unsplash.com/photo-1518770660439-4636190af475?auto=format&fit=crop&w=1200&q=80",
    created_at: new Date().toISOString(),
  },
  {
    id: 102,
    title: "Data Literacy for Everyone",
    description:
      "Understand data, dashboards, and everyday analytics—no math anxiety required.",
    category: "Data",
    price: 19.99,
    instructor_id: 1,
    image_url:
      "https://images.unsplash.com/photo-1551288049-bebda4e38f71?auto=format&fit=crop&w=1200&q=80",
    created_at: new Date().toISOString(),
  },
  {
    id: 103,
    title: "UX Design Essentials",
    description:
      "Design user-friendly interfaces using simple principles, patterns, and feedback loops.",
    category: "Design",
    price: 29.99,
    instructor_id: 1,
    image_url:
      "https://images.unsplash.com/photo-1559028012-481c04fa702d?auto=format&fit=crop&w=1200&q=80",
    created_at: new Date().toISOString(),
  },
];

export const mockLessonsByCourseId = {
  101: [
    {
      id: 1001,
      course_id: 101,
      section_title: "Getting Started",
      lesson_title: "Welcome & how to use this course",
      content_body:
        "In this course, you’ll learn step-by-step. Use the sidebar to navigate lessons and mark them complete.",
      video_link: "https://www.youtube.com/embed/dQw4w9WgXcQ",
      order_sequence: 1,
    },
    {
      id: 1002,
      course_id: 101,
      section_title: "Core Concepts",
      lesson_title: "HTML basics",
      content_body:
        "HTML provides structure. Headings, paragraphs, lists, and links are your core building blocks.",
      video_link: "https://www.youtube.com/embed/pQN-pnXPaVg",
      order_sequence: 2,
    },
    {
      id: 1003,
      course_id: 101,
      section_title: "Core Concepts",
      lesson_title: "CSS basics",
      content_body:
        "CSS controls presentation. Learn selectors, spacing, and layout fundamentals.",
      video_link: "https://www.youtube.com/embed/yfoY53QXEnI",
      order_sequence: 3,
    },
  ],
  102: [
    {
      id: 2001,
      course_id: 102,
      section_title: "Foundations",
      lesson_title: "What is data literacy?",
      content_body:
        "Data literacy is the ability to read, understand, create, and communicate data as information.",
      video_link: "https://www.youtube.com/embed/ua-CiDNNj30",
      order_sequence: 1,
    },
    {
      id: 2002,
      course_id: 102,
      section_title: "Foundations",
      lesson_title: "Charts that people misread",
      content_body:
        "We’ll cover common chart pitfalls and how to interpret data responsibly.",
      video_link: "https://www.youtube.com/embed/5Zg-C8AAIGg",
      order_sequence: 2,
    },
  ],
  103: [
    {
      id: 3001,
      course_id: 103,
      section_title: "UX Basics",
      lesson_title: "The job of UX",
      content_body:
        "UX reduces friction and increases confidence. Your goal is clarity, not complexity.",
      video_link: "https://www.youtube.com/embed/Ovj4hFxko7c",
      order_sequence: 1,
    },
    {
      id: 3002,
      course_id: 103,
      section_title: "UX Basics",
      lesson_title: "User flows",
      content_body:
        "User flows help you map how a person completes a task—one step at a time.",
      video_link: "https://www.youtube.com/embed/9B0iB6Yv7a8",
      order_sequence: 2,
    },
  ],
};
