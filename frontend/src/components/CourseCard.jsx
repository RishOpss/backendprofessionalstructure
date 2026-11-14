function CourseCard({ course, onDelete }) {
  return (
    <div className="course-card">
      <h3>{course.name}</h3>
      <p>
        <strong>ID:</strong> {course.course_id}
      </p>
      <p>
        <strong>Duration:</strong> {course.duration}
      </p>
      <button
        className="btn btn-danger"
        onClick={() => onDelete(course.course_id)}
      >
        Delete
      </button>
    </div>
  );
}

export default CourseCard;
