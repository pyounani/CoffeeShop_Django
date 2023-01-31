
from django.shortcuts import render
from product.models import Item

# Create your views here.
def landing(request):
    recent_item = Item.objects.order_by('-pk')[:3]
    return render(request, 'main_pages/landing.html', {
        'recent_items': recent_item,
    })

def about_me(request):
    return render(request, 'main_pages/about_me.html')


def about_company(request):
    return render(request, 'main_pages/company.html')
