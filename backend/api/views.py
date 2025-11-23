from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.status import *
from rest_framework.permissions import IsAuthenticated
from .models import Dataset
from .csv_handler import validate_and_parse_csv
import json

@api_view(["POST"])
@permission_classes([IsAuthenticated])
def upload_csv(request):
    file = request.FILES.get("file")
    if not file:
        return Response({"error": "File required"}, status=400)

    try:
        df, summary = validate_and_parse_csv(file)
    except Exception as e:
        return Response({"error": str(e)}, status=400)

    # Save last 5 datasets
    Dataset.objects.create(
        user=request.user,
        file_name=file.name,
        summary=summary,
    )

    # Limit history to last 5
    datasets = Dataset.objects.filter(user=request.user).order_by('-uploaded_at')
    if datasets.count() > 5:
        for old in datasets[5:]:
            old.delete()

    return Response(summary)
    

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def history(request):
    datasets = Dataset.objects.filter(user=request.user)
    return Response([
        {
            "file": d.file_name,
            "uploaded_at": d.uploaded_at,
            "summary": d.summary
        } for d in datasets
    ])
