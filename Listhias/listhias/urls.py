from django.contrib import admin
from django.urls import path, include

# from rest_framework import routers
# from app.views import TaskViewSet

# router = routers.DefaultRouter()
# router.register(r'tasks', TaskViewSet, 'task')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('app.urls'))
]
