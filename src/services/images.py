from src.services.base import BaseService
from fastapi import UploadFile
import shutil
from src.tasks.tasks import resize_image


class ImageService(BaseService):
    def upload(file: UploadFile):
        file_name = f"src/static/images/{file.filename}"
        with open(file_name, "wb+") as new_file:
            shutil.copyfileobj(file.file, new_file)

        resize_image.delay(file_name)