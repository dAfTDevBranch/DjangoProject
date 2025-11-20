from django import forms

from .models import Feedback, Task


class TaskForm(forms.ModelForm):
    due_date = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={"type": "date"}),
        label="Fecha límite",
    )

    class Meta:
        model = Task
        fields = ["title", "description", "due_date", "category", "tags", "completed"]
        widgets = {
            "description": forms.Textarea(attrs={"rows": 4}),
            "tags": forms.CheckboxSelectMultiple(),
        }
        labels = {
            "title": "Título",
            "description": "Descripción",
            "category": "Categoría",
            "tags": "Etiquetas",
            "completed": "Completada",
        }


class TaskCompleteForm(forms.Form):
    confirm = forms.BooleanField(
        required=True,
        label="Confirmo que deseo marcar la tarea como completada",
    )

class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = ["name", "comment", "rating"]
        widgets = {
            "name": forms.TextInput,
            "comment": forms.Textarea(attrs={"rows": 4}),
            "rating": forms.NumberInput(attrs={"min": 1, "max": 10}),
        }
        labels = {
            "name": "Nombre",
            "comment": "Comentario",
            "rating": "Calificación (1-10)",
        }