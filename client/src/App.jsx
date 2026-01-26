import { BrowserRouter, Routes, Route } from "react-router-dom";
import { useEffect } from "react";
import AppLayout from "./layouts/AppLayout";
import Landing from "./pages/Landing";
import Catalog from "./pages/Catalog";
import CourseDetails from "./pages/CourseDetails";
import Login from "./pages/Login";
import Register from "./pages/Register";
import Recovery from "./pages/Recovery";
import ResetPassword from "./pages/ResetPassword";
import Dashboard from "./pages/Dashboard";
import CoursePlayer from "./pages/CoursePlayer";
import Settings from "./pages/Settings";
import Studio from "./pages/Studio";
import NewCourse from "./pages/NewCourse";
import EditCourse from "./pages/EditCourse";
import ProtectedRoute from "./components/ProtectedRoute";
import { useAuthStore } from "./store/authStore";


function App() {
  const hydrate = useAuthStore((state) => state.hydrate);

  useEffect(() => {
    hydrate();
  }, [hydrate]);

  return (
    <BrowserRouter>
      <Routes>
        <Route element={<AppLayout />}>
          <Route path="/" element={<Landing />} />
          <Route path="/catalog" element={<Catalog />} />
          <Route path="/courses/:courseId" element={<CourseDetails />} />
          <Route path="/login" element={<Login />} />
          <Route path="/register" element={<Register />} />
          <Route path="/account/recovery" element={<Recovery />} />
          <Route path="/account/reset/:token" element={<ResetPassword />} />

          <Route element={<ProtectedRoute />}>
            <Route path="/dashboard" element={<Dashboard />} />
            <Route path="/learn/:courseId" element={<CoursePlayer />} />
            <Route path="/settings" element={<Settings />} />
          </Route>

          <Route element={<ProtectedRoute allowedRoles={["instructor"]} />}>
            <Route path="/studio" element={<Studio />} />
            <Route path="/studio/courses/new" element={<NewCourse />} />
            <Route path="/studio/courses/:courseId/edit" element={<EditCourse />} />
          </Route>
        </Route>
      </Routes>
    </BrowserRouter>
  );
}

export default App;
