from directory_components.widgets import CheckboxWithInlineLabel
from directory_components.widgets import CheckboxSelectInlineLabelMultiple
from bs4 import BeautifulSoup


def test_checkbox_inline_label_widget():
    widget = CheckboxWithInlineLabel(
        label='Box label',
        help_text='Help text',
        attrs={
            'id': 'checkbox_id',
            'class': 'test-class'
        }
    )
    html = widget.render('name', 'value')
    soup = BeautifulSoup(html, 'html.parser')

    assert '<label ' in html
    assert '<span ' in html

    label = soup.find('label')
    assert label['for'] == 'checkbox_id'

    label_text = soup.select('span.form-label')[0]
    assert label_text.string == 'Box label'

    help_text = soup.select('span.form-hint')[0]
    assert help_text.string == 'Help text'


def test_checkbox_inline_label_multiple_widget():
    widget = CheckboxSelectInlineLabelMultiple()
    html = widget.render('name', 'value')
    assert '<ul ' in html
