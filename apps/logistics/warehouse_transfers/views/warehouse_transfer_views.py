from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

class FieldInspectionUploadView(APIView):
    def post(self, request, *args, **kwargs):
        return Response({"message": "Field inspection uploaded successfully"}, status=status.HTTP_201_CREATED)