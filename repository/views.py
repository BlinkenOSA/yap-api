from rest_framework import generics
from repository.models import Record
from repository.serializers import RecordSerializer


class RecordDetail(generics.RetrieveAPIView):
    queryset = Record.objects.all()
    serializer_class = RecordSerializer
