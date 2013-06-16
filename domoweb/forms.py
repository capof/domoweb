#!/usr/bin/env python
import json
import itertools
from django.utils.translation import ugettext as _
from itertools import groupby
from django import forms
from django.core.exceptions import ObjectDoesNotExist
from django.core.validators import *
from collections import OrderedDict
from domoweb import fields
from domoweb.models import PageIcon, PageTheme, WidgetOption, WidgetInstanceOption, WidgetSensor, WidgetInstanceSensor, Sensor, WidgetCommand, WidgetInstanceCommand, Command, WidgetDevice, WidgetInstanceDevice, Device
   
# Page configuration form
class PageForm(forms.Form):
    name = forms.CharField(max_length=50, label=_("Page name"), widget=forms.TextInput(attrs={'class':'icon32-form-tag'}), required=True)
    description = forms.CharField(label=_("Page description"), widget=forms.Textarea(attrs={'class':'icon32-form-edit'}), required=False)
    icon = fields.IconChoiceField(label=_("Choose the icon"), required=False, empty_label="No icon", queryset=PageIcon.objects.all())
    theme = forms.ModelChoiceField(label=_("Choose a theme"), required=False, empty_label="No theme", queryset=PageTheme.objects.all())

class GroupedModelChoiceField(forms.ModelChoiceField):
    def __init__(self, queryset, group_by_field, group_label=None, *args, **kwargs):
        """
        group_by_field is the name of a field on the model
        group_label is a function to return a label for each choice group
        """
        super(GroupedModelChoiceField, self).__init__(queryset, *args, **kwargs)
        self.group_by_field = group_by_field
        if group_label is None:
            self.group_label = lambda group: group.name
        else:
            self.group_label = group_label
    
    def _get_choices(self):
        """
        Exactly as per ModelChoiceField except returns new iterator class
        """
        if hasattr(self, '_choices'):
            return self._choices
        return GroupedModelChoiceIterator(self)
    choices = property(_get_choices, forms.ModelChoiceField._set_choices)

class GroupedModelChoiceIterator(forms.models.ModelChoiceIterator):
    def __iter__(self):
        if self.field.empty_label is not None:
            yield (u"", self.field.empty_label)
        if self.field.cache_choices:
            if self.field.choice_cache is None:
                self.field.choice_cache = [
                    (self.field.group_label(group), [self.choice(ch) for ch in choices])
                        for group,choices in groupby(self.queryset.all(),
                            key=lambda row: getattr(row, self.field.group_by_field))
                ]
            for choice in self.field.choice_cache:
                yield choice
        else:
            for group, choices in groupby(self.queryset.all(),
                    key=lambda row: getattr(row, self.field.group_by_field)):
                yield (self.field.group_label(group), [self.choice(ch) for ch in choices])

class MaskInput(forms.TextInput):
    def __init__(self, mask, *args, **kwargs):
#        mask = kwargs.pop('mask', {})
        super(MaskInput, self).__init__(*args, **kwargs)
        self.mask = mask

    def render(self, name, value, attrs=None):
        attrs['class'] = 'mask '
        attrs['mask'] = self.mask
        return super(MaskInput, self).render(name, value, attrs=attrs)
    
class ParametersForm(forms.Form):
    def __init__(self, *args, **kwargs):
        # This should be done before any references to self.fields
        super(ParametersForm, self).__init__(*args, **kwargs)

    """def clean(self):
        cleaned_data = super(ParametersForm, self).clean()
        
        return cleaned_data
    """    
    def setData(self, kwds):
        """Set the data to include in the form"""
        for name,field in self.fields.items():
            self.data[name] = field.widget.value_from_datadict(
                kwds, self.files, self.add_prefix(name))
        self.is_bound = True
    
    def validate(self):
        self.full_clean()

#        for name,field in self.fields.items():
#            if 'errors' in field:
#                print name, field.errors

