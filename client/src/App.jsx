import { BrowserRouter as Router, Routes, Route, Navigate } from "react-router-dom";
import { useAuthStore } from "./store/authStore";
import AppLayout from "./layouts/AppLayout";
import ProtectedRoute from "./components/ProtectedRoute";
import Landing from "./pages/Landing";
import Login from "./pages/Login";
import Register from "./pages/Register";
import Recovery from "./pages/Recovery";
import ResetPassword from "./pages/ResetPassword";
import Dashboard from "./pages/Dashboard";
import Catalog from "./pages/Catalog";
import CourseDetails from "./pages/CourseDetails";
import CoursePlayer from "./pages/CoursePlayer";
import Studio from "./pages/Studio";
import NewCourse from "./pages/NewCourse";
import EditCourse from "./pages/EditCourse";
import Settings from "./pages/Settings";

function App() {
  const token = useAuthStore((s) => s.token);

  return (
    <Router>
      <Routes>
        <Route path="/" element={token ? <Navigate to="/dashboard" /> : <Landing />} />
        <Route path="/login" element={token ? <Navigate to="/dashboard" /> : <Login />} />
        <Route path="/register" element={token ? <Navigate to="/dashboard" /> : <Register />} />
        <Route path="/account/recovery" element={<Recovery />} />
        <Route path="/account/reset" element={<ResetPassword />} />
        
        <Route element={<ProtectedRoute />}>
          <Route element={<AppLayout />}>
            <Route path="/dashboard" element={<Dashboard />} />
            <Route path="/catalog" element={<Catalog />} />
            <Route path="/course/:id" element={<CourseDetails />} />
            <Route path="/course/:id/play" element={<CoursePlayer />} />
            <Route path="/studio" element={<Studio />} />
            <Route path="/studio/new" element={<NewCourse />} />
            <Route path="/studio/edit/:id" element={<EditCourse />} />
            <Route path="/settings" element={<Settings />} />
          </Route>
        </Route>
      </Routes>
    </Router>
  );
}

export default App
