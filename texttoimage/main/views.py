from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from main.tasks import process_prompt


class TextToImageView(APIView):
    """
    API to convert text to image
    accepts a list of prompts separated by "|"
    """

    def get(self, request):
        data = request.GET
        prompts = data.get("prompts")
        prompts = prompts.split("|")
        for prompt in prompts:
            process_prompt.delay(prompt)
        return Response({"message": "Image Creation Processed!"})
