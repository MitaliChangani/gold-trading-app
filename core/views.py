import os, json
from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponseBadRequest
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from .models import Wallet
from .transactions import Transaction
from .withdrawals import WithdrawalRequest
import razorpay
RP_KEY = os.environ.get('RAZORPAY_KEY_ID')
RP_SECRET = os.environ.get('RAZORPAY_KEY_SECRET')
if RP_KEY and RP_SECRET:
    client = razorpay.Client(auth=(RP_KEY, RP_SECRET))
else:
    client = None
def home(request):
    return render(request, 'home.html')
@csrf_exempt
def create_order(request):
    if request.method != 'POST':
        return HttpResponseBadRequest('POST required')
    if not client:
        return JsonResponse({'error':'Razorpay keys not configured'}, status=500)
    data = json.loads(request.body.decode('utf-8') or '{}')
    amount = float(data.get('amount',0))
    if amount <= 0:
        return JsonResponse({'error':'amount must be > 0'}, status=400)
    order = client.order.create({'amount': int(round(amount*100)), 'currency':'INR', 'payment_capture':1})
    return JsonResponse(order)
@csrf_exempt
def payment_verify(request):
    if request.method != 'POST':
        return HttpResponseBadRequest('POST required')
    if not client:
        return JsonResponse({'error':'Razorpay keys not configured'}, status=500)
    data = json.loads(request.body.decode('utf-8') or '{}')
    try:
        razorpay.utility.verify_payment_signature({
            'razorpay_order_id': data.get('razorpay_order_id'),
            'razorpay_payment_id': data.get('razorpay_payment_id'),
            'razorpay_signature': data.get('razorpay_signature')
        })
        uid = int(data.get('user_id',0))
        amount = float(data.get('amount',0))
        if uid and amount>0:
            user = User.objects.filter(id=uid).first()
            if user:
                w = getattr(user,'wallet',None)
                if not w:
                    w = Wallet.objects.create(user=user)
                Transaction.objects.create(user=user,type='PAYMENT',amount_cents=int(round(amount*100)),reference=data.get('razorpay_payment_id'))
                w.balance_cents += int(round(amount*100))
                w.save()
        return JsonResponse({'ok':True})
    except Exception as e:
        return JsonResponse({'error':str(e)}, status=400)
@login_required
def profile(request):
    user = request.user
    wallet = getattr(user,'wallet',None)
    balance = wallet.balance() if wallet else 0.0
    return render(request, 'profile.html', {'balance': balance})
@csrf_exempt
def signup(request):
    if request.method=='POST':
        data = json.loads(request.body.decode('utf-8') or '{}')
        username = data.get('username')
        password = data.get('password')
        if not username or not password:
            return JsonResponse({'error':'username & password required'}, status=400)
        if User.objects.filter(username=username).exists():
            return JsonResponse({'error':'username exists'}, status=400)
        u = User.objects.create_user(username=username, password=password)
        Wallet.objects.create(user=u)
        return JsonResponse({'ok':True, 'id': u.id})
    return JsonResponse({'error':'POST required'}, status=400)
@csrf_exempt
def login_view(request):
    if request.method=='POST':
        data = json.loads(request.body.decode('utf-8') or '{}')
        username = data.get('username')
        password = data.get('password')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return JsonResponse({'ok':True, 'id': user.id})
        return JsonResponse({'error':'invalid credentials'}, status=400)
    return JsonResponse({'error':'POST required'}, status=400)
@login_required
def logout_view(request):
    logout(request)
    return redirect('home')
@csrf_exempt
def withdraw_request(request):
    if request.method!='POST':
        return JsonResponse({'error':'POST required'}, status=400)
    data = json.loads(request.body.decode('utf-8') or '{}')
    uid = int(data.get('user_id',0))
    amount = float(data.get('amount',0))
    user = User.objects.filter(id=uid).first()
    if not user:
        return JsonResponse({'error':'user not found'}, status=404)
    wallet = getattr(user,'wallet',None)
    if not wallet or wallet.balance_cents < int(round(amount*100)):
        return JsonResponse({'error':'insufficient balance'}, status=400)
    wr = WithdrawalRequest.objects.create(user=user, amount_cents=int(round(amount*100)))
    return JsonResponse({'ok':True, 'id': wr.id})