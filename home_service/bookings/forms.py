from django import forms
from .models import Booking,Review

from django import forms
from .models import Booking
from datetime import date
from django import forms
from .models import Booking
from django.contrib.auth import get_user_model

User = get_user_model()

from django import forms
from datetime import date
from .models import Booking

class BookingForm(forms.ModelForm):

    class Meta:
        model = Booking
        fields = ['freelancer', 'date', 'time', 'address']

        widgets = {
            'freelancer': forms.Select(attrs={'class': 'form-control'}),

            'date': forms.DateInput(attrs={
                'type': 'date',
                'class': 'form-control',
                'min': date.today().isoformat()   # ✅ disable past dates
            }),

            'time': forms.TimeInput(attrs={
                'type': 'time',
                'class': 'form-control'
            }),

            'address': forms.TextInput(attrs={'class': 'form-control'}),
        }

    # 🔒 BACKEND VALIDATION (VERY IMPORTANT)
    def clean_date(self):
        selected_date = self.cleaned_data['date']

        if selected_date < date.today():
            raise forms.ValidationError("Past dates are not allowed")

        return selected_date
class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'comment']
        widgets = {
            'rating': forms.Select(choices=[(i, i) for i in range(1, 6)]),
        }        