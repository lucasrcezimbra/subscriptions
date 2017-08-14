import os
from datetime import datetime

import pandas as pd
from django.core.exceptions import ValidationError
from django.db import models

from subscriptions.core.validators import validate_file


SHIRT_SIZES = (
    ('BL', 'Baby Look'),
    ('P', 'P'),
    ('M', 'M'),
    ('G', 'G'),
    ('GG', 'GG'),
    ('2', 'Infantil 2'),
    ('4', 'Infantil 4'),
    ('6', 'Infantil 6'),
    ('8', 'Infantil 8'),
    ('10', 'Infantil 10'),
    ('12', 'Infantil 12'),
    ('14', 'Infantil 14'),
    ('SEM', 'Sem Camiseta'),
    ('VAZIO', 'VAZIO')
)

MODALITIES = (
    ('1', '1km'),
    ('2', '2km'),
    ('3', '3km'),
    ('4', '4km'),
    ('5', '5km'),
    ('6', '6km'),
    ('7', '7km'),
    ('8', '8km'),
    ('9', '9km'),
    ('10', '10km'),
    ('I', 'Infantil'),
    ('J', 'Juvenil'),
    ('C', 'Caminhada'),
    ('K', 'Kangoo'),
)

class Subscription(models.Model):
    GENDERS = (
        ('F', 'Feminino'),
        ('M', 'Masculino'),
    )

    name = models.CharField('nome', max_length=200)
    email = models.EmailField('e-mail', blank=True)
    name_for_bib_number = models.CharField('nome para número de peito',
                                           max_length=200, blank=True)
    gender = models.CharField('sexo', max_length=1, choices=GENDERS)
    date_of_birth = models.DateField('data de nascimento')
    city = models.CharField('cidade', max_length=100, blank=True)
    team = models.CharField('equipe', max_length=100, blank=True)
    modality = models.CharField('modalidade', max_length=2, choices=MODALITIES)
    shirt_size = models.CharField('tamanho da camiseta',
                                  max_length=5, choices=SHIRT_SIZES, blank=True)
    import_t = models.ForeignKey('Import',
                                 on_delete=models.CASCADE, null=True, blank=True)

    def save(self, *args, **kwargs):
        self.full_clean()
        super(Subscription, self).save(*args, **kwargs)

    def __str__(self):
        return str(self.name)


class Import(models.Model):
    origin = models.CharField('origem',max_length=100)
    file = models.FileField(validators=[validate_file])
    date_format = models.CharField('formato da data', max_length=15, blank=True, null=True, default='%d/%m/%Y')

    def __str__(self):
        return str(self.origin)

    def save(self, *args, **kwargs):
        super(Import, self).save(*args, **kwargs)
        self._import()

    def _import(self):
        extension = self.file.name.split('.')[-1]
        if extension == 'csv':
            dataset = pd.read_csv(self.file.name, sep=';', keep_default_na=False)
        elif extension in ('xls', 'xlsx'):
            dataset = pd.read_excel(self.file.name, keep_default_na=False)

        self._create_subscriptions(dataset)

    def _file_column(self, subscription_name):
        column_filter = self._columns.filter(
            subscription_name__exact=subscription_name
        )
        return column_filter[0].file_column

    def _file_columns(self):
        columns = self._columns.exclude(subscription_name__exact='ignore')\
                               .values_list('subscription_name', flat=True)
        return { column:self._file_column(column) for column in columns }

    def _create_subscriptions(self, dataset):
        instances = self._new_subscriptions(dataset)
        Subscription.objects.bulk_create(instances)

    def _new_subscriptions(self, dataset):
        self._columns = Column.objects.filter(file_column__in=set(dataset.columns))
        records = dataset.to_dict('records')
        file_columns = self._file_columns()
        instances = [self._new_subscription(record, file_columns)
                     for record in records]
        return instances

    def _new_subscription(self, record, file_columns):
        params = {column:record[file_columns[column]] for column in file_columns}
        if params.get('modality'):
            params['modality'] = Modality.objects.get(
                file_modality__exact=record[file_columns['modality']]
            )
        if params.get('shirt_size'):
            params['shirt_size'] = ShirtSize.objects.get(
                file_shirt_size__exact=record[file_columns['shirt_size']]
            )
        if type(params['date_of_birth']) == str:
            params['date_of_birth'] = datetime.strptime(
                params['date_of_birth'].strip(), self.date_format
            ).date()
        params['import_t'] = self

        subscription = Subscription(**params)
        subscription.full_clean()
        return subscription


class Column(models.Model):
    COLUMNS = (
        ('name', 'name'),
        ('email', 'email'),
        ('name_for_bib_number', 'name_for_bib_number'),
        ('gender', 'gender'),
        ('date_of_birth', 'date_of_birth'),
        ('city', 'city'),
        ('team', 'team'),
        ('shirt_size', 'shirt_size'),
        ('modality', 'modality'),
        ('ignore', 'ignore')
    )

    subscription_name = models.CharField('coluna', max_length=20, choices=COLUMNS)
    file_column = models.CharField(max_length=100, primary_key=True)

    def save(self, *args, **kwargs):
        self.full_clean()
        super(Column, self).save(*args, **kwargs)

    def __str__(self):
        return str(self.file_column)


class ShirtSize(models.Model):
    shirt_size = models.CharField('camiseta', max_length=10, choices=SHIRT_SIZES)
    file_shirt_size = models.CharField(max_length=100, primary_key=True)

    def save(self, *args, **kwargs):
        self.full_clean()
        super(ShirtSize, self).save(*args, **kwargs)

    def __str__(self):
        return str(self.shirt_size)

    def __eq__(self, other):
        return other == self.shirt_size


class Modality(models.Model):
    modality = models.CharField('modalidade', max_length=2, choices=MODALITIES)
    file_modality = models.CharField(max_length=100)

    def save(self, *args, **kwargs):
        self.full_clean()
        super(Modality, self).save(*args, **kwargs)

    def __str__(self):
        return str(self.modality)
