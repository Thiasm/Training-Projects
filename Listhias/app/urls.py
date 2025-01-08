from django.urls import path
from .views import ItemList, add_task, add_item, edit_item, delete_item, complete_item, edit_item, CategoryList, add_category, search_items

urlpatterns = [
    path('', CategoryList.as_view(), name='home'),
    
    path('add_category/', add_category, name='add_category'),

    # Remove Category
    # Edit Category

    path('<category>/', ItemList.as_view(), name='view'),

    path('<category>/search_items/', search_items, name='search_items'),

    path('<category>/add_task/', add_task, name='add_task'),
    path('<category>/add_item/', add_item, name='add_item'),
    path('<category>/edit_item/<int:id>', edit_item, name='edit_item'),
    path('<category>/delete_item/<int:id>', delete_item, name='delete_item'),
    path('<category>/complete_item/<int:id>', complete_item, name='complete_item'),
]
