from django.db import models


class TelegramUser(models.Model):
    username = models.CharField(max_length=100, db_index=True, default=None)
    state = models.CharField(max_length=200, default='/')


class RemontObject(models.Model):
    name = models.CharField(max_length=100, db_index=True, verbose_name='Наименование')

    def __str__(self):
        return f"{self.name}"

    class Meta:
        verbose_name = 'Объект'
        verbose_name_plural = 'Объекты'


class Material(models.Model):
    UNIT_OF_MEASUREMENT = [
        ('шт', 'шт'),
        ('лист', 'лист'),
        ('пачка', 'пачка'),
        ('рулон', 'рулон'),
        ('мешок', 'мешок'),
        ('ведро', 'ведро'),
        ('м', 'м'),
    ]
    name = models.CharField(max_length=250, db_index=True, verbose_name='Наименование материала', unique=True)
    unit_measurement = models.CharField(max_length=100, verbose_name='Единица измерения', choices=UNIT_OF_MEASUREMENT)

    class Meta:
        verbose_name = 'Материал'
        verbose_name_plural = 'Материалы'


class WorkType(models.Model):
    name = models.CharField(max_length=250, db_index=True, verbose_name='Наименование', unique=True)
    materials = models.ManyToManyField(Material)

    class Meta:
        verbose_name = 'Вид работ'
        verbose_name_plural = 'Виды работ'
