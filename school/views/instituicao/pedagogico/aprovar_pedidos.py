from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import permission_required, login_required
from django.utils import timezone
from django.contrib import messages
from school.models.documento.pedido_documento import PedidoDocumento

#@permission_required('pedagogico.aprovar_docs', raise_exception=True)
@login_required
def aprovar_pedidos(request):
    pedidos = PedidoDocumento.objects.filter(status='p')

    if request.method == 'POST':
        for key, value in request.POST.items():
            if key.startswith("p_"):
                pedido_id = key.replace("p_", "")
                pedido = get_object_or_404(PedidoDocumento, pk=pedido_id)
                acao = value  # 'aprovar' ou 'rejeitar'
                pedido.status = 'a' if acao == 'a' else 'r'
                pedido.data_validacao = timezone.now()
                pedido.validado_por = request.user
                pedido.save()

        messages.success(request, "Pedidos processados com sucesso.")
        return redirect('school:aprovar_pedidos')

    return render(request, 'apps/instituicao/pedagogico/documentos/aprovar_pedidos.html', {'pedidos': pedidos})
