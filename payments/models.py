from django.conf import settings
from django.core.validators import MinValueValidator
from django.db import models


class Payment(models.Model):
    collect = models.ForeignKey(
        'collects.Collect',
        on_delete=models.CASCADE,
        related_name='payments',
        verbose_name='Сбор',
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name='payments',
        verbose_name='Пользователь',
    )
    amount = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        validators=[MinValueValidator(0.01)],
        verbose_name='Сумма пожертвования',
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата и время пожертвования',
    )

    class Meta:
        verbose_name = 'Пожертвование'
        verbose_name_plural = 'Пожертвования'
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.user} — {self.amount}'