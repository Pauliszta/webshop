from django import forms
from .models import UserBase
from django.contrib.auth.forms import AuthenticationForm


class RegistrationForm(forms.ModelForm):
    user_name = forms.CharField(label="Wprowadź nazwę użytkownika", min_length=4, max_length=50, help_text='Wymagane')
    email = forms.EmailField(label="Wprowadź e-maila", max_length=100, help_text='Wymagane',
                             error_messages={'required': 'Przykro mi, potrzebujemy Twojego maila'})
    password = forms.CharField(label='Wprowadź hasło', widget=forms.PasswordInput)
    password2 = forms.CharField(label="Powtórz hasło", widget=forms.PasswordInput)
    first_name = forms.CharField(label="Podaj imię", min_length=4, max_length=50)
    last_name = forms.CharField(label="Podaj nazwisko", min_length=2, max_length=50)

    class Meta:
        model = UserBase
        fields = ('user_name', 'email',)

    def clean_username(self):
        user_name = self.cleaned_data['user_name'].lower()
        r = UserBase.objects.filter(user_name=user_name)
        if r.count():
            raise forms.ValidationError("Użytkownik o takiej nazwie już istnieje")
        return user_name

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Podane hasła nie są identyczne.')
        return cd['password2']

    def clean_email(self):
        email = self.cleaned_data['email'].lower()
        if UserBase.objects.filter(email=email).exists():
            raise forms.ValidationError("Proszę użyć innego adresu mailowego, ten już jest używany")
        return email

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['user_name'].widget.attrs.update(
            {'class': 'form-control mb-3', 'placeholder': 'Nazwa użytkownika'})
        self.fields['email'].widget.attrs.update(
            {'class': 'form-control mb-3', 'placeholder': 'E-mail', 'name': 'email'})
        self.fields['password'].widget.attrs.update(
            {'class': 'form-control mb-3', 'placeholder': 'Hasło'})
        self.fields['password2'].widget.attrs.update(
            {'class': 'form-control mb-3', 'placeholder': 'Powtórz hasło'})
        self.fields['first_name'].widget.attrs.update(
            {'class': 'form-control mb-3', 'placeholder': 'Imię'})
        self.fields['last_name'].widget.attrs.update(
            {'class': 'form-control mb-3', 'placeholder': 'Nazwisko'})


class UserLoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control mb-3',
                                                             'placeholder': 'Nazwa użytkownika',
                                                             'id': 'login-username'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Hasło',
            'id': 'login-pwd',
        }
    ))


class UserEditForm(forms.ModelForm):
    email = forms.EmailField(label='Email nie może być zmieniony', max_length=100, widget=forms.TextInput(
        attrs={'class': 'forms-control mb-3', 'placeholder': 'email', 'id': 'form-email', 'readonly': 'readonly'}))
    user_name = forms.CharField(label='Nazwa użytkownika', min_length=4, max_length=50, widget=forms.TextInput(
        attrs={'class': 'form-control mb-3', 'placeholder': 'Nazwa użytkownika', 'id': 'form-username',
               'readonly': 'readonly'}))
    first_name = forms.CharField(label='Imię', min_length=3, max_length=50, widget=forms.TextInput(
        attrs={'class': 'form-control mb-3', 'placeholder': 'Imię', 'id': 'form-firstname'}))
    last_name = forms.CharField(label="Nazwisko", min_length=3, max_length=50, widget=forms.TextInput(
        attrs={'class': 'form-control mb-3', 'placeholder': 'Nazwisko', 'id': 'form-lastname'}))
    address = forms.CharField(label="Adres", max_length=150, widget=forms.TextInput(
        attrs={'class': 'form-control mb-3', 'placeholder': 'Adres', 'id': 'form-address'}))
    postal_code = forms.CharField(label="Kod pocztowy", max_length=20, widget=forms.TextInput(
        attrs={'class': 'form-control mb-3', 'placeholder': 'Kod pocztowy', 'id': 'form-postalcode'}))
    city = forms.CharField(label="Miasto", max_length=150, widget=forms.TextInput(
        attrs={'class': 'form-control mb-3', 'placeholder': 'Miasto', 'id': 'form-city'}))

    class Meta:
        model = UserBase
        fields = ('email', 'user_name', 'first_name', 'last_name', 'address', 'postal_code', 'city')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['user_name'].required = True
        self.fields['email'].required = True
