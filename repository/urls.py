from django.urls import path
from repository.views import RecordDetail, RecordList, CollectionList, RecordMapList, \
    RecordMapListFirst, RecordMapListSecond

app_name = 'repository'

urlpatterns = [
    path('records/', RecordList.as_view(), name='record-list'),
    path('records_map/', RecordMapList.as_view(), name='record-map-list'),
    path('records_map_01/', RecordMapListFirst.as_view(), name='record-map-list-first'),
    path('records_map_02/', RecordMapListSecond.as_view(), name='record-map-list-second'),
    path('records/<int:pk>/', RecordDetail.as_view(), name='record-detail'),
    path('collections/', CollectionList.as_view(), name='collection-list'),
]