#http://stackoverflow.com/questions/4466499/in-django-how-do-i-change-this-field-is-required-to-name-is-required
#https://gist.github.com/stholmes/3889441

    def addCharField(self, key, label, required, max_length=60, default=None, help_text=None, options=None):
        validators=[]
        widget=forms.TextInput
        if options:
            if "min_length" in options:
                validators.append(MinLengthValidator(options["min_length"]))
            if "max_length" in options:
                validators.append(MaxLengthValidator(options["max_length"]))
            if "multilignes" in options:
                widget=forms.Textarea
            elif "mask" in options: #https://github.com/shaungrady/jquery-mask-input
                widget=MaskInput(options['mask'])
        self.fields[key] = forms.CharField(widget=widget, label=label, required=required, max_length=max_length, initial=default, help_text=help_text, validators=validators)

    def addBooleanField(self, key, label, default=None, help_text=None):
        self.fields[key] = forms.BooleanField(label=label, required=False, initial=default, help_text=help_text)

    def addGroupedModelChoiceField(self, key, label, queryset, group_by_field, empty_label, required, default=None, help_text=None):
        self.fields[key] = GroupedModelChoiceField(label=label, required=required, queryset=queryset, group_by_field=group_by_field, empty_label=empty_label, initial=default, help_text=help_text)

    def addChoiceField(self, key, label, required, default=None, help_text=None, options=None, empty_label=None):
        choices = [('', '--Select Parameter--')]
        if options:
            if "choices" in options:
                ordered = OrderedDict(sorted(options["choices"].items()))
                for v, l in ordered.iteritems():
                    choices.append((v, l))
        self.fields[key] = forms.ChoiceField(label=label, required=required, choices=choices, initial=default, help_text=help_text)

    def addMultipleChoiceField(self, key, label, required, default=None, help_text=None, options=None, empty_label=None):
        import collections
        choices = []
        if options:
            if "choices" in options:
                ordered = OrderedDict(sorted(options["choices"].items()))
                for v, l in ordered.iteritems():
                    choices.append((v, l))
        self.fields[key] = forms.MultipleChoiceField(label=label, required=required, choices=choices, initial=default, help_text=help_text)

    def addDateField(self, key, label, required, default=None, help_text=None):
        self.fields[key] = forms.DateField(label=label, required=required, initial=default, help_text=help_text, input_formats=['%d/%m/%Y'])

    def addTimeField(self, key, label, required, default=None, help_text=None):
        self.fields[key] = forms.TimeField(label=label, required=required, initial=default, help_text=help_text, input_formats=['%H:%M:%S'])

    def addDateTimeField(self, key, label, required, default=None, help_text=None):
        self.fields[key] = forms.DateTimeField(label=label, required=required, initial=default, help_text=help_text, input_formats=['%Y-%m-%d %H:%M:%S'])

    def addFloatField(self, key, label, required, default=None, help_text=None, options=None):
        validators=[]
        if options:
            if "min_value" in options:
                validators.append(MinValueValidator(options["min_value"]))
            if "max_value" in options:
                validators.append(MaxValueValidator(options["max_value"]))

        self.fields[key] = forms.FloatField(label=label, required=required, initial=default, help_text=help_text, validators=validators)

    def addIntegerField(self, key, label, required, default=None, help_text=None, options=None):
        validators=[]
        if options:
            if "min_value" in options:
                validators.append(MinValueValidator(options["min_value"]))
            if "max_value" in options:
                validators.append(MaxValueValidator(options["max_value"]))

        self.fields[key] = forms.IntegerField(label=label, required=required, initial=default, help_text=help_text, validators=validators)

    def addEmailField(self, key, label, required, default=None, help_text=None, options=None):
        validators=[]
        if options:
            if "min_length" in options:
                validators.append(MinLengthValidator(options["min_length"]))
            if "max_length" in options:
                validators.append(MaxLengthValidator(options["max_length"]))
        self.fields[key] = forms.EmailField(label=label, required=required, initial=default, help_text=help_text, validators=validators)

    def addURLField(self, key, label, required, default=None, help_text=None, options=None):
        validators=[]
        if options:
            if "min_length" in options:
                validators.append(MinLengthValidator(options["min_length"]))
            if "max_length" in options:
                validators.append(MaxLengthValidator(options["max_length"]))
        self.fields[key] = forms.URLField(label=label, required=required, initial=default, help_text=help_text, validators=validators)

    def addIPv4Field(self, key, label, required, default=None, help_text=None):
        self.fields[key] = forms.IPAddressField(label=label, required=required, initial=default, help_text=help_text)

