from django.db import models

class Subscription(models.Model):
    GENDERS = (
        ('F', 'Feminino'),
        ('M', 'Masculino'),
    )

    name = models.CharField('nome', max_length=200)
    email = models.EmailField('e-mail')
    name_for_bib_number = models.CharField('nome para número de peito',
                                           max_length=200)
    gender = models.CharField('sexo', max_length=1, choices=GENDERS)
    date_of_birth = models.DateField('data de nascimento')
    city = models.CharField('cidade', max_length=100)
    team = models.CharField('equipe', max_length=100)
    shirt_size = models.CharField('tamanho da camiseta', max_length=25)
    modality = models.CharField('modalidade', max_length=25)
