import pandas as pd
from django.core.exceptions import ValidationError

class ValidateFile:
    def columns(value):
        valid_columns = ("*Nome Completo","Nome para Numero de Peito","*Sexo (M ou F)","*Data Nascimento (dd/mm/aaaa)","CPF","Cidade","Equipe","E-mail","Modalidade","Tamanho da Camiseta")
        filepath = 'test123.csv'
        with open(filepath, 'wb+') as destination:
            for chunk in value.chunks():
                destination.write(chunk)

        csv = pd.DataFrame.from_csv(filepath, sep=';')
        invalid_columns = [column
                           for column in csv.columns
                           if column not in valid_columns]
        if invalid_columns:
            message = 'Colunas {} invalidas'.format(invalid_columns)
            raise ValidationError(message)
