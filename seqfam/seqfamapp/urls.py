from django.views.generic.base import RedirectView
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'interpro', views.InterProViewSet)
router.register(r'pfam', views.PfamViewSet)
router.register(r'uniprot', views.UniProtKBViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
    path('', RedirectView.as_view(pattern_name='interpro_list', permanent=False)),
    path('interpro', views.interpro_list, name='interpro_list'),
    path('compress/sequence/', views.CompressExistingDBSequencesView.as_view(),
         name='compress_sequemce'),
    path('pfam', views.pfam_list, name='pfam_list'),
    path('uniprot', views.uniprot_list, name='uniprot_list'),
]
