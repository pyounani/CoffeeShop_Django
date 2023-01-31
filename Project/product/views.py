from datetime import timezone

from django.core.exceptions import PermissionDenied
from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404
from django.utils.text import slugify
from django.views.generic import ListView, CreateView, UpdateView, DetailView
from .models import Item, Category, Tag, Comment, Company
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .forms import CommentForm
from rest_framework import viewsets
from .serializers import itemSerializer

# Create your views here.
class itemViewSet(viewsets.ModelViewSet):
    queryset = Item.objects.all()
    serializer_class = itemSerializer

def delete_comment(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    item = comment.item
    if request.user.is_authenticated and request.user == comment.author:
        comment.delete()
        return redirect(item.get_absolute_url())
    else:
        PermissionDenied

class ItemUpdate(LoginRequiredMixin, UpdateView):
    model = Item
    fields = ['title', 'content', 'head_image', 'price', 'company', 'category', 'nutrient']
    template_name = 'product/item_update_form.html'

    def dispatch(self, request, *args, **kwargs):
        current_user = self.request.user
        if current_user.is_authenticated:
            return super(ItemUpdate, self).dispatch(request, *args, **kwargs)
        else:
            raise PermissionDenied

    def form_valid(self, form):
        current_user = self.request.user
        if current_user.is_authenticated and (current_user.is_superuser or current_user.is_staff):
            form.instance.author = current_user
            response = super(ItemUpdate, self).form_valid(form)
            tags_str = self.request.POST.get('tags_str')
            if tags_str:
                tags_str = tags_str.strip()
                tags_str = tags_str.replace(',', ';')
                tag_list = tags_str.split(';')
                for t in tag_list:
                    t = t.strip()
                    tag, is_tag_created = Tag.objects.get_or_create(name=t)
                    if is_tag_created:
                        tag.slug = slugify(t, allow_unicode=True)
                        tag.save()
                    self.object.tags.add(tag)
            return response
        else:
            return redirect('/product/')

    def get_context_data(self, **kwargs):
        context = super(ItemUpdate, self).get_context_data()
        context['companies'] = Company.objects.all()
        return context


class ItemCreate(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Item
    fields = ['title', 'content', 'head_image', 'price', 'company', 'category', 'nutrient']

    def test_func(self):
        return self.request.user.is_superuser or self.request.user.is_staff

    def form_valid(self, form):
        current_user = self.request.user
        if current_user.is_authenticated and (current_user.is_superuser or current_user.is_staff):
            form.instance.author = current_user
            response = super(ItemCreate, self).form_valid(form)
            tags_str = self.request.POST.get('tags_str')

            if tags_str:
                tags_str = tags_str.strip()
                tags_str = tags_str.replace(',', ';')
                tag_list = tags_str.split(';')
                for t in tag_list:
                    t = t.strip()
                    tag, is_tag_created = Tag.objects.get_or_create(name=t)
                    if is_tag_created:
                        tag.slug = slugify(t, allow_unicode=True)
                        tag.save()
                    self.object.tags.add(tag)
            return response

        else:
            return redirect('/product/')

    def get_context_data(self, **kwargs):
        context = super(ItemCreate, self).get_context_data()
        context['companies'] = Company.objects.all()
        return context


class ItemList(ListView):
    model = Item
    ordering = '-pk'
    paginate_by = 6

    def get_context_data(self,  **kwargs):
        context = super(ItemList, self).get_context_data()
        context['companies'] = Company.objects.all()
        return context


class ItemSearch(ItemList):
    paginate_by = None

    def get_queryset(self):
        q = self.kwargs['q']
        item_list = Item.objects.filter(Q(title__contains=q) | Q(tags__name__contains=q)).distinct()
        return item_list

    def get_context_data(self, **kwargs):
        context = super(ItemSearch, self).get_context_data()
        q = self.kwargs['q']
        context['search_info'] = f'Search: {q} ({self.get_queryset().count()})'
        return context


class ItemDetail(DetailView):
    model = Item

    def get_context_data(self, **kwargs):
        context = super(ItemDetail, self).get_context_data()
        context['companies'] = Company.objects.all()
        context['comment_form'] = CommentForm
        return context


class CommentList(ListView):
    model = Comment


def new_comment(request, pk):
    if request.user.is_authenticated:
        item = get_object_or_404(Item, pk=pk)

        if request.method == 'POST':
            comment_form = CommentForm(request.POST)
            if comment_form.is_valid():
                comment = comment_form.save(commit=False)
                comment.item = item
                comment.author = request.user
                comment.save()
                return redirect(comment.get_absolute_url())
        else:
            return redirect(item.get_absolute_url())
    else:
        raise PermissionDenied


class CommentUpdate(LoginRequiredMixin, UpdateView):
    model = Comment
    form_class = CommentForm

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated and request.user == self.get_object().author:
            return super(CommentUpdate, self).dispatch(request, *args, **kwargs)
        else:
            raise PermissionDenied


def category_page(request, slug):
    category = Category.objects.get(slug=slug)
    item_list = Item.objects.filter(category=category)
    return render(request, 'product/item_list.html', {
        'category': category,
        'item_list': item_list,
        'categories': Category.objects.all()
    })


def company_page(request, slug):
    company = Company.objects.get(slug=slug)
    item_list = Item.objects.filter(company=company)
    return render(request, 'product/item_list.html', {
        'category': company,
        'item_list': item_list,
        'companies': Company.objects.all()
    })




def tag_page(request, slug):
    tag = Tag.objects.get(slug=slug)
    item_list = tag.item_set.all()
    return render(request, 'product/item_list.html', {
        'tag': tag,
        'item_list': item_list,
        'categories': Category.objects.all(),
    })

