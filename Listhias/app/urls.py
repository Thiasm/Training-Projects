from django.urls import path
from .views import ItemList, add_item, edit_item, delete_item, complete_item, edit_item, CategoryList, add_category

urlpatterns = [
    path('', CategoryList.as_view(), name='home'),
    path('add_category/', add_category, name='add_category'),
    # Remove Category
    # Edit Category

    # FIX <category>/
    path('test/', ItemList.as_view(), name='view'),

    path('add_item/', add_item, name='add_item'),
    path('edit_item/<int:id>', edit_item, name='edit_item'),
    path('delete_item/<int:id>', delete_item, name='delete_item'),
    path('complete_item/<int:id>', complete_item, name='complete_item'),

    # path('todo_list/', ItemList.as_view(), name='todo_list')
]
