from django import forms

class PCSpecsForm(forms.Form):
    cpu = forms.CharField(label='CPU', max_length=100)
    gpu = forms.CharField(label='GPU', max_length=100)
    ram = forms.FloatField(label='RAM (GB)')
    storage = forms.FloatField(label='Storage (GB)')
    os_version = forms.CharField(label='OS Version', max_length=100)