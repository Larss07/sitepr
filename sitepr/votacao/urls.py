from django.urls import include, path
from django.conf.urls import url
from . import views
# (. significa que importa views da mesma directoria)
app_name = 'votacao'
urlpatterns = [
    # ex: votacao/
    path("", views.index, name='index'),
    # ex: votacao/1
    path('<int:questao_id>', views.detalhe, name='detalhe'),
    # ex: votacao/3/resultados
    path('<int:questao_id>/resultados', views.resultados, name='resultados'),
    # ex: votacao/5/voto
    path('<int:questao_id>/voto', views.voto, name='voto'),
    # ex: votacao/novaquestao
    path('novaquestao/', views.novaquestao, name='novaquestao'),
    # ex: votacao/5/voto
    path('<int:questao_id>/novaopcao/', views.novaopcao, name='novaopcao'),
    # ex: votacao/5/voto
    path('gravarnovaquestao/', views.gravarnovaquestao, name='gravarnovaquestao'),
    # ex: votacao/5/voto
    path('gravarapagarquestao/', views.gravarapagarquestao, name='gravarapagarquestao'),
    # ex: votacao/5/voto
    path('apagarquestao/', views.apagarquestao, name='apagarquestao'),
]

