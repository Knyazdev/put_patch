from time import sleep
from src.tasks.celery_app import celery_instance
import os
from PIL import Image
from src.utils.db_manager import DBManager
from src.database import async_session_maker_null_pull
import asyncio


@celery_instance.task
def test_task():
    sleep(5)
    print("Ya svoboden")


@celery_instance.task
def resize_image(image_path: str):
    sizes = [i for i in range(500, 1000, 2)]
    output_folder = 'src/static/images'

    img = Image.open(image_path)

    base_name = os.path.basename(image_path)
    name, ext = os.path.splitext(base_name)

    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    for size in sizes:
        img_resized = img.resize(
            (size, int(img.height * (size / img.width))), Image.Resampling.LANCZOS)
        new_file = f"{name}_{size}px{ext}"

        output_path = os.path.join(output_folder, new_file)
        img_resized.save(output_path)
    print(f"Images had saved in sizes: {sizes}")


async def get_emails_to_users_with_today_checkin_helper():
    print("I am running")
    async with DBManager(session_factory=async_session_maker_null_pull) as db:
        bookings = await db.booking.get_bookings_with_today_checkin()
        print(f"{bookings=}")


@celery_instance.task(name="booking_today_checkin")
def send_emails_to_users_with_today_checkin():
    asyncio.run(get_emails_to_users_with_today_checkin_helper())
