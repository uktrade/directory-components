from django.http import HttpResponse

from directory_components.decorators import skip_ga360


@skip_ga360
def test_function(request, *args, **kwargs):
    return HttpResponse()


def test_skip_360_adds_attribute_to_response():
    response = test_function({})

    assert response.skip_ga360 is True
