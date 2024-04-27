from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse
from django.utils import timezone


class DescriptionType(models.Model):
    date = models.DateField('Срок свидетельства', null=True, blank=True)
    link =  models.CharField('Ссылка', max_length=500, null=True, blank=True)
    number = models.SlugField('Номер в госреестре', max_length=10, null=False, blank=False)
    producer = models.CharField('Изготовитель', max_length=500, null=True, blank=True)

    class Meta:
        db_table = 'Описание типа'  # название таблицы в БД
        ordering = ['number']
        verbose_name = 'Описание типа'
        verbose_name_plural = 'Описания типа'

    def __str__(self):
        return self.number

class Etalon(models.Model):
    code = models.CharField('Шифр', max_length=50, null=False, blank=True)
    name = models.CharField('Наименование', max_length=1000, null=False, blank=True)

    class Meta:
        db_table = 'Эталоны'  # название таблицы в БД
        ordering = ['code']  # сортировка
        verbose_name = 'Эталон'
        verbose_name_plural = 'Эталоны'

    
    def __str__(self):
        return self.code

class Modification(models.Model):
    modif = models.CharField('Модификация', max_length=500, null=False, blank=True)

    class Meta:
        db_table = 'Модификации'  # название таблицы в БД
        ordering = ['modif']
        verbose_name = 'Модификация'
        verbose_name_plural = 'Модификации'
    
    def __str__(self):
        return self.modif

class Methodika(models.Model):
    method = models.CharField('Методика поверки', max_length=500, null=False, blank=False)

    class Meta:
        db_table = 'Методики поверки'  # название таблицы в БД
        ordering = ['method']
        verbose_name = 'Методика поверки'
        verbose_name_plural = 'Методики поверки'

    def __str__(self):
        return self.method
    
class Name(models.Model):
    name = models.CharField('Наименование СИ', max_length=500, null=False, blank=False)

    class Meta:
        db_table = 'Наименование СИ'  # название таблицы в БД
        ordering = ['name']
        verbose_name = 'Наименование СИ'
        verbose_name_plural = 'Наименования СИ'

    def __str__(self):
        return self.name

class Owner(models.Model):
    owner = models.CharField('Владелец, ИНН', max_length=100, null=False, blank=False)

    class Meta:
        verbose_name = 'Владелец'
        verbose_name_plural = 'Владельцы'
        ordering = ['owner']
        db_table = 'Владельцы СИ'  # название таблицы в БД
    
    def __str__(self):
        return self.owner

class Pover(models.Model):
    povername = models.CharField('Поверитель', max_length=100, null=False, blank=False)

    def __str__(self):
        return self.povername

    class Meta:
        db_table = 'Поверители'  # название таблицы в БД
        ordering = ['povername']
        verbose_name = 'Поверитель'
        verbose_name_plural = 'Поверители'

class Places(models.Model):
    place = models.CharField('Место проведения', max_length=100, null=False, blank=False)

    class Meta:
        db_table = 'Места проведения поверки'
        ordering = ['place']
        verbose_name = 'Место проведения'
        verbose_name_plural = 'Места проведения'
    
    def __str__(self):
        return self.place

class User(models.Model):
    username = models.CharField('Исполнитель', max_length=100, null=False, blank=False)

    class Meta:
        verbose_name = 'Исполнитель'
        verbose_name_plural = 'Исполнители'
        ordering = ['username']
        db_table = 'Исполнители'  # название таблицы в БД
    
    def __str__(self):
        return self.username


