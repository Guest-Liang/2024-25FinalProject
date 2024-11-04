from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import MultiPartParser, FormParser
from django.http import JsonResponse

class DecryptView(APIView):
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request, *args, **kwargs):
        # Check if has file
        if 'file' not in request.data:
            return Response({"error": "No file provided"}, status=status.HTTP_400_BAD_REQUEST)

        file = request.data['file']

        try:
            result = '''
            {
                status: "success",
            }
            '''
            return JsonResponse({"message": "File processed successfully", "result": result})
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class EchoView(APIView):
    def post(self, request, *args, **kwargs):
        input_text = request.data.get('text', None)
        if input_text is None:
            return Response({"error": "No text provided"}, status=status.HTTP_400_BAD_REQUEST)
        reversed_text = input_text[::-1]
        return Response({"original_text": input_text, "reversed_text": reversed_text}, status=status.HTTP_200_OK)
    
