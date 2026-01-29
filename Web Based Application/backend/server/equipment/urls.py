from django.urls import path
from .views import (
    generate_pdf,
    health_check,
    upload_csv,
    dataset_summary,
    dataset_history
)

urlpatterns = [
    path('health/', health_check),
    path('upload/', upload_csv),
    path('summary/<int:dataset_id>/', dataset_summary),
    path('history/', dataset_history),
    path('report/<int:dataset_id>/', generate_pdf),
]