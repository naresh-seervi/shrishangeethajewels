from django import forms
from django.contrib.auth.forms import UserCreationForm, PasswordResetForm
from django.core.validators import RegexValidator  # ✅ Correct import
from .models import CustomUser, Item, Rate, Order


class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    mobile = forms.CharField(
        max_length=10,
        required=True,
        validators=[RegexValidator(regex=r'^\d{10}$', message='Mobile number must be 10 digits')]
    )

    class Meta:
        model = CustomUser
        fields = ('first_name', 'email', 'mobile', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if 'username' in self.fields:
            del self.fields['username']
        self.fields['first_name'].label = 'Full Name'
        self.fields['first_name'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Full Name'})
        self.fields['email'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Email'})
        self.fields['mobile'].widget.attrs.update({'class': 'form-control', 'placeholder': '10-digit Mobile Number'})
        self.fields['password1'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Password'})
        self.fields['password2'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Confirm Password'})

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if CustomUser.objects.filter(email=email).exists():
            raise forms.ValidationError("This email is already registered.")
        return email

    def clean_mobile(self):
        mobile = self.cleaned_data.get('mobile')
        if CustomUser.objects.filter(mobile=mobile).exists():
            raise forms.ValidationError("This mobile number is already registered.")
        return mobile

    def save(self, commit=True):
        user = super().save(commit=False)
        base_username = email_to_username(self.cleaned_data['email'])
        username = base_username
        counter = 0
        while CustomUser.objects.filter(username=username).exists():
            counter += 1
            username = f"{base_username}_{counter}"
        user.username = username
        if commit:
            user.save()
        return user


def email_to_username(email):
    """Convert email to a valid username (letters, digits, @/./+/-/_ only)."""
    import re
    s = email.split('@')[0]
    s = re.sub(r'[^\w.+-]', '_', s)[:150]
    return s or 'user'


class LoginForm(forms.Form):
    email_or_mobile = forms.CharField(max_length=255, required=True, label='Email or Mobile Number')
    password = forms.CharField(widget=forms.PasswordInput, required=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email_or_mobile'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Email or Mobile Number'
        })
        self.fields['password'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Password',
             'id': 'id_password'
        })


class OTPVerifyForm(forms.Form):
    otp = forms.CharField(max_length=6, required=True, min_length=6)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['otp'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Enter 6-digit OTP',
            'maxlength': '6',
            'pattern': '[0-9]{6}'
        })


class ItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ['name', 'image', 'weight', 'item_type', 'description', 'video_url']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'image': forms.FileInput(attrs={'class': 'form-control'}),
            'weight': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.001'}),
            'item_type': forms.Select(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Additional details about the item'}),
            'video_url': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'https://... (optional)'}),
        }


class RateForm(forms.ModelForm):
    class Meta:
        model = Rate
        fields = ['rate_type', 'per_gram_rate']
        widgets = {
            'rate_type': forms.Select(attrs={'class': 'form-control'}),
            'per_gram_rate': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
        }


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['address']
        widgets = {
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
        }

