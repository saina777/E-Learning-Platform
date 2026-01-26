export interface User {
  id: number;
  email: string;
  full_name: string;
  role: 'student' | 'instructor' | 'admin';
  avatar_url?: string;
  created_at: string;
}

export interface Module {
  id: number;
  title: string;
  description?: string;
  order_index: number;
  lessons?: Lesson[];
}

export interface Lesson {
  id: number;
  title: string;
  content: string;
  video_url?: string;
  order_index: number;
  module_id: number;
  duration?: number; // in minutes
}

export interface Course {
  id: number;
  title: string;
  description: string;
  thumbnail_url?: string;
  instructor_id: number;
  price: number;
  is_published: boolean;
  created_at: string;
  modules?: Module[];
  instructor?: User;
  enrollment_count?: number;
}

export interface Enrollment {
  id: number;
  user_id: number;
  course_id: number;
  enrolled_at: string;
  current_status: 'active' | 'completed' | 'cancelled';
  progress_percentage: number;
  completed_lessons?: number[];
  last_accessed_at?: string;
}

export interface ApiResponse<T> {
  data: T;
  message: string;
  success: boolean;
}

export interface LoginRequest {
  email: string;
  password: string;
}

export interface LoginResponse {
  access_token: string;
  token_type: string;
  user: User;
}

export interface RegisterRequest {
  email: string;
  password: string;
  full_name: string;
  role?: 'student' | 'instructor';
}