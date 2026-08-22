from django import forms

class TransferForm(forms.Form):
    reciever = forms.IntegerField(label="Reciever Account Number")
    amount = forms.DecimalField(label="Amount", max_digits=12, decimal_places=2, min_value=0.01)  
