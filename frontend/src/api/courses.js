import { API_BASE_URL } from "../config";

async function fetchCourses() {
  const res = await fetch(`${API_BASE_URL}/courses/`);
  if (!res.ok) throw new Error("Failed to fetch courses");
  return res.json();
}

async function fetchCourseById(courseId) {
  const res = await fetch(`${API_BASE_URL}/courses/${courseId}`);
  if (!res.ok) throw new Error(`Course ${courseId} not found`);
  return res.json();
}

async function createCourse(courseData) {
  const res = await fetch(`${API_BASE_URL}/courses/`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(courseData),
  });
  if (!res.ok) throw new Error("Failed to create course");
  return res.json();
}

async function deleteCourse(courseId) {
  const res = await fetch(`${API_BASE_URL}/courses/${courseId}`, {
    method: "DELETE",
  });
  if (!res.ok) throw new Error("Failed to delete course");
  return res.json();
}

export { fetchCourses, fetchCourseById, createCourse, deleteCourse };
