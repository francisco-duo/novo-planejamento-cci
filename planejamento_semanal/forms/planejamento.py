from django import forms
from planejamento_semanal.models import PlanejamentoModel


class PlanjemantoForm(forms.ModelForm):
    class Meta:
        model = PlanejamentoModel
        fields = '__all__'
        exclude = (
            'planejamento_semanal_criador',
            'registro_planejamento_semanal_dt',
            'planejamento_semanal_enviado',
            'planejamento_semanal_cod_classroom'
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control mb-3 shadow'
