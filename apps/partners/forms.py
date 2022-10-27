from django import forms

from decimal import Decimal

from .models import Channel, Payout, PartnerPocket


class ChannelCreateUpdateForm(forms.ModelForm):
    class Meta:
        model = Channel
        fields = ['name']
        widgets = {
            'name': forms.TextInput({
                'class': 'modal_input name',
                'placeholder': 'Введите название канала'
            })
        }


class PayoutCreateForm(forms.ModelForm):
    class Meta:
        model = Payout
        fields = ['amount', 'payment_type', 'payment_address']
        widgets = {
            'amount': forms.NumberInput({
                'class': 'modal_input',
                'placeholder': 'Введите сумму для выплаты'
            }),
            'payment_type': forms.HiddenInput(),
            'payment_address': forms.TextInput({
                'class': 'modal_input inputName',
                'placeholder': 'Введите адрес для выплаты'
            })
        }

    def is_valid(self, partner_pocket: PartnerPocket):
        if Decimal(self.data['amount']) < 500:
            self.add_error('amount', 'Сумма должна превышать 500 рублей')
        elif (partner_pocket.balance - Decimal(self.data['amount'])) < 0:
            self.add_error('amount', 'У вас недостаточно средств на балансе')
        return self.is_bound and not self.errors
