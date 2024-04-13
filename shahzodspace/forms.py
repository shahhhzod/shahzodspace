from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Product, Category, Sale
from decimal import Decimal
from decimal import Decimal, ROUND_DOWN

value = Decimal("10.123")
value = value.quantize(Decimal("1.00"), rounding=ROUND_DOWN)


class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True, help_text="Обязательное поле. Введите действующий адрес электронной почты.")

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'password1': forms.PasswordInput(attrs={'class': 'form-control'}),
            'password2': forms.PasswordInput(attrs={'class': 'form-control'}),
        }

    def save(self, commit=True):
        user = super(CustomUserCreationForm, self).save(commit=False)
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['photo', 'item_number', 'category', 'name', 'model', 'quantity', 'purchase_price', 'selling_price']
        widgets = {
            'item_number': forms.TextInput(attrs={'class': 'form-control'}),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'model': forms.TextInput(attrs={'class': 'form-control'}),
            'quantity': forms.NumberInput(attrs={'class': 'form-control'}),
            'purchase_price': forms.NumberInput(attrs={'class': 'form-control'}),
            'selling_price': forms.NumberInput(attrs={'class': 'form-control'}),
            'photo': forms.FileInput(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
        }

def __init__(self, *args, **kwargs):
    user = kwargs.pop('user', None)
    super(ProductForm, self).__init__(*args, **kwargs)
    if user:
        self.fields['category'].queryset = Category.objects.filter(user=user)
        # Добавляем логгирование для отладки
        print(f"User: {user.username}, Categories: {list(self.fields['category'].queryset)}")
    else:
        print("No user provided for ProductForm")




class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'description']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control w-50'}),
            'description': forms.Textarea(attrs={'class': 'form-control w-50'}),
        }

    def __init__(self, *args, **kwargs):
        super(CategoryForm, self).__init__(*args, **kwargs)
        # Здесь не нужно изменять queryset для 'category', так как это форма для категорий, а не для продуктов.

class SaleForm(forms.ModelForm):
    class Meta:
        model = Sale
        fields = ['product', 'quantity', 'discount_percentage', 'sale_price']
        widgets = {
            'product': forms.TextInput(attrs={'class': 'hidden'}),
            'quantity': forms.TextInput(attrs={'class': 'form-control'}),
            'discount_percentage': forms.NumberInput(attrs={'class': 'form-control'}),
            'sale_price': forms.NumberInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        product = kwargs.pop('product', None)
        super().__init__(*args, **kwargs)
        if product:
            self.fields['product'].initial = product.id
            self.fields['quantity'].initial = 1
            self.fields['sale_price'].initial = product.selling_price

    def clean(self):
        cleaned_data = super().clean()
        sale_price = cleaned_data.get('sale_price')

        if sale_price:
            cleaned_data['sale_price'] = sale_price.quantize(Decimal('0.01'), rounding=ROUND_DOWN)
    
        return cleaned_data
    
class DateRangeForm(forms.Form):
    start_date = forms.DateField(label='Начальная дата', widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}))
    end_date = forms.DateField(label='Конечная дата', widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}))
    category = forms.ModelChoiceField(queryset=Category.objects.none(), label='Категория', required=False, widget=forms.Select(attrs={'select': 'text', 'class': 'form-control'}))

    def __init__(self, *args, user=None, **kwargs):
        super(DateRangeForm, self).__init__(*args, **kwargs)
        if user:
            self.fields['category'].queryset = Category.objects.filter(user=user)

    #  return redirect('product_list')  
    # else:
    #     form = SaleForm(initial={'product': product, 'quantity': 1, 'sale_price': product.selling_price})
    #         return render(request, 'shahzodspace/sell_product.html', {'form': form, 'product': product})