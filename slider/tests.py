from types import SimpleNamespace
from unittest.mock import Mock, patch

from django.test import RequestFactory, SimpleTestCase, TestCase
from django.urls import reverse

from .admin import SliderItemAdmin
from .models import SliderItem
from .views import slider_page


class SliderModelTests(SimpleTestCase):
    def test_model_meta_and_str(self):
        field_title = SliderItem._meta.get_field("title")
        field_image = SliderItem._meta.get_field("image")
        field_order = SliderItem._meta.get_field("order")

        self.assertEqual(field_title.verbose_name, "Название")
        self.assertEqual(field_image.verbose_name, "Изображение")
        self.assertEqual(field_order.verbose_name, "Порядок")
        self.assertEqual(SliderItem._meta.verbose_name, "Элемент слайдера")
        self.assertEqual(SliderItem._meta.verbose_name_plural, "Элементы слайдера")
        self.assertEqual(SliderItem._meta.ordering, ["order", "id"])

        item = SliderItem(title="Пример")
        self.assertEqual(str(item), "Пример")


class SliderAdminTests(SimpleTestCase):
    def setUp(self):
        self.admin_site = Mock()
        self.admin_instance = SliderItemAdmin(SliderItem, self.admin_site)

    def test_admin_list_configuration(self):
        self.assertEqual(self.admin_instance.list_display, ("thumbnail", "title", "order"))
        self.assertEqual(self.admin_instance.list_display_links, ("thumbnail", "title"))
        self.assertEqual(self.admin_instance.search_fields, ("title",))
        self.assertEqual(self.admin_instance.ordering, ("order", "id"))

    def test_thumbnail_returns_dash_without_image(self):
        obj = SimpleNamespace(image=None, title="Без фото")
        self.assertEqual(self.admin_instance.thumbnail(obj), "—")


    def test_thumbnail_returns_dash_when_image_url_is_invalid(self):
        class BrokenImage:
            @property
            def url(self):
                raise ValueError("bad image")

        obj = SimpleNamespace(image=BrokenImage(), title="Битое")
        self.assertEqual(self.admin_instance.thumbnail(obj), "—")
    def test_thumbnail_renders_image_tag(self):
        obj = SimpleNamespace(image=SimpleNamespace(url="/media/demo.jpg"), title="Демо")

        html = self.admin_instance.thumbnail(obj)

        self.assertIn('<img src="/media/demo.jpg"', html)
        self.assertIn('alt="Демо"', html)


class SliderPageTests(TestCase):
    def test_empty_slider_state_is_rendered(self):
        response = self.client.get(reverse("slider:page"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Слайды пока не добавлены")


    def test_slider_page_skips_invalid_image_urls(self):
        request = RequestFactory().get("/")

        class BrokenImage:
            @property
            def url(self):
                raise ValueError("broken")

        valid = SimpleNamespace(title="Ок", image=SimpleNamespace(url="/media/ok.jpg"))
        invalid = SimpleNamespace(title="Bad", image=BrokenImage())

        with patch("slider.views.SliderItem.objects") as manager:
            manager.select_related.return_value.order_by.return_value = [valid, invalid]
            response = slider_page(request)

        html = response.content.decode("utf-8")
        self.assertIn("Ок", html)
        self.assertNotIn("Bad", html)
        self.assertIn('href="/media/ok.jpg"', html)
    def test_slider_page_uses_ordering_and_renders_slides(self):
        request = RequestFactory().get("/")

        item_1 = SimpleNamespace(title="Первый", image=SimpleNamespace(url="/media/1.jpg"))
        item_2 = SimpleNamespace(title="Второй", image=SimpleNamespace(url="/media/2.jpg"))
        mocked_qs = [item_1, item_2]

        with patch("slider.views.SliderItem.objects") as manager:
            manager.select_related.return_value.order_by.return_value = mocked_qs
            response = slider_page(request)

        manager.select_related.assert_called_once_with("image")
        manager.select_related.return_value.order_by.assert_called_once_with("order", "id")

        html = response.content.decode("utf-8")
        self.assertIn("Первый", html)
        self.assertIn("Второй", html)
        self.assertIn('data-index="0"', html)
        self.assertIn('data-index="1"', html)
        self.assertIn('href="/media/1.jpg"', html)
        self.assertIn('href="/media/2.jpg"', html)
