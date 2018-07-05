from django.urls import reverse


def test_robots(client):
    url = reverse('robots')

    response = client.get(url)

    assert response.status_code == 200
    assert response.template_name == ['robots.txt']
