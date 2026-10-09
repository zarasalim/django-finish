from django.db.models import Prefetch
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response

from payments.models import Payment
from payments.serializers import PaymentSerializer
from .models import Collect
from .permissions import IsAuthorOrReadOnly
from .serializers import CollectSerializer


class CollectViewSet(viewsets.ModelViewSet):
    serializer_class = CollectSerializer
    permission_classes = [
        IsAuthenticatedOrReadOnly,
        IsAuthorOrReadOnly,
    ]

    def get_queryset(self):
        return Collect.objects.select_related('author').prefetch_related(
            Prefetch(
                'payments',
                queryset=Payment.objects.select_related('user').order_by(
                    '-created_at'
                ),
            )
        )

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    @action(detail=True, methods=['get'], url_path='payments')
    def payments(self, request, pk=None):
        collect = self.get_object()
        payments = collect.payments.select_related('user').all()

        page = self.paginate_queryset(payments)
        if page is not None:
            serializer = PaymentSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = PaymentSerializer(payments, many=True)
        return Response(serializer.data)