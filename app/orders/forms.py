from django import forms

from .models import Product


class OrderChangeListForm(forms.ModelForm):
    products = forms.ModelMultipleChoiceField(queryset=Product.objects.all(), required=False)
