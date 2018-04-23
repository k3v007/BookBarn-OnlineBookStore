from django import forms
from django.contrib.auth.models import User
from BookBarnApp.models import UserProfiles


class UserUpdateForm(forms.ModelForm):

    first_name = forms.CharField(
            required=True, 
            max_length=50,
            label='First Name', 
            widget=forms.TextInput(
                    attrs={
                        "class":"form-control",
                        "id":"id_firstName",
                        }
                    )
            )

    last_name = forms.CharField(
            required=True,
            max_length=50,
            label='Last Name',
            widget=forms.TextInput(
                    attrs={
                        "class":"form-control",
                        "id":"id_lastName",
                        }
                    )
            )

    def clean(self):
        data=self.cleaned_data
        return data

    class Meta:
        model = User
        fields = ('first_name', 'last_name')


# User Signup Form Part 2
class UserProfileUpdateForm(forms.ModelForm):
    phoneNumber = forms.CharField(
            required=True,
            label='Phone Number',
            min_length=10,
            max_length=10,
            widget=forms.TextInput(
                    attrs={
                        "class":"form-control",
                        "id":"id_phoneNumber",
                        'oninput': 'onlyNumber(id)',
                        }
                    )
            )

    address1 = forms.CharField(
            required=True,
            label='Address Line 1',
            max_length=50,
            widget=forms.TextInput(
                    attrs={
                        "class":"form-control", 
                        "id":"id_address1",
                        }
                    )
            )

    address2 = forms.CharField(
            required=False,
            label='Address Line 2',
            max_length=50,
            widget=forms.TextInput(
                    attrs={
                        "class":"form-control",
                        "id":"id_address2",
                        }
                    )
            )

    city = forms.CharField(
            required=True, 
            label='City',
            max_length=50,
            widget=forms.TextInput(
                    attrs={
                        "class":"form-control",
                        "id":"id_city",
                        }
                    )
            )

    state = forms.CharField(
            required=True,
            label='State',
            max_length=50,
            widget=forms.TextInput(
                    attrs={
                        "class":"form-control", 
                        "id":"id_state",
                        }
                    )
            )

    pinCode = forms.CharField(
            required=True, 
            label='PIN Code', 
            min_length=6, 
            max_length=6, 
            widget=forms.TextInput(
                    attrs={
                        "class":"form-control",
                        "id":"id_pincode",
                        'autocomplete': 'off',
                        'oninput': 'onlyNumber(id)',
                        }
                    )
            )
    
    def clean(self):
        data=self.cleaned_data
        return data

    class Meta:
        model = UserProfiles
        fields = ('address1', 'address2', 'city', 'state', 'pinCode', 'phoneNumber')


class UserPwdUpdateForm(forms.ModelForm):
    password = forms.CharField(
            label='New Password',
            required=True,
            min_length=6,
            max_length=50,
            widget=forms.PasswordInput(
                    attrs={
                        "class":"form-control",                        
                        "id":"id_password",
                        }
                    )
            )

    password1 = forms.CharField(
            label='Re-enter Password',
            required=True,
            min_length=6,
            max_length=50,
            widget=forms.PasswordInput(
                    attrs={
                        "class":"form-control",
                        "id":"id_password1",
                        }
                    )
            )

    def clean(self):
        data=self.cleaned_data
        password=self.cleaned_data.get("password")
        password1=self.cleaned_data.get("password1")

        if password != password1:
            raise forms.ValidationError("Passwords must match.")
        else:
            return data

    class Meta:
        model = User
        fields = ('password', 'password1')