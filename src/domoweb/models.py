from django.db import models

class Parameter(models.Model):
    key = models.CharField(max_length=30, primary_key=True)
    value = models.CharField(max_length=255)
    
class Widget(models.Model):
    id = models.CharField(max_length=50, primary_key=True)
    
class PageIcon(models.Model):
    id = models.CharField(max_length=50, primary_key=True)
    iconset_id = models.CharField(max_length=50)
    iconset_name = models.CharField(max_length=50)
    icon_id = models.CharField(max_length=50)
    label = models.CharField(max_length=50)

class WidgetInstance(models.Model):
    id = models.AutoField(primary_key=True)
    page_id = models.IntegerField()
    order = models.IntegerField()
    widget_id = models.CharField(max_length=50)
    feature_id = models.IntegerField()

class Page(models.Model):
    id = models.IntegerField(primary_key=True)
    theme_id = models.CharField(max_length=50, null=True, blank=True)
    
class PageTheme(models.Model):
    id = models.CharField(max_length=50, primary_key=True)
    label = models.CharField(max_length=50)

class GraphEngine(models.Model):
    id = models.CharField(max_length=50, primary_key=True)
    label = models.CharField(max_length=50)

class GraphEngineCSS(models.Model):
    id = models.AutoField(primary_key=True)
    graphengine = models.ForeignKey(GraphEngine)
    src = models.CharField(max_length=255)
    media = models.CharField(max_length=50)

class GraphEngineJS(models.Model):
    id = models.AutoField(primary_key=True)
    graphengine = models.ForeignKey(GraphEngine)
    src = models.CharField(max_length=255)
