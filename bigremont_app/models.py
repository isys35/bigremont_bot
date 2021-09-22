from django.db import models


class TelegramUser(models.Model):
    username = models.CharField(max_length=100, db_index=True, default=None, null=True, blank=True)
    state = models.CharField(max_length=200, default='/')

    def __str__(self):
        return f'{self.id} {self.username}'

    class Meta:
        verbose_name = 'Пользователь бота'
        verbose_name_plural = 'Пользователи бота'


class Recipient(models.Model):
    telegram_user = models.OneToOneField(TelegramUser, verbose_name="пользователь бота", on_delete=models.CASCADE,
                                         unique=True)

    class Meta:
        verbose_name = 'Получатель заявок'
        verbose_name_plural = 'Получатели заявок'


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

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Материал'
        verbose_name_plural = 'Материалы'


class WorkType(models.Model):
    name = models.CharField(max_length=250, db_index=True, verbose_name='Наименование', unique=True)
    materials = models.ManyToManyField(Material, verbose_name='Материалы', blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Вид работ'
        verbose_name_plural = 'Виды работ'


class Application(models.Model):
    remont_object = models.ForeignKey(RemontObject, verbose_name='Объект', on_delete=models.CASCADE)
    worktype = models.ForeignKey(WorkType, verbose_name='Вид работ', on_delete=models.CASCADE)
    date_create = models.DateTimeField(verbose_name='Время создания заявки', auto_now_add=True)
    date_of_delivery = models.DateTimeField(blank=True, null=True)
    materials = models.ManyToManyField(Material, verbose_name='Материалы', blank=True,
                                       through='ApplicationMaterial')

    def __str__(self):
        return f"Заявка {self.id}"

    class Meta:
        verbose_name = 'Заявка'
        verbose_name_plural = 'Заявки'


class ApplicationMaterial(models.Model):
    material = models.ForeignKey(Material, on_delete=models.CASCADE)
    application = models.ForeignKey(Application, on_delete=models.CASCADE)
    count = models.IntegerField(default=0)
