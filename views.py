from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from .utilities import analysis
from django.http import JsonResponse
from django.core.files.storage import FileSystemStorage
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from PIL import Image
from django.http import JsonResponse
from rest_framework.views import APIView

class UploadImage(APIView):
    parser_classes = (MultiPartParser, FormParser)
    def post(self, request, *args, **kwargs):
        if 'image' not in request.data:
            return JsonResponse({'error': 'No image uploaded'}, status=400)
        try:
            img = Image.open(request.data.get('image'))
            img.verify()  # Check if the file is a valid image
            image = request.data.get('image')
            fs = FileSystemStorage(location=settings.MEDIA_ROOT)
            filename = fs.save(image.name, image)
            path = fs.path(filename)
            result = analysis(path)
            if result == 'Error: Could not read image file':
                return Response({'error': 'Error In Analysis Image Is Invalid'}, status=400)
            data = {
                "result" : result
                }
            return Response(data)
        except Exception as e:
            return JsonResponse({'error': 'Invalid image file'}, status=400)
