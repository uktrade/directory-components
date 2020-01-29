from django.http import HttpRequest, HttpResponse

from directory_components.decorators import skip_ga360


@skip_ga360
def test_function(request, *args, **kwargs):
    return HttpResponse()


def test_skip_360_adds_attribute_to_response():
    request = HttpRequest()
    response = test_function(request)

    assert request.skip_ga360 is True
