import { useState, useEffect } from "react";
import CourseCard from "./CourseCard";
import { getAllCourses, removeCourse } from "../services/courseService";

function CourseList() {
  const [courses, setCourses] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  const loadCourses = async () => {
    try {
      setLoading(true);
      const data = await getAllCourses();
      setCourses(data);
    } catch (err) {
      setError(err.message || "Failed to load courses");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadCourses();
  }, []);

  const handleDelete = async (id) => {
    try {
      await removeCourse(id);
      setCourses((prev) => prev.filter((c) => c.course_id !== id));
    } catch (err) {
      setError(err.message || "Failed to delete course");
    }
  };

  if (loading) return <p className="loading">Loading courses...</p>;

  return (
    <section className="course-list">
      <h2>Courses</h2>
      {error && <p className="form-error">{error}</p>}
      {courses.length === 0 ? (
        <p className="empty">No courses found.</p>
      ) : (
        <div className="card-grid">
          {courses.map((course) => (
            <CourseCard
              key={course.course_id}
              course={course}
              onDelete={handleDelete}
            />
          ))}
        </div>
      )}
    </section>
  );
}

export default CourseList;
