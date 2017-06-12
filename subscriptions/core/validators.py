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
            dataset = pd.read_csv(self.filepath, sep=';', keep_default_na=False)
        elif extension in ('xlsx','xls'):
            dataset = pd.read_excel(self.filepath, keep_default_na=False)

        if 'Unnamed: 0' in dataset.columns:
            del dataset['Unnamed: 0']

        self._validate_columns(dataset)
        self._validate_shirt_size(dataset)

    def _validate_columns(self, dataset):
        message = 'Colunas %(invalid_columns)s invalidas'
        valid_columns = subscriptions.core.models.\
                Column.objects.filter(file_name__in=set(dataset.columns))\
                .values_list('file_name', flat=True)
        invalid_columns = self._invalid_items(dataset.columns, valid_columns)

        if invalid_columns:
            raise ValidationError(
                message,
                code='columns',
                params={'invalid_columns': invalid_columns}
            )

    def _invalid_items(self, items_for_test, valid_items):
        return [item
                for item in items_for_test
                if item not in valid_items]

    def _validate_shirt_size(self, dataset):
        def file_shirt_sizes(dataset):
            shirt_size_columns = subscriptions.core.models.\
                    Column.objects.filter(subscription_name__exact='shirt_size').\
                    values_list('file_name', flat=True)
            columns_intersection = set(shirt_size_columns).intersection(dataset.columns)
            if columns_intersection:
                file_shirt_size_column = list(columns_intersection)[0]
                return dataset[file_shirt_size_column]
            else:
                return []

        message = 'Tamanhos de Camiseta %(invalid_shirt_sizes)s invalidos'
        file_shirt_sizes = file_shirt_sizes(dataset)
        valid_shirt_sizes = subscriptions.core.models.\
                ShirtSize.objects.filter(file_shirt_size__in=set(file_shirt_sizes))\
                .values_list('file_shirt_size', flat=True)
        invalid_shirt_sizes = self._invalid_items(file_shirt_sizes, valid_shirt_sizes)

        if invalid_shirt_sizes:
            raise ValidationError(
                message,
                code='shirt_size',
                params={'invalid_shirt_sizes': set(invalid_shirt_sizes)}
            )

    def __eq__(self, other):
        return isinstance(other, FileValidator)

validate_file = FileValidator()
