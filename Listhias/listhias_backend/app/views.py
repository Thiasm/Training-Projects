from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic.list import ListView
from django.views.decorators.http import require_http_methods
from django.urls import reverse_lazy
from django.http.response import HttpResponse
from .models import Task

# def home_page(request):
#     return render(request, 'app/home_page.html')

# class CategoryList(ListView):
#     model = Category
#     context_object_name = 'categories' # Change the Props name
#     template_name = 'app/category_list.html'

class TaskList(ListView):
    model = Task
    template_name = 'app/todo_list.html'
    context_object_name = 'tasks' # Change the Props 

@require_http_methods(['POST'])
def add_task(request):
    task_title = request.POST.get('task_title') # Récupère l'input
    task = Task.objects.create(title = task_title) # Crée un objet Task et le sauvegarde
    tasks = Task.objects.all().order_by('-created')
    return render(request, 'app/partials/task_list.html', {'tasks': tasks})

@require_http_methods(['PUT'])
def edit_task(request, id):
    task = get_object_or_404(Task, id = id)
    return redirect(reverse_lazy('todo_list'))

@require_http_methods(['DELETE'])
def delete_task(request, id):
    task = get_object_or_404(Task, id = id)
    task.delete()
    tasks = Task.objects.all().order_by('-created')  # Récupère la liste mise à jour des tâches
    return render(request, 'app/partials/task_list.html', {'tasks': tasks})

@require_http_methods(['PUT'])
def complete_task(request, id):
    task = get_object_or_404(Task, id = id)
    task.complete = not task.complete
    task.save()
    return render(request, 'app/partials/task.html', {'task': task})

