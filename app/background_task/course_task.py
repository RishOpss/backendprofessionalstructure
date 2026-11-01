import time


def send_course_creation_email(course_name: str, email: str):

    print(f"Sending email to: {email}")

    # Simulate email processing
    time.sleep(5)

    print(f"Email sent successfully!")
    print(f"New course created: {course_name}")