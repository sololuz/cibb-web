
from core.base.viewsets import ModelListCreateViewSet
from registro.models import Attend, Suscriptor
from registro.permissions import AttendPermissionSet, SuscriptorPermissionSet
from registro.serializers import AttendSerializer, SuscriptorSerializer
from rest_framework.response import Response


class AttendViewSet(ModelListCreateViewSet):
    permission_classes = [AttendPermissionSet, ]
    serializer_class = AttendSerializer
    queryset = Attend.objects.all()
    paginate_by = 25
    page_size = 25

    def list(self, request, *args, **kwargs):
        """
        Lista a los registrados
        """
        page = self.paginate_queryset(self.queryset)
        if page is not None:
            serializer = self.get_pagination_serializer(page)
        else:
            serializer = self.get_serializer(self.queryset, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        """
        Resgistra una persona
        """
        return super(AttendViewSet, self).create(request)


class SuscriptorViewSet(ModelListCreateViewSet):
    permission_classes = [SuscriptorPermissionSet, ]
    serializer_class = SuscriptorSerializer
    queryset = Suscriptor.objects.all()
    paginate_by = 25
    page_size = 25

    def list(self, request, *args, **kwargs):
        """
        Lista los suscriptores
        """
        page = self.paginate_queryset(self.queryset)
        if page is not None:
            serializer = self.get_pagination_serializer(page)
        else:
            serializer = self.get_serializer(self.queryset, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        """
        Crea un suscriptor.
        """
        return super(SuscriptorViewSet, self).create(request)