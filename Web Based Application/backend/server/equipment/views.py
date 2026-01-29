import pandas as pd
from .models import Dataset
from io import BytesIO
from rest_framework.decorators import api_view, parser_classes
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import permission_classes
from reportlab.pdfgen import canvas
from django.http import HttpResponse
from reportlab.lib.pagesizes import A4

@api_view(['GET'])
def health_check(request):
    return Response({"status": "Backend is running"})

@api_view(['POST'])
@permission_classes([IsAuthenticated])
@parser_classes([MultiPartParser, FormParser])
def upload_csv(request):
    file = request.FILES.get('file')

    if not file:
        return Response({"error": "No file received"}, status=400)

    df = pd.read_csv(file)

    required_columns = {
        "Equipment Name",
        "Type",
        "Flowrate",
        "Pressure",
        "Temperature"
    }

    if not required_columns.issubset(df.columns):
        return Response({"error": "Invalid CSV format"}, status=400)

    summary = {
        "total_equipment": len(df),
        "average_flowrate": df["Flowrate"].mean(),
        "average_pressure": df["Pressure"].mean(),
        "average_temperature": df["Temperature"].mean(),
        "type_distribution": df["Type"].value_counts().to_dict()
    }

    dataset = Dataset.objects.create(
        file_name=file.name,
        summary=summary
    )

    if Dataset.objects.count() > 5:
        Dataset.objects.order_by('uploaded_at').first().delete()

    return Response({
        "dataset_id": dataset.id,
        "summary": summary
    })

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def dataset_summary(request, dataset_id):
    try:
        dataset = Dataset.objects.get(id=dataset_id)
    except Dataset.DoesNotExist:
        return Response({"error": "Dataset not found"}, status=404)

    return Response({
        "file_name": dataset.file_name,
        "uploaded_at": dataset.uploaded_at,
        "summary": dataset.summary
    })

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def dataset_history(request):
    datasets = Dataset.objects.order_by('-uploaded_at')[:5]

    history = [
        {
            "id": d.id,
            "file_name": d.file_name,
            "uploaded_at": d.uploaded_at
        }
        for d in datasets
    ]

    return Response(history)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def generate_pdf(request, dataset_id):
    try:
        dataset = Dataset.objects.get(id=dataset_id)
    except Dataset.DoesNotExist:
        return Response({"error": "Dataset not found"}, status=404)

    # 🔑 IMPORTANT: use buffer
    buffer = BytesIO()

    p = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4

    # Title
    p.setFont("Helvetica-Bold", 16)
    p.drawString(50, height - 50, "Chemical Equipment Dataset Report")

    # Metadata
    p.setFont("Helvetica", 12)
    p.drawString(50, height - 90, f"File Name: {dataset.file_name}")
    p.drawString(50, height - 110, f"Dataset ID: {dataset.id}")

    # Summary
    y = height - 160
    p.setFont("Helvetica-Bold", 14)
    p.drawString(50, y, "Summary")
    y -= 30

    p.setFont("Helvetica", 12)

    summary = dataset.summary  # JSONField / dict

    for key, value in summary.items():
        p.drawString(60, y, f"{key}: {value}")
        y -= 20

        if y < 50:
            p.showPage()
            p.setFont("Helvetica", 12)
            y = height - 50

    # Finalize PDF
    p.showPage()
    p.save()

    # Write buffer to response
    buffer.seek(0)
    response = HttpResponse(buffer, content_type="application/pdf")
    response["Content-Disposition"] = f'attachment; filename="report_{dataset_id}.pdf"'

    return response