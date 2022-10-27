from django import forms

from decimal import Decimal


class PaymentForm(forms.Form):
    error_css_class = 'error'

    order_sum = forms.DecimalField(max_digits=5, widget=forms.NumberInput(attrs={
        'class': "input",
        'placeholder': 'Введите сумму',
        'autocomplete': 'off'
    }))

    def is_valid(self):
        order_sum = str(self.data['order_sum']).replace(',', '.')
        if Decimal(order_sum) < Decimal(500):
            self.add_error('order_sum', 'Сумма должна превышать 500 рублей')
        return self.is_bound and not self.errors
