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
        message = 'Colunas %(invalid_columns)s invalidas'
        self._save_file(filepath, value)

        csv = pd.DataFrame.from_csv(filepath, sep=';')

        column_filter = subscriptions.core.models.\
                Column.objects.filter(file_name__in=set(csv.columns))
        columns = column_filter.values('file_name')
        valid_columns = [c['file_name'] for c in columns]
        invalid_columns = [column
                           for column in csv.columns
                           if column not in valid_columns]
        if invalid_columns:
            raise ValidationError(message,
                                  code='columns',
                                  params={'invalid_columns': invalid_columns})

    def __eq__(self, other):
        return isinstance(other, FileValidator)

validate_file = FileValidator()
