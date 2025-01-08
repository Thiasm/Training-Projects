from django.shortcuts import render, get_object_or_404
from django.views.generic.list import ListView
from django.views.decorators.http import require_http_methods
from .models import Item, Category
from django.db.models.functions import Lower
from .utils import CategoryTemplateManager, ApiRequest
from django.http import HttpResponse

class CategoryList(ListView):
    model = Category
    template_name = 'app/home.html'
    context_object_name = 'categories'
    ordering = ['-created']

    def filter_queryset(self, queryset):
        search = self.request.GET.get("research")
        if search:
            queryset = queryset.filter(title__icontains=search)
        return queryset

    # Retourne le queryset après application des filtres.
    def get_queryset(self):
        queryset = super().get_queryset()
        return self.filter_queryset(queryset)

    def get(self, request, *args, **kwargs):
        self.object_list = self.get_queryset()
        context = self.get_context_data()
        if request.headers.get("HX-Request"):
            print('HX-Request -> DONC render task_list')
            return render(request, "app/partials/category_list.html", context)
        return render(request, self.template_name, context)
    
@require_http_methods(['GET', 'POST'])
def add_category(request):
    if request.method == 'GET':
        return render(request, 'app/modals/add_category_modal.html', { 'category_types': Category.CategoryTypes })
    if request.method == 'POST':
        category_type = request.POST.get('category_type')
        category_title = request.POST.get('category_title')
        Category.objects.create(title = category_title, type = category_type) # Crée un objet Category et le sauvegarde
        categories = Category.objects.all().order_by('-created') # Récupère la liste mise à jour des catégories
        return render(request, 'app/partials/category_list.html', {'categories': categories}) # Retourne la liste des catégories

class ItemList(ListView):
    model = Item
    template_name = 'app/base_list.html'
    context_object_name = 'items'

    def filter_queryset(self, queryset):

        # FIX Get from context
        category_name = self.kwargs.get('category')
        category = get_object_or_404(Category, title=category_name)
        if category:
            queryset = queryset.filter(category=category)

        search = self.request.GET.get("research")
        if search:
            queryset = queryset.filter(title__icontains=search)

        ordering = self.request.GET.get("ordering")
        if ordering in ['title', '-title', 'created', '-created', 'complete', '-complete']:
            if ordering == 'title' or ordering == '-title':
                ordering = 'lower_title'
                queryset = queryset.annotate(lower_title=Lower('title'))
            return queryset.order_by(ordering)

        return queryset.order_by('-complete', '-created')

    def get_queryset(self):
        queryset = super().get_queryset()
        return self.filter_queryset(queryset)

    # WHAT IS CONTEXT ?
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # WHY ?
        category_name = self.kwargs.get("category")
        category = get_object_or_404(Category, title=category_name)
        context["category"] = category
        category_item = CategoryTemplateManager.get_category_item(category.type)
        context["category_item"] = category_item
        return context

    def get(self, request, *args, **kwargs):
        self.object_list = self.get_queryset()
        context = self.get_context_data()
        if request.headers.get("HX-Request"):
            return render(request, f"app/partials/{context['category_item']}_list.html", context)
        return render(request, self.template_name, context)

@require_http_methods(['GET'])
def search_items(request, category):
    category = get_object_or_404(Category, title=category)
    base_url = category.get_api_url()
    search_input = request.GET.get('item_title')
    
    # Get category type from the category model
    category_type = category.type.lower()
    
    results = ApiRequest.get_api_search(base_url, search_input, category_type)
    return render(request, 'app/partials/search_results.html', {
        'results': results,
        'category': category
    })

@require_http_methods(['GET', 'POST'])
def add_task(request, category):
    category = get_object_or_404(Category, title=category)
    category_item = CategoryTemplateManager.get_category_item(category.type)
    if request.method == 'POST':
        item_title = request.POST.get(f'{category_item}_title')
        Item.objects.create(title = item_title, category=category) # Crée un objet Item et le sauvegarde
        items = Item.objects.filter(category=category).order_by('-complete', '-created')  # Récupère la liste mise à jour des tâches
        return render(request, f'app/partials/{category_item}_list.html', {'items': items, 'category': category})

@require_http_methods(['GET', 'POST'])
def add_item(request, category):
    category = get_object_or_404(Category, title=category)
    category_item = CategoryTemplateManager.get_category_item(category.type)
    
    if request.method == 'GET':
        return render(request, f'app/modals/add_{category_item}_modal.html', {'category': category})

    if request.method == 'POST':
        title = request.POST.get('title')
        img = request.POST.get('image')
        description = request.POST.get('description')
        
        Item.objects.create(title=title, category=category, image=img, description=description)
        items = Item.objects.filter(category=category).order_by('-complete', '-created')
        return render(request, f'app/partials/{category_item}_list.html', {'items': items, 'category': category})
    
    return render(request, f'app/modals/add_{category_item}_modal.html', {'category': category})

@require_http_methods(['DELETE'])
def delete_item(request, id, category):
    category = get_object_or_404(Category, title=category)
    category_item = CategoryTemplateManager.get_category_item(category.type)
    item = get_object_or_404(Item, id = id)
    item.delete()
    items = Item.objects.filter(category=category).order_by('-complete', '-created')  # Récupère la liste mise à jour des tâches
    return render(request, f'app/partials/{category_item}_list.html', {'items': items, 'category': category})

@require_http_methods(['POST'])
def complete_item(request, id, category):
    category = get_object_or_404(Category, title=category)
    category_item = CategoryTemplateManager.get_category_item(category.type)
    item = get_object_or_404(Item, id=id)
    item.complete = not item.complete
    item.save()
    items = Item.objects.filter(category=category).order_by('-complete', '-created')  # Récupère la liste mise à jour des tâches
    return render(request, f'app/partials/{category_item}_list.html', {'items': items, 'category': category})

@require_http_methods(['GET', 'POST'])
def edit_item(request, id, category):
    category = get_object_or_404(Category, title=category)
    category_item = CategoryTemplateManager.get_category_item(category.type)
    item = get_object_or_404(Item, id = id)
    if request.method == 'GET':
        return render(request, f'app/modals/edit_{category_item}_modal.html', {'item': item, 'category': category})
    if request.method == 'POST':
        item.title = request.POST.get(f'{category_item}_title')
        item.description = request.POST.get(f'{category_item}_description')
        item.complete = f'{category_item}_complete' in request.POST
        item.save()
        return render(request, f'app/partials/{category_item}.html', {'item': item, 'category': category})

def custom_page_not_found_view(request, exception):
    response = render(request, 'app/404.html', {})
    response.status_code = 404
    return response