class Register(models.Model):
    date = models.DateField('Дата поверки', null=False, blank=False)
    descr = models.ForeignKey(DescriptionType, on_delete=models.PROTECT, verbose_name="Описание типа",
                              help_text='выберите описание типа', null=False, blank=False)
    id_numb = models.SlugField('Номер протокола', max_length=10, db_index=True, null=True, blank=True)

    modif = models.ForeignKey(Modification, on_delete=models.PROTECT, verbose_name="Модификация",
                              help_text='выберите модификацию', blank=True, null=True)

    method = models.ForeignKey(Methodika, on_delete=models.PROTECT, verbose_name="Методика поверки",
                                   help_text='выберите методику поверки', blank=True, null=True)
    mpi = models.CharField(max_length=10, choices=(
        ('1 год', '1'),
        ('2 года', '2'),
        ('3 года', '3'),
        ('4 года', '4'),
        ('5 лет', '5'),
        ('6 лет', '6'),
    ), verbose_name='Межповерочный интервал', null=True, blank=True)
    name = models.ForeignKey(Name, on_delete=models.PROTECT, verbose_name="Наименование средства измерений", blank=True,
                             null=True)
    owner = models.ForeignKey(Owner, on_delete=models.PROTECT, related_name="+", verbose_name="Владелец СИ, ИНН",
                              default=None, blank=True, null=True)
    place = models.ForeignKey(Places, on_delete=models.PROTECT, verbose_name="Место проведения поверки", 
                          default=None, blank=True, null=True)

    povername = models.ForeignKey(Pover, on_delete=models.PROTECT, verbose_name="Поверитель", blank=True, null=True)
    until = models.DateField('Действительно до', blank=True, null=True)
    number = models.CharField('Заводской номер', max_length=50, blank=True, null=True)
    etalons = models.ManyToManyField(Etalon, related_name='etalons', blank=True)

    temp_val = models.DecimalField('Температура', default=22.0, max_digits=3, decimal_places=1, null=True, blank=True)

    class TempKind(models.TextChoices):
        cel = '°С', '°С'
        kel = 'К', 'К'
        # __empty__='выберите'

    temp_kind = models.CharField('Ед.изм. температуры', max_length=100, choices=TempKind.choices,
                                 default=TempKind.cel,
                                 blank=True, null=True)
    temp_t = ('temp_cal', 'temp_kind')
    press_val = models.DecimalField('Давление', default=101.2, max_digits=4, decimal_places=1, blank=True, null=True)

    class PresKind(models.TextChoices):
        kpa = 'кПа', 'кПа'
        mmrs = 'мм.рт.ст.', 'мм.рт.ст.'
        # __empty__='выберите'

    press_kind = models.CharField('Ед.изм. давления', max_length=10, choices=PresKind.choices, default=PresKind.kpa,
                                  blank=True, null=True)
    hum_val = models.DecimalField('Влажность', default=45.0, max_digits=3, decimal_places=1, blank=True)
    hum_kind = models.CharField('Ед.изм. влажности', max_length=10, default='%', blank=True, null=True)
    others = models.CharField('Другие условия поверки', max_length=100, blank=True, null=True)
    d_min = models.CharField('Нижний диапазон', max_length=100, null=True, blank=True)
    d_max = models.CharField('Верхний диапазон', max_length=100, null=True, blank=True)

    class EdIzmKind(models.TextChoices):
        kpa = 'кПа', 'кПа'
        mpa = 'МПа', 'МПа'
        bar = 'бар', 'бар'
        milibar = 'мбар', 'мбар'
        cel = '°С', '°С'
        nkpr = '% НКПР', '% НКПР'
        mamp = 'мА', 'мА'
        volt = 'В', 'В'
        mm = 'мм', 'мм'
        kgs = 'кгс/см²', 'кгс/см²'
        mgm = 'мг/м³', 'мг/м³'
        vol = '% об. д.', '% об. д.'
        ppm = 'ppm', 'ppm'
        __empty__ = 'выберите единицы измерения'

    ed_izm = models.CharField('Единицы измерения', max_length=100, choices=EdIzmKind.choices, null=True, blank=True)
    other_range = models.CharField('Другой диапазон', max_length=100, null=True, blank=True)
    pogr_val = models.CharField('Погрешность', max_length=100, blank=True, null=True)

    class PogrKind(models.TextChoices):
        abs = 'абсолютная', 'абсолютная'
        otn = 'относительная', 'относительная'
        priv = 'приведённая', 'приведённая'

    pogr_kind = models.CharField('Единицы измерения погрешности', max_length=100, choices=PogrKind.choices,
                                 blank=True, null=True)

    impl_name = models.ForeignKey(User, on_delete=models.PROTECT, verbose_name="Исполнитель", blank=True,
                                  null=True)
    publish = models.DateTimeField('Создано', default=timezone.now)
    created_at = models.DateTimeField("Создано auto now add", auto_now_add=True)
    updated = models.DateTimeField('Изменено', auto_now=True)

    class Status(models.TextChoices):
        DRAFT = 'Не загружено в АРШИН', 'Не загружено в АРШИН'
        PUBLISHED = 'Загружено в АРШИН', 'Загружено в АРШИН'

    status = models.CharField(max_length=30, choices=Status.choices, default=Status.DRAFT, blank=True, null=True)
    author = models.ForeignKey(User, on_delete=models.PROTECT, related_name='reestr_posts', blank=True, null=True)
    objects = models.Manager()  # менеджер, применяемый по умолчанию
    
    class Kinds(models.TextChoices):
        perv = 'первичная', 'первичная'
        period = 'периодическая', 'периодическая'
        __empty__='выберите'
    kind = models.CharField(max_length=50, choices=Kinds.choices, default=Kinds.period, verbose_name='Вид поверки', blank=True, null=True)


    class Meta:
        verbose_name = 'Реестр'
        verbose_name_plural = 'Реестр'
        ordering = ['-updated']
        indexes = [
            models.Index(fields=['id_numb']),
            models.Index(fields=['descr']),
            models.Index(fields=['number']),
            models.Index(fields=['date']),
            models.Index(fields=['modif']),
        ]

    def __str__(self):
        return self.id_numb

    def get_category(self): return ", ".join([str(p) for p in self.etalons.all()])
