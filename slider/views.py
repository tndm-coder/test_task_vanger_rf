from django.shortcuts import render

from .models import SliderItem

def slider_page(request):
    slider_items = SliderItem.objects.select_related("image").order_by("order", "id")
    slides = [
        {"title": item.title, "image_url": item.image.url}
        for item in slider_items
        if item.image
    ]
    return render(request, "slider/index.html", {"slides": slides})
