from django.template import Context, Template


def test_static_absolute(rf):
    template = Template(
        '{% load static_absolute from directory_components_tags %}'
        '{% static_absolute "directory_components/images/favicon.ico" %}'
    )

    context = Context({'request': rf.get('/')})
    html = template.render(context)

    assert html == (
        'http://testserver/static/directory_components/images/favicon.ico'
    )
