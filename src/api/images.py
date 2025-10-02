from fastapi import APIRouter, UploadFile
import shutil
from src.tasks.tasks import resize_image

router = APIRouter(prefix='/images', tags=['Images'])


@router.post('')
def upload_image(file: UploadFile):
    file_name = f"src/static/images/{file.filename}"
    with open(file_name, 'wb+') as new_file:
        shutil.copyfileobj(file.file, new_file)

    resize_image.delay(file_name)
    return {
        'error': None,
        'result': {}
    }
