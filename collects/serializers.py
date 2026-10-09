from rest_framework import serializers

from .models import Collect


class CollectSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField(read_only=True)
    collected_amount = serializers.DecimalField(
        max_digits=12,
        decimal_places=2,
        read_only=True,
    )

    class Meta:
        model = Collect
        fields = [
            'id',
            'author',
            'title',
            'occasion',
            'description',
            'target_amount',
            'collected_amount',
            'cover',
            'end_at',
            'created_at',
        ]
        read_only_fields = ['id', 'author', 'collected_amount', 'created_at']

    def validate_end_at(self, value):
        from django.utils import timezone

        if value is not None and value <= timezone.now():
            raise serializers.ValidationError(
                'Дата завершения должна быть в будущем.'
            )
        return value