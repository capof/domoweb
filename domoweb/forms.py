#!/usr/bin/env python
from django import forms

class ParametersForm(forms.Form):
    def __init__(self, *args, **kwargs):
        # This should be done before any references to self.fields
        super(ParametersForm, self).__init__(*args, **kwargs)

    def setData(self, kwds):
        """Set the data to include in the form"""
        for name,field in self.fields.items():
            self.data[name] = field.widget.value_from_datadict(
                kwds, self.files, self.add_prefix(name))
        self.is_bound = True
    
    def validate(self): self.full_clean()
    
    def addCharField(self, key, label, required=False, max_length=50, default=None):
        self.fields[key] = forms.CharField(label=label, required=required, max_length=max_length, default=default)

    def addBooleanField(self, key, label, default=None):
        self.fields[key] = forms.BooleanField(label=label, required=False, initial=default)

    def addField(self, parameter, value=None):
        default = None
        if value is None :
            value = parameter.default
        if parameter.type == 'boolean':
            if not value == '':
                default = (value == 'true' or value == 'True')
            self.addBooleanField(key=parameter.key, label=parameter.name, default=default)
        else:
            if not value == '':
                default = value
            self.addCharField(key=parameter.key, label=parameter.name, default=default)