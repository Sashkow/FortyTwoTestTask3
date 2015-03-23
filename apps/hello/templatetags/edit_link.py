"""
tag that accepts any object and renders the link to its admin edit page
"""
from django import template
from django.core.urlresolvers import reverse

register = template.Library()

def do_edit_link(parser, token):
    """
    compile funcion for edit_link tag 
    """
    try:
        # split_contents() knows not to split quoted strings.
        tag_name, object_string = token.split_contents()

    except ValueError:
        raise template.TemplateSyntaxError("%r tag requires a single argument" % token.contents.split()[0])
    # if not (format_string[0] == format_string[-1] and format_string[0] in ('"', "'")):
    #     raise template.TemplateSyntaxError("%r tag's argument should be in quotes" % tag_name)
    return EditLinkNode(object_string)


class EditLinkNode(template.Node):
    def __init__(self, object_string):
        self.object_variable = template.Variable(object_string)
    def render(self, context):
        try:
            actual_object = self.object_variable.resolve(context)

            # by analogy to  {% url 'admin:polls_choice_change' choice.id %}
            app = actual_object._meta.app_label
            model = actual_object._meta.module_name
            pk = actual_object.pk
            url = reverse("admin:%s_%s_change" % (app, model),args=[pk]) 
            link ='<a href="%s">(admin)</a>' % url
            return link
        except template.VariableDoesNotExist:
            return ''

register.tag('edit_link', do_edit_link)
