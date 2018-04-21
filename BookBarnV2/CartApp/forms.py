from django import forms

# ADDRESS_CHOICES = (
#     ('dft_add', "Default Address"),
#     ('new_add', "Other Address"),
# )

# # Address Selection Form
# class AddressChoiceForm(forms.Form):
#     delivery_address = forms.CharField(
#             label='Select Delivery Address',
#             widget=forms.RadioSelect(
#                     choices=ADDRESS_CHOICES,
#                     )
#             )
#     def clean(self):
#         data=self.cleaned_data
#         return data

# Form for filling New Address
class NewAddressForm(forms.Form):    
    address1 = forms.CharField(
            required=False, 
            label='', 
            max_length=50, 
            widget=forms.TextInput(
                    attrs={
                        "class":"form-control required_field_1", 
                        "placeholder":"Address Line 1", 
                        "id":"id_address1",
                        }
                    )
            )

    address2 = forms.CharField(
            required=False, 
            label='', 
            max_length=50, 
            widget=forms.TextInput(
                    attrs={
                        "class":"form-control", 
                        "placeholder":"Address Line 2", 
                        "id":"id_address2",
                        }
                    )
            )

    city = forms.CharField(
            required=False, 
            label='', 
            max_length=50, 
            widget=forms.TextInput(
                    attrs={
                        "class":"form-control required_field_1", 
                        "placeholder":"City", 
                        "id":"id_city",
                        }
                    )
            )

    state = forms.CharField(
            required=False, 
            label='', 
            max_length=50, 
            widget=forms.TextInput(
                    attrs={
                        "class":"form-control required_field_1", 
                        "placeholder":"State", 
                        "id":"id_state",
                        }
                    )
            )

    pinCode = forms.CharField(
            required=False, 
            label='', 
            min_length=6, 
            max_length=6, 
            widget=forms.TextInput(
                    attrs={
                        "class":"form-control required_field_1", 
                        "placeholder":"PIN Code", 
                        "id":"id_pincode",
                        'oninput': 'onlyNumber(id)'
                        }
                    )
            )

    phoneNumber = forms.CharField(
            required=False, 
            label='', 
            min_length=10, 
            max_length=10, 
            widget=forms.TextInput(
                    attrs={
                        "class":"form-control required_field_1", 
                        "placeholder":"Phone Number", 
                        "id":"id_phoneNumber",
                        'style': 'width:50ch',
                        'oninput': 'onlyNumber(id)'
                        }
                    )
            ) 
    
    def clean(self):
        data=self.cleaned_data
        return data


# Form for crredit/debit card details
class CardForm(forms.Form):
    name = forms.CharField(
            required=False, 
            max_length=50,
            label='', 
            widget=forms.TextInput(
                    attrs={
                        "class":"form-control required_field_2", 
                        "placeholder":"Name on Card", 
                        "id":"name",
                        "autocomplete":"off",
                        }
                    )
            )
        
    cvv = forms.CharField(
            label='', 
            required=False, 
            min_length=3, 
            max_length=3, 
            widget=forms.PasswordInput(
                    attrs={ 
                        "class":"form-control required_field_2",
                        "placeholder":"CVV", 
                        "id":"cvv",
                        'oninput': 'onlyNumber(id)',
                        }   
                    )
            )
    
    cardNumber = forms.CharField(
            required=False, 
            label='', 
            min_length=16, 
            max_length=16, 
            widget=forms.TextInput(
                    attrs={
                        "class":"form-control required_field_2", 
                        "placeholder":"Card Number", 
                        "id":"cardNumber",
                        'oninput': 'onlyNumber(id)',
                        }
                    )
            ) 
    
    date_mm = forms.CharField(
            required=False, 
            label='', 
            min_length=2, 
            max_length=2, 
            widget=forms.TextInput(
                    attrs={
                        "class":"form-control required_field_2", 
                        "placeholder":"MM", 
                        "id":"date_mm",
                        'oninput': 'onlyNumber(id)'
                        }
                    )
            )

    date_yyyy = forms.CharField(
            required=False, 
            label='', 
            min_length=4, 
            max_length=4, 
            widget=forms.TextInput(
                    attrs={
                        "class":"form-control required_field_2", 
                        "placeholder":"YYYY", 
                        "id":"date_yyyy",
                        'oninput': 'onlyNumber(id)'
                        }
                    )
            )
    def clean(self):
        data=self.cleaned_data
        return data