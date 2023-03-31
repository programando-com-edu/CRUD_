from django.urls import path
from .views import PessoaList, PessoaCreate, PessoaUpdate, PessoaDelete

urlpatterns = [
    path('', PessoaList.as_view(), name='list'),
    path('create/', PessoaCreate.as_view(), name='pessoa_create'),
    path('update/<int:pk>/', PessoaUpdate.as_view(), name='pessoa_update'),
    path('delete/<int:pk>/', PessoaDelete.as_view(), name='pessoa_delete'),
]