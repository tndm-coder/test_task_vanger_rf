from django.shortcuts import render

from .models import SliderItem


def slider_page(request):
    slider_items = SliderItem.objects.select_related("image").order_by("order", "id")
    slides = []

    for item in slider_items:
        if not item.image:
            continue
        try:
            image_url = item.image.url
        except (AttributeError, ValueError, OSError):
            continue

        slides.append({"title": item.title, "image_url": image_url})

    return render(request, "slider/index.html", {"slides": slides})
