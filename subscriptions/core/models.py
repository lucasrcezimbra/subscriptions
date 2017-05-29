import os
import pandas as pd
from datetime import datetime
from django.db import models
from subscriptions.core.validators import validate_file


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
    file = models.FileField(validators=[validate_file])

    def __str__(self):
        return str(self.pk)

    def save(self, *args, **kwargs):
        super(Import, self).save(*args, **kwargs)
        self._import()

    def _import(self):
        csv = pd.DataFrame.from_csv(self.file.name, sep=';')
        self._create_subscriptions(csv)

    def _file_column(self, subscription_name):
        column_filter = self._columns.filter(
            subscription_name__exact=subscription_name
        )
        return column_filter[0].file_name

    def _file_columns(self):
        return {
            'name':self._file_column('name'),
            'email':self._file_column('email'),
            'name_for_bib_number':self._file_column('name_for_bib_number'),
            'gender':self._file_column('gender'),
            'date_of_birth':self._file_column('date_of_birth'),
            'city':self._file_column('city'),
            'team':self._file_column('team'),
            'shirt_size':self._file_column('shirt_size'),
            'modality':self._file_column('modality'),
        }

    def _create_subscriptions(self, csv):
        self._columns = Column.objects.filter(file_name__in=set(csv.columns))
        records = csv.to_dict('records')
        file_columns = self._file_columns()
        model_instances = [self._new_subscription(record, file_columns)
                           for record in records]

        Subscription.objects.bulk_create(model_instances)

    def _new_subscription(self, record, file_columns):
        return Subscription(
            name=record[file_columns['name']],
            email=record[file_columns['email']],
            name_for_bib_number=record[file_columns['name_for_bib_number']],
            gender=record[file_columns['gender']],
            date_of_birth=datetime.strptime(
                record[file_columns['date_of_birth']],
                '%d/%m/%Y').date(),
            city=record[file_columns['city']],
            team=record[file_columns['team']],
            shirt_size=record[file_columns['shirt_size']],
            modality=record[file_columns['modality']],
            import_t=self,
        )


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
