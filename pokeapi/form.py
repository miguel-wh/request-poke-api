from django import forms

class FormLimit(forms.Form):
	limit = forms.IntegerField(min_value=1, max_value=20)
	
 
