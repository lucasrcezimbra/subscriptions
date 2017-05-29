import pandas as pd
from django.core.exceptions import ValidationError
import subscriptions.core.models

class ValidateFile:
    def columns(value):
        filepath = 'test123.csv'
        with open(filepath, 'wb+') as destination:
            for chunk in value.chunks():
                destination.write(chunk)

        csv = pd.DataFrame.from_csv(filepath, sep=';')

        columns = subscriptions.core.models.\
                Column.objects.filter(file_name__in=set(csv.columns)).values('file_name')
        valid_columns = [c['file_name'] for c in columns]
        invalid_columns = [column
                           for column in csv.columns
                           if column not in valid_columns]
        if invalid_columns:
            message = 'Colunas {} invalidas'.format(invalid_columns)
            raise ValidationError(message)
