from __future__ import unicode_literals

import sys

from django.templatetags.i18n import TemplateSyntaxError, Variable, Node, \
    render_value_in_context
from django.template import Library
from django.utils import six

register = Library()


class TranslateNode(Node):
    def __init__(self, filter_expression, noop, asvar=None,
                 message_context=None):
        self.noop = noop
        self.asvar = asvar
        self.message_context = message_context
        self.filter_expression = filter_expression
        if isinstance(self.filter_expression.var, six.string_types):
            self.filter_expression.var = Variable(
                "'%s'" % self.filter_expression.var)
        self.request = Variable('request')

    def render(self, context):
        self.filter_expression.var.translate = not self.noop
        if self.message_context:
            self.filter_expression.var.message_context = (
                self.message_context.resolve(context))
        output = self.filter_expression.resolve(context)
        value = render_value_in_context(output, context)
        # print(self.request.resolve(context).resolver_match.app_name)
        if self.asvar:
            context[self.asvar] = value
            return ''
        else:
            return value


@register.tag("trans")
def do_translate(parser, token):
    """
    This will mark a string for translation and will
    translate the string for the current language.
    Usage::
        {% trans "this is a test" %}
    This will mark the string for translation so it will
    be pulled out by mark-messages.py into the .po files
    and will run the string through the translation engine.
    There is a second form::
        {% trans "this is a test" noop %}
    This will only mark for translation, but will return
    the string unchanged. Use it when you need to store
    values into forms that should be translated later on.
    You can use variables instead of constant strings
    to translate stuff you marked somewhere else::
        {% trans variable %}
    This will just try to translate the contents of
    the variable ``variable``. Make sure that the string
    in there is something that is in the .po file.
    It is possible to store the translated string into a variable::
        {% trans "this is a test" as var %}
        {{ var }}
    Contextual translations are also supported::
        {% trans "this is a test" context "greeting" %}
    This is equivalent to calling pgettext instead of (u)gettext.
    """
    bits = token.split_contents()
    if len(bits) < 2:
        raise TemplateSyntaxError("'%s' takes at least one argument" % bits[0])
    message_string = parser.compile_filter(bits[1])
    remaining = bits[2:]

    noop = False
    asvar = None
    message_context = None
    seen = set()
    invalid_context = {'as', 'noop'}

    while remaining:
        option = remaining.pop(0)
        if option in seen:
            raise TemplateSyntaxError(
                "The '%s' option was specified more than once." % option,
            )
        elif option == 'noop':
            noop = True
        elif option == 'context':
            try:
                value = remaining.pop(0)
            except IndexError:
                msg = "No argument provided to the " \
                    "'%s' tag for the context option." % bits[0]
                six.reraise(
                    TemplateSyntaxError, TemplateSyntaxError(msg),
                    sys.exc_info()[2])
            if value in invalid_context:
                raise TemplateSyntaxError(
                    "Invalid argument '%s' provided to the"
                    " '%s' tag for the context option" % (value, bits[0]),
                )
            message_context = parser.compile_filter(value)
        elif option == 'as':
            try:
                value = remaining.pop(0)
            except IndexError:
                msg = "No argument provided to the '%s' tag for " \
                    "the as option." % bits[0]
                six.reraise(
                    TemplateSyntaxError, TemplateSyntaxError(msg),
                    sys.exc_info()[2])
            asvar = value
        else:
            raise TemplateSyntaxError(
                "Unknown argument for '%s' tag: '%s'. The only options "
                "available are 'noop', 'context' \"xxx\", and 'as VAR'." % (
                    bits[0], option,
                )
            )
        seen.add(option)

    return TranslateNode(message_string, noop, asvar, message_context)
