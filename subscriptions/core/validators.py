import pandas as pd
from django.core.exceptions import ValidationError
from django.utils.deconstruct import deconstructible
import subscriptions.core.models

@deconstructible
class FileValidator(object):
    def _save_file(self, filepath, value):
        with open(filepath, 'wb+') as destination:
            for chunk in value.chunks():
                destination.write(chunk)

    def __call__(self, value):
        filepath = 'test123.csv'
        self._save_file(filepath, value)
        csv = pd.DataFrame.from_csv(filepath, sep=';')

        self._validate_columns(csv)
        self._validate_shirt_size(csv)

    def _validate_columns(self, csv):
        message = 'Colunas %(invalid_columns)s invalidas'
        column_filter = subscriptions.core.models.\
                Column.objects.filter(file_name__in=set(csv.columns))
        columns = column_filter.values('file_name')
        valid_columns = [c['file_name'] for c in columns]
        invalid_columns = [column
                           for column in csv.columns
                           if column not in valid_columns]
        if invalid_columns:
            raise ValidationError(
                message,
                code='columns',
                params={'invalid_columns': invalid_columns}
            )

    def _validate_shirt_size(self, csv):
        message = 'Tamanhos de Camiseta %(invalid_shirt_sizes)s invalidos'
        shirt_size_columns = subscriptions.core.models.\
                Column.objects.filter(subscription_name__exact='shirt_size').\
                values_list('file_name', flat=True)
        abc = set(shirt_size_columns).intersection(csv.columns)
        file_shirt_size_column = list(
            set(shirt_size_columns).intersection(csv.columns)
        )[0]
        file_shirt_sizes = csv[file_shirt_size_column]
        shirt_size_filter = subscriptions.core.models.\
                ShirtSize.objects.filter(file_shirt_size__in=set(file_shirt_sizes))
        shirt_sizes = shirt_size_filter.values('file_shirt_size')
        valid_shirt_sizes = [c['file_shirt_size'] for c in shirt_sizes]
        invalid_shirt_sizes = [shirt_size
                               for shirt_size in file_shirt_sizes
                               if shirt_size not in valid_shirt_sizes]
        if invalid_shirt_sizes:
            raise ValidationError(
                message,
                code='shirt_size',
                params={'invalid_shirt_sizes': set(invalid_shirt_sizes)}
            )

    def __eq__(self, other):
        return isinstance(other, FileValidator)

validate_file = FileValidator()
