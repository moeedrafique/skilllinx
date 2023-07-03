from django import forms
from .models import Registration

class RegistrationForm(forms.ModelForm):
    declaration = forms.BooleanField(
        required=True,
        widget=forms.CheckboxInput(attrs={
            'class': 'form-check-input',
            'value': 'I hereby acknowledge that I have carefully read and agree to the terms and conditions outlined by BMC Training and Development. I understand that BMC Training and Development shall not be held responsible for any damage, loss, or incorrect information submitted through this registration form. I take full responsibility for the accuracy and validity of the information provided.'
        })
    )

    class Meta:
        model = Registration
        fields = [
            'name',
            'email',
            'phone_number',
            'job_title',
            'passport_number',
            'nationality',
            'company_name',
            'company_country',
            'company_city',
            'company_address',
            'declaration',
        ]
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control'}),
            'job_title': forms.TextInput(attrs={'class': 'form-control'}),
            'passport_number': forms.TextInput(attrs={'class': 'form-control'}),
            'nationality': forms.TextInput(attrs={'class': 'form-control'}),
            'company_name': forms.TextInput(attrs={'class': 'form-control'}),
            'company_country': forms.TextInput(attrs={'class': 'form-control'}),
            'company_city': forms.TextInput(attrs={'class': 'form-control'}),
            'company_address': forms.TextInput(attrs={'class': 'form-control'}),
            'declaration': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        required_fields = ['name', 'email', 'phone_number', 'job_title', 'company_name',
                           'company_country', 'company_city', 'company_address', 'declaration']

        for field in required_fields:
            if not cleaned_data.get(field):
                self.add_error(field, 'This field is required.')


        email = cleaned_data.get('email')
        phone_number = cleaned_data.get('phone_number')
        declaration = cleaned_data.get('declaration')

        # Validate email and phone number uniqueness
        if email and Registration.objects.filter(email=email).exists():
            self.add_error('email', 'This email address is already registered.')

        if phone_number and Registration.objects.filter(phone_number=phone_number).exists():
            self.add_error('phone_number', 'This phone number is already registered.')

        # Validate declaration checkbox
        if not declaration:
            self.add_error('declaration', 'You must accept the declaration.')

        return cleaned_data