class WidgetOptionsForm(ParametersForm):
    def __init__(self, *args, **kwargs):
        # This should be done before any references to self.fields
        super(WidgetOptionsForm, self).__init__(*args, **kwargs)
        self.to_update = {}
        self.to_create = {}

    def addField(self, parameter, wio=None, tmpid=None):
        default = None
        options = json.loads(parameter.options)
        if wio is None :
            key = ('optionparam_%s_%s' % (tmpid, parameter.id))
            value = parameter.default
            self.to_create[key] = parameter
        else:
            key = ('optionparam_%s' % (wio.id))
            value = wio.value
            self.to_update[key] = wio

        if parameter.type == 'boolean':
            if not value == '':
                default = (value == 'true' or value == 'True')
            self.addBooleanField(key=key, label=parameter.name, default=default, help_text=parameter.description)
        elif parameter.type == 'string':
            if not value == '':
                default = value
            self.addCharField(key=key, label=parameter.name, required=parameter.required, default=default, help_text=parameter.description, options=options)
        elif parameter.type == 'choice':
            if not value == '':
                default = value
            self.addChoiceField(key=key, label=parameter.name, required=parameter.required, default=default, help_text=parameter.description, options=options)
        elif parameter.type == 'multiplechoice':
            if not value == '':
                default = value
            self.addMultipleChoiceField(key=key, label=parameter.name, required=parameter.required, default=default, help_text=parameter.description, options=options)
        elif parameter.type == 'date':
            if not value == '':
                default = value
            self.addDateField(key=key, label=parameter.name, required=parameter.required, default=default, help_text=parameter.description)
        elif parameter.type == 'time':
            if not value == '':
                default = value
            self.addTimeField(key=key, label=parameter.name, required=parameter.required, default=default, help_text=parameter.description)
        elif parameter.type == 'datetime':
            if not value == '':
                default = value
            self.addDateTimeField(key=key, label=parameter.name, required=parameter.required, default=default, help_text=parameter.description)
        elif parameter.type == 'float':
            if not value == '':
                default = value
            self.addFloatField(key=key, label=parameter.name, required=parameter.required, default=default, help_text=parameter.description, options=options)
        elif parameter.type == 'integer':
            if not value == '':
                default = value
            self.addIntegerField(key=key, label=parameter.name, required=parameter.required, default=default, help_text=parameter.description, options=options)
        elif parameter.type == 'email':
            if not value == '':
                default = value
            self.addEmailField(key=key, label=parameter.name, required=parameter.required, default=default, help_text=parameter.description, options=options)
        elif parameter.type == 'ipv4':
            if not value == '':
                default = value
            self.addIPv4Field(key=key, label=parameter.name, required=parameter.required, default=default, help_text=parameter.description)
        elif parameter.type == 'url':
            if not value == '':
                default = value
            self.addURLField(key=key, label=parameter.name, required=parameter.required, default=default, help_text=parameter.description, options=options)

        else:
            if not value == '':
                default = value
            self.addCharField(key=key, label=parameter.name, required=parameter.required, default=default, help_text=parameter.description, options=options)

    def save(self, instance):
        try:
            for field, parameter in self.to_create.iteritems():
                wio = WidgetInstanceOption(instance=instance, parameter=parameter, value=self.cleaned_data[field])
                wio.save()
            for field, wio in self.to_update.iteritems():
                wio.value=self.cleaned_data[field]
                wio.save()
        except KeyError: #Did not pass validation
            pass

class WidgetSensorsForm(ParametersForm):
    def __init__(self, *args, **kwargs):
        # This should be done before any references to self.fields
        super(WidgetSensorsForm, self).__init__(*args, **kwargs)
        self.to_update = {}
        self.to_create = {}

    def addField(self, parameter, wis=None, tmpid=None):
        if wis is None :
            key = ('sensorparam_%s_%s' % (tmpid, parameter.id))
            default = None
            self.to_create[key] = parameter
        else:
            key = ('sensorparam_%s' % (wis.id))
            default = wis.sensor
            self.to_update[key] = wis

        sensors = Sensor.objects.filter(datatype_id__in = parameter.types_as_list)
        self.addGroupedModelChoiceField(key=key, label=parameter.name, required=parameter.required, default=default, queryset=sensors, group_by_field='device', empty_label=_("--Select Sensor--"), help_text=parameter.description)

    def save(self, instance):
        try:
            for field, parameter in self.to_create.iteritems():
                wis = WidgetInstanceSensor(instance=instance, parameter=parameter, sensor=self.cleaned_data[field])
                wis.save()
            for field, wis in self.to_update.iteritems():
                wis.sensor=self.cleaned_data[field]
                wis.save()
        except KeyError: #Did not pass validation
            pass

class WidgetCommandsForm(ParametersForm):
    def __init__(self, *args, **kwargs):
        # This should be done before any references to self.fields
        super(WidgetCommandsForm, self).__init__(*args, **kwargs)
        self.to_update = {}
        self.to_create = {}

    def addField(self, parameter, wic=None, tmpid=None):
        if wic is None :
            key = ('commandparam_%s_%s' % (tmpid, parameter.id))
            default = None
            self.to_create[key] = parameter
        else:
            key = ('commandparam_%s' % (wic.id))
            default = wic.command
            self.to_update[key] = wic

        datatypes = []
        types = json.loads(parameter.types)
        for type in types:
            for p in itertools.permutations(type):            
                datatypes.append(''.join(p))
        commands = Command.objects.filter(datatypes__in = datatypes)
        self.addGroupedModelChoiceField(key=key, label=parameter.name, required=parameter.required, default=default, queryset=commands, group_by_field='device', empty_label=_("--Select Command--"), help_text=parameter.description)

    def save(self, instance):
        try:
            for field, parameter in self.to_create.iteritems():
                wic = WidgetInstanceCommand(instance=instance, parameter=parameter, command=self.cleaned_data[field])
                wic.save()
            for field, wic in self.to_update.iteritems():
                wic.command=self.cleaned_data[field]
                wic.save()
        except KeyError: #Did not pass validation
            pass

