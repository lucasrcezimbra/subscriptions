from django import forms


class ExportForm(forms.Form):
    FORMATS = (
        ('csv', 'CSV'),
        ('xlsx', 'XLSX'),
    )
    FIELDS = [
        ('id', 'ID'),
        ('name', 'nome'),
        ('email', 'e-mail'),
        ('name_for_bib_number', 'nome para número de peito'),
        ('gender', 'sexo'),
        ('date_of_birth', 'data de nascimento'),
        ('city', 'cidade'),
        ('team', 'equipe'),
        ('modality', 'modalidade'),
        ('shirt_size', 'tamanho da camiseta'),
        ('paid', 'pago'),
        ('import_t__origin', 'origin'),
    ]
    format = forms.ChoiceField(
        label='Formato',
        widget=forms.RadioSelect,
        choices=FORMATS)
    fields = forms.MultipleChoiceField(
        label='Campos',
        widget=forms.SelectMultiple(attrs={'size': len(FIELDS)+1}),
        choices=FIELDS)
