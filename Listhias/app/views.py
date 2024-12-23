from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic.list import ListView
from django.views.decorators.http import require_http_methods
from django.urls import reverse_lazy
from .models import Task

class TaskList(ListView):
    model = Task
    template_name = 'app/todo_list.html'
    context_object_name = 'tasks' # Change the Props
    ordering = ['-complete']

@require_http_methods(['POST'])
def add_task(request):
    task_title = request.POST.get('task_title') # Récupère l'input
    task = Task.objects.create(title = task_title) # Crée un objet Task et le sauvegarde
    tasks = Task.objects.all().order_by('-complete', '-created')
    return render(request, 'app/partials/task_list.html', {'tasks': tasks})

@require_http_methods(['DELETE'])
def delete_task(request, id):
    task = get_object_or_404(Task, id = id)
    task.delete()
    tasks = Task.objects.all().order_by('-complete', '-created')  # Récupère la liste mise à jour des tâches
    return render(request, 'app/partials/task_list.html', {'tasks': tasks})

@require_http_methods(['PUT'])
def complete_task(request, id):
    task = get_object_or_404(Task, id = id)
    task.complete = not task.complete
    task.save()
    tasks = Task.objects.all().order_by('-complete', '-created')  # Récupère la liste mise à jour des tâches
    return render(request, 'app/partials/task_list.html', {'tasks': tasks})
    # return render(request, 'app/partials/task.html', {'task': task})

@require_http_methods(['GET', 'POST'])
def edit_task(request, id):
    task = get_object_or_404(Task, id = id)
    if request.method == 'GET':
        return render(request, 'app/modals/edit_task_modal.html', {'task': task})
    if request.method == 'POST':
        task.title = request.POST.get("task_title")
        task.description = request.POST.get("task_description")
        task.complete = 'task_complete' in request.POST
        task.save()
        return render(request, 'app/partials/task.html', {'task': task})