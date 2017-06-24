from tempfile import NamedTemporaryFile
import pandas as pd
from django.core.exceptions import ValidationError
from django.utils.deconstruct import deconstructible
import subscriptions.core.models

@deconstructible
class FileValidator(object):
    def _save_file(self, value):
        with open(self.filepath, 'wb+') as destination:
            for chunk in value.chunks():
                destination.write(chunk)

    def __call__(self, value):
        self.filepath = NamedTemporaryFile().name
        self._save_file(value)
        extension = value.name.split('.')[-1]
        if extension == 'csv':
            self.dataset = pd.read_csv(self.filepath, sep=';', keep_default_na=False)
        elif extension in ('xlsx','xls'):
            self.dataset = pd.read_excel(self.filepath, keep_default_na=False)

        if 'Unnamed: 0' in self.dataset.columns:
            del self.dataset['Unnamed: 0']

        self._validate_columns()
        self._validate_shirt_size()
        self._validate_modalities()

    def _validate_columns(self):
        self.__validate_items(
            'column',
            subscriptions.core.models.Column.objects,
            'Colunas %(invalid_columns)s invalidas',
            self.dataset.columns,
        )

    def _validate_shirt_size(self):
        self.__validate_items(
            'shirt_size',
            subscriptions.core.models.ShirtSize.objects,
            'Tamanhos de Camiseta %(invalid_columns)s invalidos',
        )

    def _validate_modalities(self):
        self.__validate_items(
            'modality',
            subscriptions.core.models.Modality.objects,
            'Modalidades %(invalid_columns)s invalidas',
        )

    def __validate_items(self, column, queryset, message, items=[]):
        def get_invalid_items(column, queryset, items):
            if not len(items):
                items = get_items_from_column(column)
            valid_items = get_valid_items(items, column, queryset)
            return [item
                    for item in items
                    if item not in valid_items]

        def get_valid_items(items, column, queryset):
            filter = {
                'file_{}__in'.format(column): set(items) #file_column__in=set(items)
            }
            return queryset.filter(**filter)\
                           .values_list('file_{}'.format(column), flat=True)

        def get_items_from_column(column):
            column_possible_names = subscriptions.core.models.\
                    Column.objects.filter(subscription_name__exact=column).\
                    values_list('file_column', flat=True)
            columns_intersection = set(column_possible_names).intersection(self.dataset.columns)
            if columns_intersection:
                column = list(columns_intersection)[0]
                return self.dataset[column]
            else:
                return []

        invalid_items = get_invalid_items(column, queryset, items)

        if invalid_items:
            raise ValidationError(
                message,
                code=column,
                params={'invalid_columns': set(invalid_items)}
            )

    def __eq__(self, other):
        return isinstance(other, FileValidator)

validate_file = FileValidator()
