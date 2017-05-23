import os
import pandas as pd
from datetime import datetime
from subscriptions.core.models import Subscription

class SubscriptionImporter:
    def __init__(self, filepath):
        self.filepath = filepath

    def save(self):
        csv = pd.DataFrame.from_csv(self.filepath, sep=';')
        records = csv.to_dict('records')
        # import pdb;pdb.set_trace()
        model_instances = [Subscription(
            name=record['*Nome Completo'],
            email=record['E-mail'],
            name_for_bib_number=record['Nome para Numero de Peito'],
            gender=record['*Sexo (M ou F)'],
            date_of_birth=datetime.strptime(
                record['*Data Nascimento (dd/mm/aaaa)'],
                '%d/%m/%Y').date(),
            city=record['Cidade'],
            team=record['Equipe'],
            shirt_size=record['Tamanho da Camiseta'],
            modality=record['Modalidade'],
        ) for record in records]

        Subscription.objects.bulk_create(model_instances)

    def _delete_file(self):
        os.remove(self.filepath)
