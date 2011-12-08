from django import forms
from django.utils.safestring import mark_safe
from django.conf import settings
from django.core.urlresolvers import reverse

date_map = {'%Y':'yy', '%m':'mm','%d':'dd'}

def date_mapper(date):
    date_parts = str(date).split('-')   
    post = [date_map[date_part] for date_part in date_parts]
    return "-".join(post)


class JQueryWidget:
    class Media:
        js = (
            settings.STATIC_URL + 'js/jquery.js',
            settings.STATIC_URL + 'js/jquery-ui.js',
        )
        css = {
            'all': settings.STATIC_URL + 'css/theme/jquery-ui.css',
        }
    def merge_media(self):
        self._media.js = list(self._media.js)

class DatePicker(forms.DateInput, JQueryWidget):
    def __init__(self, *args, **kwargs):
        if 'jq_attrs' in kwargs:
            self.jq_attrs = kwargs['jq_attrs']
            del kwargs['jq_attrs']
        else:
            self.jq_attrs = None
        super(DatePicker, self).__init__(*args, **kwargs)
    
    
    def render(self, name, value, attrs=None):
        rendered = super(DatePicker, self).render(name, value, attrs)
        #defaults = {'changeYear: "true", yearRange: "1920:2020",'}
        
        if self.jq_attrs:
            js_string = []
            for key in self.jq_attrs:
                js_string.append("%s: '%s'" % (key, self.jq_attrs[key]))
            js_string = ',' + ','.join(js_string)
        else:
            js_string = ''
        
        return rendered + mark_safe(u'''<script type="text/javascript">jQuery(function (){
                jQuery('#id_%(name)s').datepicker({ dateFormat: '%(format)s' %(js_string)s});
            });</script>''' % {'name' : name, 'format': date_mapper(self.format), 'js_string': js_string})


class TimePicker(forms.TimeInput, JQueryWidget):
    class Media:
        js = ( settings.STATIC_URL + 'js/ui.timepickr.js' )
        css = { 'all': settings.STATIC_URL + 'css/ui.timepickr.css' }
        
    _defaults = {
        'convention':12
        }
    
    def __init__(self, *args, **kwargs):
        self.js_options = self._defaults.copy()
        if 'jq_attrs' in kwargs:
            self.js_options.update(kwargs['jq_attrs'])
            del kwargs['jq_attrs']
        sup = super(TimePicker, self)
        sup.__init__(*args, **kwargs)
        self._media.js = list(self._media.js).append(list(sup.Media.js))
        self.media.css
        
    
    def render(self, name, value, attrs=None):
        rendered = super(DatePicker, self).render(name, value, attrs)
        js_options = ',' + ','.join(["%s: %s" % (key, ("'"+val+"'" if isinstance(val, basestring) else val)) 
                                     for key, val in self.js_options.iteritems()])
        
        return rendered + mark_safe(
        u'''<script type="text/javascript">$('#id_%(name)s').timepickr({%(js_options)s});</script>''' % {
                'name' : name,
                'js_options': js_options,
            })
        
class SplitDateTimeWidget(forms.SplitDateTimeWidget):
    def __init__(self, attrs=None, date_format=None, time_format=None):
        widgets = (DatePicker(attrs=attrs, format=date_format),
                   TimePicker(attrs=attrs, format=time_format))
        super(forms.SplitDateTimeWidget, self).__init__(widgets, attrs)