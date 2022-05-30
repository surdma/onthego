from django import forms
from django.utils.translation import gettext_lazy as _
class CartAddForm(forms.Form):
    quantity = forms.IntegerField(min_value=1, max_value=1000,label=_("Product Quantity"))
    override = forms.BooleanField(required=False, initial=False, widget=forms.HiddenInput)