# -*- encoding: utf-8 -*-

# Python imports
# Django imports

# Third part imports
from crispy_forms.layout import Field
from crispy_forms.utils import TEMPLATE_PACK

# Project imports


class PrependedIconText(Field):
    template = "fields/prepend_text_with_icon.html"
    icon_class = "fa fa-user"

    def __init__(self, *args, **kwargs):
        if not hasattr(self, 'attrs'):
            self.attrs = {}
        if 'icon_class' in kwargs:
            self.icon_class = kwargs.pop('icon_class')
        super(PrependedIconText, self).__init__(*args, **kwargs)

    def render(self, form, form_style, context, template_pack=TEMPLATE_PACK):
        if hasattr(self, 'icon_class'):
            context['icon_class'] = self.icon_class
        return super(PrependedIconText, self).render(form, form_style, context, template_pack=template_pack)


class CustomCheckbox(Field):
    template = "fields/custom_checkbox.html"
    type_checkbox = "checkbox-primary"

    def __init__(self, *args, **kwargs):
        if not hasattr(self, 'attrs'):
            self.attrs = {}
        if 'type_checkbox' in kwargs:
            self.type_checkbox = kwargs.pop('type_checkbox')
        super(CustomCheckbox, self).__init__(*args, **kwargs)

    def render(self, form, form_style, context, template_pack=TEMPLATE_PACK):
        if hasattr(self, 'type_checkbox'):
            context['type_checkbox'] = self.type_checkbox
        return super(CustomCheckbox, self).render(form, form_style, context, template_pack=template_pack)