from django.conf import settings
from django.core.validators import MinValueValidator
from django.db import models
from django.db.models import Sum
from django.db.models.signals import post_delete
from django.dispatch import receiver


class Collect(models.Model):
    class Occasion(models.TextChoices):
        BIRTHDAY = 'birthday', 'День рождения'
        WEDDING = 'wedding', 'Свадьба'
        CHARITY = 'charity', 'Благотворительность'
        GIFT = 'gift', 'Подарок'
        OTHER = 'other', 'Другое'

    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='collects',
        verbose_name='Автор',
    )
    title = models.CharField(
        max_length=200,
        verbose_name='Название',
    )
    occasion = models.CharField(
        max_length=20,
        choices=Occasion.choices,
        default=Occasion.OTHER,
        verbose_name='Повод',
    )
    description = models.TextField(
        verbose_name='Описание',
    )
    target_amount = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        null=True,
        blank=True,
        validators=[MinValueValidator(0.01)],
        verbose_name='Целевая сумма',
        help_text='Оставьте пустым для сбора без ограничения суммы.',
    )
    cover = models.ImageField(
        upload_to='collects/covers/',
        null=True,
        blank=True,
        verbose_name='Обложка',
    )
    end_at = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name='Дата и время завершения',
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата создания',
    )

    class Meta:
        verbose_name = 'Сбор'
        verbose_name_plural = 'Сборы'
        ordering = ['-created_at']

    def __str__(self):
        return self.title

    @property
    def collected_amount(self):
        result = self.payments.aggregate(
            total=Sum('amount')
        )['total']
        return result or 0


@receiver(post_delete, sender=Collect)
def delete_collect_cover(sender, instance, **kwargs):
    if instance.cover:
        instance.cover.delete(save=False)