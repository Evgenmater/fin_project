import datetime as dt

from django.shortcuts import get_object_or_404, render

from blog.models import Post, Category


def index(request):
    template = 'blog/index.html'
    post_list = Post.objects.select_related(
        'author',
        'location',
        'category',
    ).filter(
        pub_date__date__lte=dt.datetime.now(),
        is_published=True,
        category__is_published=True,
    ).order_by('-pub_date')[:5]
    context = {
        'post_list': post_list,
    }
    return render(request, template, context)


def post_detail(request, pk):
    template = 'blog/detail.html'
    post = get_object_or_404(
        Post.objects.filter(
         pub_date__date__lte=dt.datetime.now(),
         is_published=True,
         category__is_published=True,
        ),
        pk=pk,
    )
    context = {
        'post': post,
    }
    return render(request, template, context)


def category_posts(request, category_slug):
    template = 'blog/category.html'
    category_post = get_object_or_404(
        Category,
        slug=category_slug,
        is_published=True,
    )
    post_list = Post.objects.select_related(
        'category',
        'location',
        'author',
    ).filter(
        pub_date__date__lte=dt.datetime.now(),
        is_published=True,
        category=category_post,
    )
    context = {
        'category_post': category_post,
        'post_list': post_list
    }
    return render(request, template, context)
