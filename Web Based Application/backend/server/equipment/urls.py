from django.urls import path
from .views import (
    generate_pdf,
    health_check,
    upload_csv,
    dataset_summary,
    dataset_history,
    generate_report,
    register_user
)

urlpatterns = [
    path('health/', health_check),
    path('register/', register_user),
    path('upload/', upload_csv),
    path('summary/<int:dataset_id>/', dataset_summary),
    path('history/', dataset_history),
    path('report/<int:dataset_id>/', generate_pdf),
    path('generate-report/', generate_report),
]