from django.urls import path
from repository.views import RecordDetail

app_name = 'repository'

urlpatterns = [
    path('records/<int:pk>/', RecordDetail.as_view(), name='record-detail'),
]