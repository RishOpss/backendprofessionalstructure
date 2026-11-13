import time
import asyncio
async def send_course_creation_email(course_name : str, email : str):
    await asyncio.sleep(10)
    print(f"Sending email to {email}")
    print(f"Email Sent Succesfully")
    print(f"New Course created:{course_name}")
    
