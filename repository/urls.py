from django.urls import path
from repository.views import RecordDetail, RecordList, CollectionList, RecordMapList, RecordListAll, RecordExport

app_name = 'repository'

urlpatterns = [
    path('records/', RecordList.as_view(), name='record-list'),
    path('records_all/', RecordListAll.as_view(), name='record-list-all'),
    path('records_map/', RecordMapList.as_view(), name='record-map-list'),
    path('records/<int:pk>/', RecordDetail.as_view(), name='record-detail'),
    path('collections/', CollectionList.as_view(), name='collection-list'),

    path('export/<int:collection_id>', RecordExport.as_view(), name='record-export')
]