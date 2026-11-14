import CourseForm from "../components/CourseForm";
import CourseList from "../components/CourseList";

function HomePage() {
  return (
    <main className="home-page">
      <header className="page-header">
        <h1>Course &amp; Student Manager</h1>
        <p>Frontend for the Course and Student API</p>
      </header>
      <div className="page-body">
        <CourseList />
        <CourseForm onCourseCreated={() => window.location.reload()} />
      </div>
    </main>
  );
}

export default HomePage;
