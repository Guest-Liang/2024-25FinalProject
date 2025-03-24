from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import MultiPartParser, FormParser
from django.http import JsonResponse, FileResponse
from django.conf import settings
from datetime import datetime
import os, base64, random, urllib.parse, mimetypes, logging, pdb
logger = logging.getLogger(__name__)
# Personal imports
import LSB, En_Decryption, Email
from .responses import CustomResponse

class DecryptView(APIView):
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request, *args, **kwargs):
        logger.info(f"Receive Post Request in Decryption, Start processing. Data Body: {request.data}")
        # Check if file is provided
        if 'file' not in request.data and 'file[]' not in request.data:
            return CustomResponse(error="No file provided", status=status.HTTP_400_BAD_REQUEST)

        Files = request.data.getlist('file')
        Timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        Results = []
        
        for i, File in enumerate(Files):
            
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
                OutputPath = os.path.join(settings.TRANSIT_DIR, f"{Timestamp}_{base64.urlsafe_b64decode(FileName).decode('utf-8')}")
                with open(OutputPath, 'wb') as OutputFile:
                    OutputFile.write(DecryptedData)
            
                Results.append({
                    'status': "success",
                    "DecryptedFilePath": OutputPath
                })

            except Exception as e:
                os.remove(FilePath)
                logger.error("Error: ",e)
                return CustomResponse(error=str(e), status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            
            os.remove(FilePath)
        
        logger.info("File decrypted successfully. End of processing.")

        return CustomResponse(results=Results, message="File decrypted successfully", status=status.HTTP_200_OK)


class EncryptView(APIView):
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request, *args, **kwargs):
        logger.info(f"Receive Post Request in Encryption, Start processing. Data Body: {request.data}")

        isUseCustomImg = request.data.get('isUseCustomImg')
        CustomImgPath = os.path.join(settings.TRANSIT_DIR, 'custom.png')
        EmailAddress = request.data.get('EmailAddress')

        if isUseCustomImg is not None:
            with open(CustomImgPath, 'wb') as des:
                for chunk in isUseCustomImg.chunks():
                    des.write(chunk)

        # Check if file is provided
        if 'file' not in request.data and 'file[]' not in request.data:
            os.remove(CustomImgPath)
            return CustomResponse(error="No file provided", status=status.HTTP_400_BAD_REQUEST)

        Files = request.data.getlist('file')
        Timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        Results = []
        OutputImagePaths = []

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
                OutputImagePath = os.path.join(settings.TRANSIT_DIR, f"{File.name}_ImageKey_{Timestamp}.png")
                LSB.LSB_Encode(ImagePath, OutputImagePath, EncryptedInfo)
                
                Results.append({
                    "status": "success",
                    "EncodedImagePath": OutputImagePath
                })
                OutputImagePaths.append(OutputImagePath)

            except Exception as e:
                os.remove(FilePath)
                logger.error("Error: ", e)
                return CustomResponse(error=str(e), status=status.HTTP_500_INTERNAL_SERVER_ERROR)
                                
            os.remove(FilePath)

        if os.path.exists(CustomImgPath):
            os.remove(CustomImgPath)

        if EmailAddress:
            try:
                logger.info("Start sending email...")
                Email.SendEmailWithAttachment(EmailAddress, file_paths=OutputImagePaths)
                logger.info("Email sent successfully.")
            except Exception as e:
                logger.error(f"Failed to send email: {e}")
                return CustomResponse(error="Failed to send email: " + str(e), status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            
        logger.info("File encrypted and saved. " + ('' if EmailAddress is None else "Email successfully sent. ") + 'End of processing.')

        return CustomResponse(results=Results,
                              message="File encrypted and saved, Email successfully sent." if EmailAddress is not None else "File encrypted and saved.", 
                              status=status.HTTP_200_OK
                              )

    
class DownloadView(APIView):
    def get(self, request, file_name):
        logger.info(f"Receive Get Request in Download, Start processing. Data Body: {request.data}")

        FilePath = os.path.join(settings.TRANSIT_DIR, file_name)

        if os.path.exists(FilePath):
            logger.info(f"Downloading file: {FilePath}")
            content_type, _ = mimetypes.guess_type(FilePath)
            response = FileResponse(open(FilePath, 'rb'), content_type=content_type)
            response['Content-Disposition'] = f'attachment; filename="{urllib.parse.quote(file_name)}"'
            logger.info("File downloaded successfully. End of processing.")
            return response
        else:
            logger.error(f"File not found: {FilePath}. End of processing.")
            return CustomResponse(error="File not found", status=status.HTTP_404_NOT_FOUND)


class EchoView(APIView):
    def post(self, request, *args, **kwargs):
        logger.info(f"Receive Post Request in Echo, Start processing. Data Body: {request.data}")
        InputText = request.data.get('text', None)
        if InputText is None:
            logger.error("No text provided. End of processing.")
            return Response({"error": "No text provided"}, status=status.HTTP_400_BAD_REQUEST)
        ReversedText = InputText[::-1]
        logger.info(f"Text reversed sent. End of processing.")
        return Response({"Original Text": InputText, "Reversed Text": ReversedText}, status=status.HTTP_200_OK)
    
