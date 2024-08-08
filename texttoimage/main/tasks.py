from main.models import TextToImage
from celery import shared_task
import os
from django.conf import settings
import requests


@shared_task()
def process_prompt(prompt):
    print(f"Processing prompt: {prompt}")
    text_to_image = TextToImage.objects.create(prompt=prompt)
    text_to_image.status = TextToImage.RequestStatus.PROCESSING
    text_to_image.save()
    # Get the image from the API
    response = requests.post(
        f"https://api.stability.ai/v2beta/stable-image/generate/sd3",
        headers={
            "authorization": f"Bearer {os.environ.get('STABLE_API_API_KEY')}",
            "accept": "image/*",
        },
        files={"none": ""},
        data={
            "prompt": text_to_image.prompt,
            "output_format": "jpeg",
        },
    )

    if response.status_code == 200:
        # Save the image in media folder
        media_path = f"{settings.MEDIA_ROOT}/images/{text_to_image.uuid}.jpeg"
        if not os.path.exists(os.path.dirname(media_path)):
            os.makedirs(os.path.dirname(media_path))
        with open(media_path, "wb") as file:
            file.write(response.content)
    else:
        text_to_image.status = TextToImage.RequestStatus.FAILED
        text_to_image.failed_reason = str(response.json())
        text_to_image.save()

    text_to_image.image = f"/images/{text_to_image.uuid}.jpeg"
    text_to_image.status = TextToImage.RequestStatus.COMPLETED
    text_to_image.save()
