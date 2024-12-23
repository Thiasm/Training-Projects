from django.urls import path
from .views import TaskList, add_task, edit_task, delete_task, complete_task, edit_task

urlpatterns = [
    path('', TaskList.as_view(), name='todo_list'),
    path('add_task/', add_task, name='add_task'),
    path('edit_task/<int:id>', edit_task, name='edit_task'),
    path('delete_task/<int:id>', delete_task, name='delete_task'),
    path('complete_task/<int:id>', complete_task, name='complete_task'),
    path('edit_task/<int:id>', edit_task, name='edit_task')
]
