from django import forms
from django.contrib.auth.models import User
from .models import Profile, Notification

class RegisterForm(forms.ModelForm):
    """
    Form to handle user registration, capturing base user fields
    as well as profile fields in one process.
    """
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=50, required=True)
    last_name = forms.CharField(max_length=50, required=True)
    phone_number = forms.CharField(max_length=15, required=False)
    profile_picture = forms.ImageField(required=False)
    
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password_confirm = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}), label="Confirm Password")

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'password']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("A user with this email already exists.")
        return email

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password_confirm = cleaned_data.get("password_confirm")

        if password and password_confirm and password != password_confirm:
            self.add_error('password_confirm', "Passwords do not match.")
        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
            # The profile is automatically created by signal. We update the profile details.
            profile = user.profile
            profile.phone_number = self.cleaned_data.get('phone_number')
            if self.cleaned_data.get('profile_picture'):
                profile.profile_picture = self.cleaned_data.get('profile_picture')
            profile.save()
        return user


class UserUpdateForm(forms.ModelForm):
    """
    Form to update standard User details: first name, last name, email.
    """
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']


class ProfileUpdateForm(forms.ModelForm):
    """
    Form to update Profile details: phone number, profile picture.
    """
    class Meta:
        model = Profile
        fields = ['phone_number', 'profile_picture']


class NotificationForm(forms.ModelForm):
    """
    Form used by admins to publish a platform-wide notification.
    """
    class Meta:
        model = Notification
        fields = ['title', 'message', 'target']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. Maintenance window'}),
            'message': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Share important news with attendees.'}),
            'target': forms.Select(attrs={'class': 'form-select'}),
        }
