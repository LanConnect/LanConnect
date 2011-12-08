from django import template
from acheivements.models import Achievement
from sorl.thumbnail.templatetags import thumbnail
from django.contrib.admin.models import LogEntry
register = template.Library()


#this all needs a lot of work!

class _FakeParser(object):
    def __init__(self, real_parser, text):
        self = real_parser
        self.text = text
    def compile_filter(self,*args,**kwargs): real_parser.compile_filter(*args, **kwargs)
    def next_token(self,*args,**kwargs): real_parser.next_token(*args, **kwargs)
    def parse(self, *args):
        nodelist = template.NodeList()
        nodelist.extend(template.compile_string(text, None))
        return nodelist

@register.tag
def acheivement_icons(parser, token):
    try:
        # split_contents() knows not to split quoted strings.
        tag_name, user, size = token.split_contents()
        user = template.Variable(user_var)
        
    except ValueError:
        raise template.TemplateSyntaxError, "%r tag requires a single argument (user)" % token.contents.split()[0]
    return AcheivementIconsNode(user, size)

class AcheivementIconsNode(template.Node):
    def __init__(self, user, parser, token):
        self.token = token
        context[self].parser = parser
        
    def render(self, context):
        user = self.user.resolve(context)
        fake_parser = _FakeParser(context[self].parser, '<img src="{{ im.url }}" width="{{ im.width }}" height="{{ im.height }}">')
        #for image in blah:
        context.push()
        context['image'] = val
        tnode = thumbnail.ThumbnailNode(fake_parser, self.token)
        context.pop()
        return output
