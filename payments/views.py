from rest_framework import viewsets
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from .models import Payment
from .permissions import IsPaymentOwnerOrReadOnly
from .serializers import PaymentSerializer


class PaymentViewSet(viewsets.ModelViewSet):
    serializer_class = PaymentSerializer
    permission_classes = [
        IsAuthenticatedOrReadOnly,
        IsPaymentOwnerOrReadOnly,
    ]

    def get_queryset(self):
        queryset = Payment.objects.select_related('user', 'collect')

        collect_id = self.request.query_params.get('collect')
        if collect_id:
            queryset = queryset.filter(collect_id=collect_id)

        return queryset

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def perform_update(self, serializer):
        if serializer.instance.user != self.request.user:
            raise PermissionDenied(
                'Вы можете изменять только собственные пожертвования.'
            )

        serializer.save()