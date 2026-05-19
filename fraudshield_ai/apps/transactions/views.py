from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Transaction
from .ml_engine import predict_fraud


@login_required
def transaction_check(request):
    if request.method == 'POST':
        try:
            amount = float(request.POST.get('amount', 0))
            transaction_type = request.POST.get('transaction_type', 'purchase')
            merchant = request.POST.get('merchant', 'Unknown').strip()
            location = request.POST.get('location', 'Unknown').strip()
            device = request.POST.get('device', 'mobile')
            transaction_time = int(request.POST.get('transaction_time', 12))

            if amount <= 0:
                messages.error(request, 'Amount must be positive.')
                return redirect('transactions:check')

            is_fraud, confidence, anomaly_score = predict_fraud(
                amount, transaction_type, merchant, location, device, transaction_time
            )

            status = 'fraud' if is_fraud else 'safe'

            txn = Transaction.objects.create(
                user=request.user,
                amount=amount,
                transaction_type=transaction_type,
                merchant=merchant,
                location=location,
                device=device,
                transaction_time=transaction_time,
                status=status,
                confidence=confidence,
            )

            context = {
                'transaction': txn,
                'is_fraud': is_fraud,
                'confidence': round(confidence * 100, 1),
                'anomaly_score': round(anomaly_score, 4),
                'status': status,
            }
            return render(request, 'transactions/result.html', context)

        except (ValueError, TypeError) as e:
            messages.error(request, f'Invalid input: {e}')
            return redirect('transactions:check')

    return render(request, 'transactions/check.html')


@login_required
def transaction_history(request):
    transactions = Transaction.objects.filter(user=request.user)
    total = transactions.count()
    fraud_count = transactions.filter(status='fraud').count()
    safe_count = transactions.filter(status='safe').count()

    context = {
        'transactions': transactions,
        'total': total,
        'fraud_count': fraud_count,
        'safe_count': safe_count,
    }
    return render(request, 'transactions/history.html', context)
