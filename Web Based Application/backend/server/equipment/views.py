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


from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
from reportlab.lib.units import inch
from datetime import datetime

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def generate_report(request):
    """
    Generates a PDF report using ReportLab Platypus.
    Input: Optional 'dataset_id' in POST data. Default: Latest dataset.
    """
    dataset_id = request.data.get('dataset_id')

    if dataset_id:
        try:
            dataset = Dataset.objects.get(id=dataset_id)
        except Dataset.DoesNotExist:
            return Response({"error": "Dataset not found"}, status=404)
    else:
        # Default to latest
        dataset = Dataset.objects.order_by('-uploaded_at').first()
        if not dataset:
            return Response({"error": "No datasets available"}, status=404)

    # Buffer for PDF
    buffer = BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=72, leftMargin=72,
        topMargin=72, bottomMargin=18
    )

    story = []
    styles = getSampleStyleSheet()
    
    # 1. Title Section
    title_style = styles['Title']
    story.append(Paragraph("Chemical Equipment Analysis Report", title_style))
    story.append(Spacer(1, 12))

    # Date & Metadata
    normal_style = styles['Normal']
    date_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    story.append(Paragraph(f"<b>Generated on:</b> {date_str}", normal_style))
    story.append(Paragraph(f"<b>Dataset ID:</b> {dataset.id}", normal_style))
    story.append(Paragraph(f"<b>File Name:</b> {dataset.file_name}", normal_style))
    story.append(Spacer(1, 24))

    # 2. Summary Section
    story.append(Paragraph("Summary Statistics", styles['Heading2']))
    story.append(Spacer(1, 12))
    
    summ = dataset.summary
    # Safe access with defaults
    total = summ.get('total_equipment', 0)
    avg_flow = summ.get('average_flowrate', 0)
    avg_press = summ.get('average_pressure', 0)
    avg_temp = summ.get('average_temperature', 0)

    summary_data = [
        ["Metric", "Value"],
        ["Total Equipment", str(total)],
        ["Average Flowrate", f"{avg_flow:.2f} L/min"],
        ["Average Pressure", f"{avg_press:.2f} bar"],
        ["Average Temperature", f"{avg_temp:.2f} °C"]
    ]

    t_summ = Table(summary_data, colWidths=[200, 200])
    t_summ.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ]))
    story.append(t_summ)
    story.append(Spacer(1, 24))

    # 3. Equipment Type Distribution
    story.append(Paragraph("Equipment Type Distribution", styles['Heading2']))
    story.append(Spacer(1, 12))

    type_dist = summ.get('type_distribution', {})
    if type_dist:
        dist_data = [["Equipment Type", "Count"]]
        for k, v in type_dist.items():
            dist_data.append([str(k), str(v)])
        
        t_dist = Table(dist_data, colWidths=[200, 100])
        t_dist.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (1, 0), colors.darkblue),
            ('TEXTCOLOR', (0, 0), (1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (1, 0), 'Helvetica-Bold'),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ]))
        story.append(t_dist)
    else:
        story.append(Paragraph("No distribution data available.", normal_style))

    # Build PDF
    doc.build(story)

    # Return response
    buffer.seek(0)
    response = HttpResponse(buffer, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="equipment_report_{dataset.id}.pdf"'
    return response