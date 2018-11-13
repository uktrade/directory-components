from django import forms


class DirectoryComponentsFormMixin:

    use_required_attribute = False
    error_css_class = 'form-group-error'

    def as_p(self):
        return self._html_output(
            normal_row=(
                '<p%(html_class_attr)s>%(label)s %(help_text)s %(field)s</p>'
            ),
            error_row='%s',
            row_ender='</p>',
            help_text_html=' <span class="form-hint">%s</span>',
            errors_on_separate_row=True
        )


class Form(DirectoryComponentsFormMixin, forms.Form):
    pass
