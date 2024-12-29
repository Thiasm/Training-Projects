from django.shortcuts import render, get_object_or_404
from django.views.generic.list import ListView
from django.views.decorators.http import require_http_methods
from .models import Item, Category
from django.db.models.functions import Lower

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
            return render(request, "app/partials/category_list.html", context)
        return render(request, self.template_name, context)
    
@require_http_methods(['GET', 'POST'])
def add_category(request):
    if request.method == 'GET':
        context = { 'category_types': Category.CategoryTypes } # Add Category_List to the modal
        return render(request, 'app/modals/add_category_modal.html', context)
    if request.method == 'POST':
        category_type = request.POST.get('category_type')
        category_title = request.POST.get('category_title')
        Category.objects.create(title = category_title, type = category_type) # Crée un objet Category et le sauvegarde
        categories = Category.objects.all().order_by('-created') # Récupère la liste mise à jour des catégories
        return render(request, 'app/partials/category_list.html', {'categories': categories}) # Retourne la liste des catégories

class ItemList(ListView):
    model = Item
    template_name = 'app/todo_list.html'
    context_object_name = 'items'

    ordering = ['-complete', '-created']

    def filter_queryset(self, queryset):
        search = self.request.GET.get("research")
        ordering = self.request.GET.get("ordering")
    
        # category_name = self.kwargs.get('category')
        # category = get_object_or_404(Category, title=category_name)  # Find category by name
        # if category:
            # print('Filtred by Category:', category)
            # return Item.objects.filter(category=category)

        if search:
            queryset = queryset.filter(title__icontains=search) # Filtre les tâches par titre
        if ordering in ['title', '-title', 'created', '-created', 'complete', '-complete']:
            if 'title' in ordering: # Si le tri est basé sur le titre, utilise la fonction Lower pour trier en minuscule
                ordering = ordering.replace('title', 'lower_title') # ????
                queryset = queryset.annotate(lower_title=Lower('title'))
            queryset = queryset.order_by(ordering)
        # order_by('-complete', '-created')
        return queryset

    def get_queryset(self):
        queryset = super().get_queryset()
        return self.filter_queryset(queryset)

    def get(self, request, *args, **kwargs):
        self.object_list = self.get_queryset()
        context = self.get_context_data()
        if request.headers.get("HX-Request"):
            # FIX TASK_LIST OR TODO_LIST
            return render(request, "app/partials/task_list.html", context)
        return render(request, self.template_name, context)

@require_http_methods(['GET', 'POST'])
def add_item(request):
    print('Add_Item')
    if request.method == 'GET':
        print('Add_Item GET')
        # FIX ADD_TASK OR ADD_ITEM
        return render(request, 'app/modals/add_task_modal.html')
    if request.method == 'POST':
        print('Add_Item POST')
        # FIX TASK OR ITEM
        item_title = request.POST.get('task_title') # Récupère l'input

        category_id = request.POST.get('category')  # Category ID from the form
        category = Category.objects.get(id=category_id)

        Item.objects.create(title = item_title, category=category) # Crée un objet Item et le sauvegarde
        items = Item.objects.order_by('-complete', '-created')
        # .filter(category=category)
        return render(request, 'app/partials/task_list.html', {'items': items})

@require_http_methods(['DELETE'])
def delete_item(request, id):
    item = get_object_or_404(Item, id = id)
    item.delete()
    items = Item.objects.all().order_by('-complete', '-created')  # Récupère la liste mise à jour des tâches
    return render(request, 'app/partials/task_list.html', {'items': items})

@require_http_methods(['POST'])
def complete_item(request, id):
    item = get_object_or_404(Item, id = id)
    item.complete = not item.complete
    item.save()
    items = Item.objects.all().order_by('-complete', '-created')  # Récupère la liste mise à jour des tâches
    return render(request, 'app/partials/task_list.html', {'items': items})

@require_http_methods(['GET', 'POST'])
def edit_item(request, id):
    item = get_object_or_404(Item, id = id)
    if request.method == 'GET':
        return render(request, 'app/modals/edit_item_modal.html', {'item': item})
    if request.method == 'POST':
        item.title = request.POST.get("item_title")
        item.description = request.POST.get("item_description")
        item.complete = 'item_complete' in request.POST
        item.save()
        return render(request, 'app/partials/task.html', {'item': item})
