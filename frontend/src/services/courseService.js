import {
  fetchCourses,
  fetchCourseById,
  createCourse,
  deleteCourse,
} from "../api/courses";

async function getAllCourses() {
  return fetchCourses();
}

async function getCourseById(id) {
  return fetchCourseById(id);
}

async function addCourse(course) {
  return createCourse(course);
}

async function removeCourse(id) {
  return deleteCourse(id);
}

export { getAllCourses, getCourseById, addCourse, removeCourse };
