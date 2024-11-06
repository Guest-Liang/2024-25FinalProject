from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import MultiPartParser, FormParser
from django.http import JsonResponse
from django.conf import settings
from datetime import datetime
import os, base64, random
# Personal imports
import LSB, En_Decryption

class DecryptView(APIView):
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request, *args, **kwargs):
        # Check if file is provided
        if 'file' not in request.data:
            return Response({"error": "No file provided"}, status=status.HTTP_400_BAD_REQUEST)

        File = request.data['file']
        Timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        
        # Save file to TRANSIT_DIR
        FilePath = os.path.join(settings.TRANSIT_DIR, f"Uploaded_{Timestamp}.png")
        with open(FilePath, 'wb') as des:
            for chunk in File.chunks():
                des.write(chunk)

        try:
            # Decode the encrypted information from the image
            EncryptedInfo = LSB.LSB_Decode(FilePath)
            
            # Decrypt the file data
            DecryptedData, FileName = En_Decryption.DecryptFile(EncryptedInfo)
            
            # Save the decrypted file to TRANSIT_DIR
            OutputPath = os.path.join(settings.TRANSIT_DIR, f"{Timestamp}_{base64.b64decode(FileName).decode('utf-8')}")
            with open(OutputPath, 'wb') as OutputFile:
                OutputFile.write(DecryptedData)
            
            result = {
                "status": "success",
                "DecryptedFilePath": OutputPath
            }
            os.remove(FilePath)
            return JsonResponse({"message": "File processed successfully", "result": result})

        except Exception as e:
            os.remove(FilePath)
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class EncryptView(APIView):
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request, *args, **kwargs):

        isUseCustomImg = request.data.get('isUseCustomImg')
        CustomImgPath = os.path.join(settings.TRANSIT_DIR, 'custom.png')
        if isUseCustomImg is not None:
            with open(CustomImgPath, 'wb') as des:
                for chunk in isUseCustomImg.chunks():
                    des.write(chunk)

        # Check if file is provided
        if 'file' not in request.data and 'file[]' not in request.data:
            os.remove(CustomImgPath)
            return Response({"error": "No file provided"}, status=status.HTTP_400_BAD_REQUEST)

        Files = request.data.getlist('file')
        Timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        results = []

        for i,File in enumerate(Files):
            FilePath = os.path.join(settings.TRANSIT_DIR, File.name)
            
            # Save each file to the specified directory
            with open(FilePath, 'wb') as des:
                for chunk in File.chunks():
                    des.write(chunk)

            try:
                # Encrypt the file
                EncryptedInfo = En_Decryption.EncryptFile(FilePath)

                # Encode the encrypted info into an image
                ImagePath = os.path.join(settings.PIC_DIR, random.choice(os.listdir(settings.PIC_DIR))) if isUseCustomImg == None else CustomImgPath
                OutputImagePath = os.path.join(settings.TRANSIT_DIR, f"EncodedImage_{Timestamp}_{i}.png")
                LSB.LSB_Encode(ImagePath, OutputImagePath, EncryptedInfo)
                
                results.append({
                    "status": "success",
                    "EncodedImagePath": OutputImagePath
                })

            except Exception as e:
                os.remove(FilePath)
                print("Error: ", e)
                return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
                                
            os.remove(FilePath)

        if os.path.exists(CustomImgPath):
            os.remove(CustomImgPath)
        return JsonResponse({"message": "File encrypted and saved successfully", "result": results}, status=status.HTTP_200_OK)
    

class EchoView(APIView):
    def post(self, request, *args, **kwargs):
        input_text = request.data.get('text', None)
        if input_text is None:
            return Response({"error": "No text provided"}, status=status.HTTP_400_BAD_REQUEST)
        reversed_text = input_text[::-1]
        return Response({"original_text": input_text, "reversed_text": reversed_text}, status=status.HTTP_200_OK)
    
