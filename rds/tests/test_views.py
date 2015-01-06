from django.test import TestCase
from django.test import Client

from django.core.urlresolvers import reverse

from ..models import Server

class JoinView(TestCase):

    def setUp(self):
        self.c = Client()

    def test_required_fields(self):
        form_data = {}
        response = self.c.post(
            reverse('api_join'),
            data=form_data
            )
        self.assertEqual(response.status_code, 400)

    # def test_join(self):
    #     ip = '10.0.0.1'
    #     name = 'name'
    #     domain = 'domain'
        
    #     form_data = {
    #         'ip': ip,
    #         'name': name,
    #         'domain': domain
    #     }
    #     response = self.c.post(
    #         reverse('api_join'),
    #         data=form_data
    #         )
    #     self.assertEqual(response.status_code, 200)
    #     s = Server.objects.get(ip=ip)

    #     self.assertEquals(s.name, name)
    #     self.assertEquals(s.domain, domain)
