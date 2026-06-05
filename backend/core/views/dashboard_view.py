from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from core.service.dashboard_service import DashboardService


@login_required(login_url='/web/login/')
def tela_dashboard(request):
    dados = DashboardService().resumo()
    return render(request, 'dashboard.html', dados)
