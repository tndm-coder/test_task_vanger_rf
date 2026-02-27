from django.db import models
from filer.fields.image import FilerImageField


class SliderItem(models.Model):
    title = models.CharField("Название", max_length=255)
    image = FilerImageField(
        verbose_name="Изображение",
        on_delete=models.PROTECT,
        related_name="slider_items",
    )
    order = models.PositiveIntegerField("Порядок", default=0, db_index=True)

    class Meta:
        ordering = ["order", "id"]
        verbose_name = "Элемент слайдера"
        verbose_name_plural = "Элементы слайдера"

    def __str__(self):
        return self.title
