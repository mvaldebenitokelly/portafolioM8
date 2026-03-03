from django import forms
from .models import Product, ContactMessage

BOOTSTRAP_INPUT = {"class": "form-control"}
BOOTSTRAP_TEXTAREA = {"class": "form-control", "rows": 4}
BOOTSTRAP_SELECT = {"class": "form-select"}
BOOTSTRAP_CHECK = {"class": "form-check-input"}


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ["name", "description", "price", "stock", "category", "active", "image"]
        widgets = {
            "name": forms.TextInput(attrs=BOOTSTRAP_INPUT),
            "description": forms.Textarea(attrs=BOOTSTRAP_TEXTAREA),
            "price": forms.NumberInput(attrs={**BOOTSTRAP_INPUT, "step": "0.01", "min": "0.01"}),
            "stock": forms.NumberInput(attrs={**BOOTSTRAP_INPUT, "min": "0"}),
            "category": forms.Select(attrs=BOOTSTRAP_SELECT),
            "active": forms.CheckboxInput(attrs=BOOTSTRAP_CHECK),
            "image": forms.ClearableFileInput(attrs={"class": "form-control"}),
        }

    def clean_price(self):
        price = self.cleaned_data.get("price")
        if price is None or price <= 0:
            raise forms.ValidationError("El precio debe ser mayor a 0.")
        return price


class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ["name", "email", "subject", "message"]
        widgets = {
            "name": forms.TextInput(attrs=BOOTSTRAP_INPUT),
            "email": forms.EmailInput(attrs=BOOTSTRAP_INPUT),
            "subject": forms.TextInput(attrs=BOOTSTRAP_INPUT),
            "message": forms.Textarea(attrs=BOOTSTRAP_TEXTAREA),
        }

    def clean_message(self):
        msg = (self.cleaned_data.get("message") or "").strip()
        if len(msg) < 10:
            raise forms.ValidationError("El mensaje debe tener al menos 10 caracteres.")
        return msg
