import React from "react";
import ReactDOM from "react-dom/client";
import { createBrowserRouter, RouterProvider } from "react-router-dom";
import "./index.css";

import AppLayout from "./layouts/AppLayout";
import ProtectedRoute from "./components/ProtectedRoute";

// Public pages
import Landing from "./pages/Landing";
import Catalog from "./pages/Catalog";
import CourseDetails from "./pages/CourseDetails";
import Login from "./pages/Login";
import Register from "./pages/Register";
import Recovery from "./pages/Recovery";
import ResetPassword from "./pages/ResetPassword";

// Protected pages
import Dashboard from "./pages/Dashboard";
import CoursePlayer from "./pages/CoursePlayer";
import Studio from "./pages/Studio";
import NewCourse from "./pages/NewCourse";
import EditCourse from "./pages/EditCourse";
import Settings from "./pages/Settings";

const router = createBrowserRouter([
  {
    element: <AppLayout />,
    children: [
      { path: "/", element: <Landing /> },
      { path: "/catalog", element: <Catalog /> },
      { path: "/courses/:courseId", element: <CourseDetails /> },
      { path: "/login", element: <Login /> },
      { path: "/register", element: <Register /> },
      { path: "/account/recovery", element: <Recovery /> },
      { path: "/account/reset/:token", element: <ResetPassword /> },

      // Protected (5+)
      {
        element: <ProtectedRoute />,
        children: [
          { path: "/dashboard", element: <Dashboard /> },
          { path: "/learn/:courseId", element: <CoursePlayer /> },
          { path: "/studio", element: <Studio /> },
          { path: "/studio/courses/new", element: <NewCourse /> },
          { path: "/studio/courses/:courseId/edit", element: <EditCourse /> },
          { path: "/settings", element: <Settings /> },
        ],
      },
    ],
  },
]);

ReactDOM.createRoot(document.getElementById("root")).render(
  <React.StrictMode>
    <RouterProvider router={router} />
  </React.StrictMode>
);
