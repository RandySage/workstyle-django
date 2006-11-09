from django.template import Node, Library
from WorkStyle.workstyle.models import Status, Tag

register = Library()

class StatusListNode(Node):
    def __init__(self, variable):
        self.variable = variable

    def render(self, context):
        context[self.variable] = Status.objects.all().order_by('id')
        return ''

class TagListNode(Node):
    def __init__(self, variable):
        self.variable = variable

    def render(self, context):
        context[self.variable] = Tag.objects.all().order_by('tag_type', 'name')
        return ''

def do_get_status_list(parser, token):
    """
    {% get_status_list as status_list %}
    """
    bits = token.contents.split()
    if len(bits) != 3:
        raise template.TemplateSyntaxError, "'%s' tag takes two arguments" % bits[0]
    if bits[1] != "as":
        raise template.TemplateSyntaxError, "First argument to '%s' tag must be 'as'" % bits[0]
    return StatusListNode(bits[2])
register.tag('get_status_list', do_get_status_list)

def do_get_tag_list(parser, token):
    """
    {% get_tag_list as tag_list %}
    """
    bits = token.contents.split()
    if len(bits) != 3:
        raise template.TemplateSyntaxError, "'%s' tag takes two arguments" % bits[0]
    if bits[1] != "as":
        raise template.TemplateSyntaxError, "First argument to '%s' tag must be 'as'" % bits[0]
    return TagListNode(bits[2])
register.tag('get_tag_list', do_get_tag_list)

