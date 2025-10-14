from django import forms
from .models import Profile,UserTag
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import password_validation
from django.core.exceptions import ValidationError


class UserRegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username__iexact=username).exists():
            raise forms.ValidationError("That username is already taken.")
        return username

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        base_classes = (
            "w-full rounded-lg border border-[#d8c3a5] bg-white/70 px-4 py-2 "
            "text-[#3b2f2f] outline-none transition focus:border-[#c0a080] "
            "focus:ring-2 focus:ring-[#d2a679]/40"
        )
        placeholders = {
            'username': 'Enter your username',
            'password1': 'Create a password',
            'password2': 'Repeat your password',
        }
        labels = {
            'password1': 'Password',
            'password2': 'Confirm Password',
        }
        for name, field in self.fields.items():
            field.widget.attrs.setdefault("class", base_classes)
            if name in placeholders:
                field.widget.attrs.setdefault("placeholder", placeholders[name])
            if name in labels:
                field.label = labels[name]

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2:
            if password1 != password2:
                raise forms.ValidationError(
                    self.error_messages['password_mismatch'],
                    code='password_mismatch',
                )
            self.instance.username = self.cleaned_data.get('username')
            try:
                password_validation.validate_password(password2, self.instance)
            except ValidationError as exc:
                for message in exc.messages:
                    self.add_error('password1', message)
                raise forms.ValidationError(exc.messages)
        return password2

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['Display_name', 'name', 'family', 'number', 'bio', 'email', 'ProfileImage']

    def clean_number(self):
        number = self.cleaned_data.get('number')
        if Profile.objects.filter(number = number).exists():
            raise forms.ValidationError("That phone number is already registered.")
        return number
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if Profile.objects.filter(email = email).exists():
            raise forms.ValidationError("That email is already registered.")
        return email


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        base_classes = (
            "w-full rounded-lg border border-[#d8c3a5] bg-white/70 px-4 py-2 "
            "text-[#3b2f2f] outline-none transition focus:border-[#c0a080] "
            "focus:ring-2 focus:ring-[#d2a679]/40"
        )
        placeholders = {
            'Display_name': 'Display name',
            'name': 'First name',
            'family': 'Last name',
            'number': 'Phone number',
            'bio': 'Tell us about yourself',
            'email': 'Email address',
        }
        for name, field in self.fields.items():
            if isinstance(field.widget, forms.FileInput):
                field.widget.attrs.setdefault(
                    "class",
                    "block w-full text-sm text-[#3b2f2f] file:mr-4 file:rounded-md "
                    "file:border-0 file:bg-[#d2a679] file:px-4 file:py-2 file:text-sm "
                    "file:font-semibold file:text-white hover:file:bg-[#c59568]"
                )
            elif isinstance(field.widget, forms.Textarea):
                field.widget.attrs.setdefault("class", base_classes)
                field.widget.attrs.setdefault("rows", 4)
            else:
                field.widget.attrs.setdefault("class", base_classes)
            if name in placeholders:
                field.widget.attrs.setdefault("placeholder", placeholders[name])

class UserTagForm(forms.ModelForm):
    class Meta:
        model = UserTag
        fields = ['title']
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        input_classes = (
            "w-full rounded-xl border border-[#d2a679]/40 bg-white/80 px-4 py-2 "
            "text-sm text-[#3b2f2f] placeholder:text-[#6d4c41]/40 "
            "focus:border-[#c59568] focus:outline-none focus:ring-2 focus:ring-[#d2a679]/40"
        )
        self.fields['title'].label = "Tag name"
        self.fields['title'].widget.attrs.setdefault("class", input_classes)
        self.fields['title'].widget.attrs.setdefault("placeholder", "e.g. Ideas")

