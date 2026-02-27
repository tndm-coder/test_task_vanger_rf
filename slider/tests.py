from django.test import TestCase
from django.urls import reverse


class SliderPageTests(TestCase):
    def test_empty_slider_state_is_rendered(self):
        response = self.client.get(reverse("slider:page"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Слайды пока не добавлены")
