# creao este rchivo form, para formularios personalizados
# formularios que usen, modelos que yo cree 
from django import forms
from .models import Task

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title','description','important']
        widgets = {
                    'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Write a Title'}), # paso la clase de bustra que desee
                    'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Write a descrition'}),
                    'important': forms.CheckboxInput(attrs={'class': 'form-check-input'})
                    }
        

