from django.urls import path
from repository.views import RecordDetail, RecordList

app_name = 'repository'

urlpatterns = [
    path('records/', RecordList.as_view(), name='record-list'),
    path('records/<int:pk>/', RecordDetail.as_view(), name='record-detail'),
]