from fastapi import APIRouter, UploadFile
import shutil


router = APIRouter(
    prefix="/files",
    tags=["Загрузка файлов"]
)


@router.post("/upload")
async def upload_file(name: str, file: UploadFile):
    with open(f"app/media/images/{name}.webp", "wb+") as file_object:
        shutil.copyfileobj(file.file, file_object)
