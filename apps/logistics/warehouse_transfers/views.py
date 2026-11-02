from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework import status
from apps.logistics.warehouse_transfers.models import WarehouseTransferProfile[cite: 1]

class FieldInspectionUploadView(APIView):
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request, transfer_id):
        try:
            transfer = WarehouseTransferProfile.objects.get(id=transfer_id)
            unboxing_image = request.FILES.get('unboxing_image')
            qa_report_image = request.FILES.get('qa_report_image')
            remarks = request.data.get('remarks', '')

            if unboxing_image:
                transfer.unboxing_image = unboxing_image
            if qa_report_image:
                transfer.qa_report_image = qa_report_image
            
            transfer.remarks = remarks
            transfer.is_inspected = True
            transfer.save()

            return Response({"message": "களப்பணி தணிக்கை படங்கள் வெற்றிகரமாகப் பதிவேற்றப்பட்டன."}, status=status.HTTP_200_OK)
        except WarehouseTransferProfile.DoesNotExist:
            return Response({"error": "பரிமாற்ற விவரம் கிடைக்கவில்லை"}, status=status.HTTP_404_NOT_FOUND)