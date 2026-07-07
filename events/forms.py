from django import forms
from .models import Event

class EventForm(forms.ModelForm):
    """
    Form for organizers/admins to create and edit events.
    """
    class Meta:
        model = Event
        fields = [
            'title', 'description', 'category', 'date', 
            'time', 'venue', 'capacity', 'ticket_price', 
            'image', 'status'
        ]
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter event title'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Describe the event...'}),
            'category': forms.Select(attrs={'class': 'form-select'}),
            'date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'time': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
            'venue': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter venue name/address'}),
            'capacity': forms.NumberInput(attrs={'class': 'form-control', 'min': 1}),
            'ticket_price': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'min': '0.00'}),
            'image': forms.FileInput(attrs={'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-select'}),
        }
