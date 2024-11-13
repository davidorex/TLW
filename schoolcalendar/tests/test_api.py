from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .factories import PeriodTemplateFactory

class PeriodTemplateAPITests(APITestCase):
    def setUp(self):
        self.template = PeriodTemplateFactory()

    def test_list_period_templates(self):
        url = reverse('periodtemplate-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 1)

    def test_create_period_template(self):
        url = reverse('periodtemplate-list')
        data = {
            'name': 'New Template',
            'schedule_type': 'STD',
            'effective_from': '2024-01-01',
            'morning_periods': 3,
            'afternoon_periods': 2,
            'evening_periods': 1,
            'period_length': 45,
            'passing_time': 5,
            'first_period': '08:00',
            'is_default': False,
            'version': 1
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_update_period_template(self):
        url = reverse('periodtemplate-detail', args=[self.template.id])
        data = {'name': 'Updated Template'}
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Updated Template')

    def test_delete_period_template(self):
        url = reverse('periodtemplate-detail', args=[self.template.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
