import os
import pandas as pd
from datetime import datetime
from django.db import models
from subscriptions.core.validators import ValidateFile


class Subscription(models.Model):
    GENDERS = (
        ('F', 'Feminino'),
        ('M', 'Masculino'),
    )

    name = models.CharField('nome', max_length=200)
    email = models.EmailField('e-mail')
    name_for_bib_number = models.CharField('nome para número de peito',
                                           max_length=200, blank=True)
    gender = models.CharField('sexo', max_length=1, choices=GENDERS)
    date_of_birth = models.DateField('data de nascimento')
    city = models.CharField('cidade', max_length=100, blank=True)
    team = models.CharField('equipe', max_length=100, blank=True)
    shirt_size = models.CharField('tamanho da camiseta', max_length=25)
    modality = models.CharField('modalidade', max_length=25)
    import_t = models.ForeignKey('Import', on_delete=models.CASCADE, null=True)


class Import(models.Model):
    origin=models.CharField('origem',max_length=100)
    file = models.FileField(validators=[ValidateFile.columns])

    def __str__(self):
        return str(self.pk)

    def save(self, *args, **kwargs):
        super(Import, self).save(*args, **kwargs)
        self._import()

    def _import(self):
        csv = pd.DataFrame.from_csv(self.file.name, sep=';')
        columns = Column.objects.filter(file_name__in=set(csv.columns))
        records = csv.to_dict('records')
        model_instances = [Subscription(
            name=record[self._columns_names(columns, 'name')],
            email=record[self._columns_names(columns, 'email')],
            name_for_bib_number=record[self._columns_names(columns, 'name_for_bib_number')],
            gender=record[self._columns_names(columns, 'gender')],
            date_of_birth=datetime.strptime(
                record[self._columns_names(columns, 'date_of_birth')],
                '%d/%m/%Y').date(),
            city=record[self._columns_names(columns, 'city')],
            team=record[self._columns_names(columns, 'team')],
            shirt_size=record[self._columns_names(columns, 'shirt_size')],
            modality=record[self._columns_names(columns, 'modality')],
            import_t=self,
        ) for record in records]

        Subscription.objects.bulk_create(model_instances)

    def _columns_names(self, columns, subscription_name):
        return columns.filter(subscription_name__exact=subscription_name)[0].file_name


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

    subscription_name = models.CharField('coluna', max_length=20,
                                   choices=COLUMNS, default='')
    file_name = models.CharField(max_length=100, primary_key=True)

    def save(self, *args, **kwargs):
        self.full_clean()
        super(Column, self).save(*args, **kwargs)

    def __str__(self):
        return str(self.file_name)
