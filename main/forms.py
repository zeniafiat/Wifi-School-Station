from django import forms

class sencorIDform(forms.Form):
    sensor_id = forms.IntegerField()