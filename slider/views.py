from django.shortcuts import render


DEMO_SLIDES = [
    {
        "title": "Горы на рассвете",
        "image_url": "https://images.unsplash.com/photo-1464822759023-fed622ff2c3b?auto=format&fit=crop&w=1600&q=80",
    },
    {
        "title": "Лесная тропа",
        "image_url": "https://images.unsplash.com/photo-1441974231531-c6227db76b6e?auto=format&fit=crop&w=1600&q=80",
    },
    {
        "title": "Морское побережье",
        "image_url": "https://images.unsplash.com/photo-1507525428034-b723cf961d3e?auto=format&fit=crop&w=1600&q=80",
    },
    {
        "title": "Город вечером",
        "image_url": "https://images.unsplash.com/photo-1477959858617-67f85cf4f1df?auto=format&fit=crop&w=1600&q=80",
    },
]


def slider_page(request):
    return render(request, "slider/index.html", {"slides": DEMO_SLIDES})