class WidgetDevicesForm(ParametersForm):
    def __init__(self, *args, **kwargs):
        # This should be done before any references to self.fields
        super(WidgetDevicesForm, self).__init__(*args, **kwargs)
        self.to_update = {}
        self.to_create = {}

    def addField(self, parameter, wid=None, tmpid=None):
        if wid is None :
            key = ('deviceparam_%s_%s' % (tmpid, parameter.id))
            default = None
            self.to_create[key] = parameter
        else:
            key = ('deviceparam_%s' % (wid.id))
            default = wid.device
            self.to_update[key] = wid

        devices = Device.objects.filter(type__in = parameter.types_as_list)
        self.addGroupedModelChoiceField(key=key, label=parameter.name, required=parameter.required, default=default, queryset=devices, group_by_field='type', empty_label=_("--Select Device--"), help_text=parameter.description)

    def save(self, instance):
        try:
            for field, parameter in self.to_create.iteritems():
                wid = WidgetInstanceDevice(instance=instance, parameter=parameter, device=self.cleaned_data[field])
                wid.save()
            for field, wid in self.to_update.iteritems():
                wid.device=self.cleaned_data[field]
                wid.save()
        except KeyError: #Did not pass validation
            pass
        
class WidgetInstanceForms(object):
    def __init__(self, widget, instance=None, tmpid=None):
        self.optionsform = WidgetOptionsForm()
        self.sensorsform = WidgetSensorsForm()
        self.commandsform = WidgetCommandsForm()
        self.devicesform = WidgetDevicesForm()
        widgetoptions = WidgetOption.objects.filter(widget=widget)
        widgetsensors = WidgetSensor.objects.filter(widget=widget)    
        widgetcommands = WidgetCommand.objects.filter(widget=widget)    
        widgetdevices = WidgetDevice.objects.filter(widget=widget)    

        if instance:
            for parameter in widgetoptions:
                try:
                    wio = WidgetInstanceOption.objects.get(instance=instance, parameter=parameter)
                except ObjectDoesNotExist:
                    self.optionsform.addField(parameter=parameter, tmpid=instance.id)
                else:
                    self.optionsform.addField(parameter=parameter, wio=wio)
            for parameter in widgetsensors:
                try:
                    wis = WidgetInstanceSensor.objects.get(instance=instance, parameter=parameter)
                except ObjectDoesNotExist:
                    self.sensorsform.addField(parameter=parameter, tmpid=instance.id)
                else:
                    self.sensorsform.addField(parameter=parameter, wis=wis)
            for parameter in widgetcommands:
                try:
                    wic = WidgetInstanceCommand.objects.get(instance=instance, parameter=parameter)
                except ObjectDoesNotExist:
                    self.commandsform.addField(parameter=parameter, tmpid=instance.id)
                else:
                    self.commandsform.addField(parameter=parameter, wic=wic)
            for parameter in widgetdevices:
                try:
                    wid = WidgetInstanceDevice.objects.get(instance=instance, parameter=parameter)
                except ObjectDoesNotExist:
                    self.devicesform.addField(parameter=parameter, tmpid=instance.id)
                else:
                    self.devicesform.addField(parameter=parameter, wid=wid)
            
        else:
            for parameter in widgetoptions:
                self.optionsform.addField(parameter=parameter, tmpid=tmpid)
            for parameter in widgetsensors:
                self.sensorsform.addField(parameter=parameter, tmpid=tmpid)
            for parameter in widgetcommands:
                self.commandsform.addField(parameter=parameter, tmpid=tmpid)
            for parameter in widgetdevices:
                self.devicesform.addField(parameter=parameter, tmpid=tmpid)

    def setData(self, kwds):
        self.optionsform.setData(kwds)
        self.sensorsform.setData(kwds)
        self.commandsform.setData(kwds)
        self.devicesform.setData(kwds)

    def validate(self):
        self.optionsform.validate()
        self.sensorsform.validate()
        self.commandsform.validate()
        self.devicesform.validate()
        """
        print "options", self.optionsform.is_valid()
        for field, errors in self.optionsform.errors.items():
            print field
            for error in errors:
                print error
        print "sensors", self.sensorsform.is_valid()
        for field, errors in self.sensorsform.errors.items():
            print field
            for error in errors:
                print error
        """

    def is_valid(self):
        return self.optionsform.is_valid() and self.sensorsform.is_valid() and self.commandsform.is_valid() and self.devicesform.is_valid()
    
    def save(self, instance):    
        self.validate()
        self.optionsform.save(instance)
        self.sensorsform.save(instance)
        self.commandsform.save(instance)
        self.devicesform.save(instance)

        return self.is_valid()
 