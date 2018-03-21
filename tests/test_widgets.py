from directory_components.widgets import CheckboxWithInlineLabel
from directory_components.widgets import CheckboxSelectInlineLabelMultiple
from directory_components.widgets import RadioSelect
from directory_components.widgets import ChoiceWidget
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


def test_radio_select_widget():
    TEST_CHOICES = (
        ('cyan', 'Cyan'),
        ('magenta', 'Magenta'),
        ('yellow', 'Yellow'),
    )
    widget = RadioSelect(
        attrs={'id': 'radio-test'},
        choices=TEST_CHOICES
    )
    html = widget.render('name', 'value')
    soup = BeautifulSoup(html, 'html.parser')

    assert '<label ' in html
    assert '<ul ' in html

    list_element = soup.find('ul')
    assert list_element['id'] == 'radio-test'

    list_items = soup.find_all('input')
    exp_ids = [
        'radio-test-cyan',
        'radio-test-magenta',
        'radio-test-yellow',
    ]
    for item, exp_id in zip(list_items, exp_ids):
        assert item.attrs['id'] == exp_id


def test_radio_select_class_has_attrs():
    radio = RadioSelect(
        attrs={'id': 'radio-test'}
    )
    assert radio.input_type == 'radio'
    assert radio.css_class_name == 'select-multiple'
    assert radio.attrs['id'] == 'radio-test'


def test_checkbox_inline_class_has_attrs():
    checkbox = CheckboxWithInlineLabel(
        label='Test label',
        help_text='Test helptext'
    )
    context = checkbox.get_context('name', 'value', attrs=None)
    assert context['label'] == 'Test label'
    assert context['help_text'] == 'Test helptext'


def test_choice_widget_id():
    choice = ChoiceWidget()
    assert choice.id_for_label('id', 'value') == 'id-value'
