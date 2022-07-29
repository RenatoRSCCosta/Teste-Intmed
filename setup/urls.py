from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from medicar.views import *


router = routers.DefaultRouter()
router.register('consultas', ConsultasViewSet, basename='consultas')
router.register('agendas', AgendasViewSet, basename='agendas')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(router.urls)),
    path('swagger/', include('swagger.urls')),
    #path('agendas/', Agendas.as_view()),
    #path('agenda/', AgendaAPIView.as_view()),
]
