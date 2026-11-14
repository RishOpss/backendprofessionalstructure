import { useState } from "react";
import { addCourse } from "../services/courseService";

function CourseForm({ onCourseCreated }) {
  const [name, setName] = useState("");
  const [duration, setDuration] = useState("");
  const [courseId, setCourseId] = useState("");
  const [error, setError] = useState("");
  const [success, setSuccess] = useState("");

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError("");
    setSuccess("");

    const data = {
      course_id: parseInt(courseId, 10),
      name,
      duration: parseInt(duration, 10),
    };

    try {
      await addCourse(data);
      setSuccess("Course created successfully!");
      setName("");
      setDuration("");
      setCourseId("");
      if (onCourseCreated) onCourseCreated();
    } catch (err) {
      setError(err.message || "Failed to create course");
    }
  };

  return (
    <form className="course-form" onSubmit={handleSubmit}>
      <h2>Create Course</h2>
      {error && <p className="form-error">{error}</p>}
      {success && <p className="form-success">{success}</p>}
      <div className="form-group">
        <label htmlFor="courseId">Course ID</label>
        <input
          id="courseId"
          type="number"
          min="1"
          value={courseId}
          onChange={(e) => setCourseId(e.target.value)}
          required
        />
      </div>
      <div className="form-group">
        <label htmlFor="courseName">Name</label>
        <input
          id="courseName"
          type="text"
          minLength={2}
          maxLength={50}
          value={name}
          onChange={(e) => setName(e.target.value)}
          required
        />
      </div>
      <div className="form-group">
        <label htmlFor="courseDuration">Duration</label>
        <input
          id="courseDuration"
          type="number"
          min="1"
          value={duration}
          onChange={(e) => setDuration(e.target.value)}
          required
        />
      </div>
      <button type="submit" className="btn btn-primary">
        Create Course
      </button>
    </form>
  );
}

export default CourseForm;
