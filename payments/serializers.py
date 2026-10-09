from django.utils import timezone
from rest_framework import serializers

from collects.models import Collect
from .models import Payment


class PaymentSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Payment
        fields = [
            'id',
            'collect',
            'user',
            'amount',
            'created_at',
        ]
        read_only_fields = ['id', 'user', 'created_at']

    def validate_amount(self, value):
        if value <= 0:
            raise serializers.ValidationError(
                'Сумма пожертвования должна быть больше нуля.'
            )
        return value

    def validate(self, attrs):
        collect = attrs.get(
            'collect',
            getattr(self.instance, 'collect', None),
        )

        if collect is None:
            raise serializers.ValidationError(
                {'collect': 'Необходимо указать сбор.'}
            )

        if collect.end_at and collect.end_at <= timezone.now():
            raise serializers.ValidationError(
                {'collect': 'Срок этого сбора уже завершён.'}
            )

        if self.instance and (
            collect != self.instance.collect
            or attrs.get('amount', self.instance.amount)
            != self.instance.amount
        ):
            raise serializers.ValidationError(
                'Нельзя изменять сумму или сбор существующего пожертвования.'
            )

        return attrs