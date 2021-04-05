from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.template import loader
from django.urls import reverse
from django.utils import timezone
from .models import Questao, Opcao

def index(request):
    latest_question_list = Questao.objects.order_by('-pub_data')[:5]
    context = {'latest_question_list': latest_question_list}
    return render(request, 'votacao/index.html', context)

def detalhe(request, questao_id):
    questao = get_object_or_404(Questao, pk=questao_id)
    return render(request, 'votacao/detalhe.html', {'questao': questao})

def resultados(request, questao_id):
    questao = get_object_or_404(Questao, pk=questao_id)
    return render(request, 'votacao/resultados.html', {'questao': questao})

def novaquestao (request):
    return render(request, 'votacao/novaquestao.html')

def gravarnovaquestao (request):
    novaquestaotxt = request.POST['novaquestao']
    q = Questao(questao_texto = novaquestaotxt, pub_data=timezone.now())
    q.save()
    return HttpResponseRedirect(reverse('votacao:index'))

def novaopcao (request, questao_id):
    questao = get_object_or_404(Questao, pk=questao_id)
    opcaotxt = request.POST.get('novaopcao', False)
    if opcaotxt is not False:
        questao.opcao_set.create(opcao_texto=opcaotxt, votos=0)
        return HttpResponseRedirect(reverse('votacao:detalhe',args=(questao.id,)))
    else:
        return render(request, 'votacao/novaopcao.html', {'questao': questao})

def apagarquestao (request):
    latest_question_list = Questao.objects.order_by('-pub_data')[:5]
    context = {'latest_question_list': latest_question_list}
    return render(request, 'votacao/apagarquestao.html', context)

def gravarapagarquestao (request):
    questao = get_object_or_404(Questao, pk=request.POST['questao'])
    questao.delete()
    return HttpResponseRedirect(reverse('votacao:index'))

def voto(request, questao_id):
    questao = get_object_or_404(Questao, pk=questao_id)
    try:
        opcao_seleccionada = questao.opcao_set.get(pk=request.POST['opcao'])
    except (KeyError, Opcao.DoesNotExist):
        # Apresenta de novo o form para votar
        return render(request, 'votacao/detalhe.html', {
            'questao': questao,
            'error_message': "Não escolheu uma opção",
        })
    else:
        opcao_seleccionada.votos += 1
        opcao_seleccionada.save()
        # Retorne sempre HttpResponseRedirect depois de
        # tratar os dados POST de um form
        # pois isso impede os dados de serem tratados
        # repetidamente se o utilizador
        # voltar para a página web anterior.
        return HttpResponseRedirect(reverse('votacao:resultados', args=(questao.id,)))