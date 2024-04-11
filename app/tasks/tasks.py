from pathlib import Path

from PIL import Image

from app.tasks.celery import celery


@celery.task
def proccess_pic(
    path: str,
):
    image_path = Path(path)
    image = Image.open(image_path)
    image_resized_large = image.resize((1000, 500))
    image_resized_small = image.resize((200, 100))
    image_resized_large.save(
        f'app/static/images/large_{image_path.name}'
    )
    image_resized_small.save(
        f'app/static/images/small_{image_path.name}'
    )
