from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from apps.transactions.models import Transaction


@login_required
def dashboard(request):
    user_transactions = Transaction.objects.filter(user=request.user)
    total = user_transactions.count()
    fraud_count = user_transactions.filter(status='fraud').count()
    safe_count = user_transactions.filter(status='safe').count()
    recent = user_transactions[:5]

    fraud_rate = round((fraud_count / total * 100), 1) if total > 0 else 0

    context = {
        'total': total,
        'fraud_count': fraud_count,
        'safe_count': safe_count,
        'recent_transactions': recent,
        'fraud_rate': fraud_rate,
    }
    return render(request, 'dashboard/dashboard.html', context)
