from django.contrib.auth import get_user_model
from django.http import JsonResponse,HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required

# Create your views here.

import braintree

gateway = braintree.BraintreeGateway(
    braintree.Configuration(
        braintree.Environment.Sandbox,
        merchant_id="jmxykkpqf9wgfkf7",
        public_key="7jqb5882fxgf5gv6",
        private_key="d0a7e23c103013dc929ad16b66b8579b"
    )
)


def validate_user_session(id,token):
    UserModel = get_user_model()
    try:
        user = UserModel.objects.get(pk=id)
        if user.session_token == token:
            return True
        return False
    except UserModel.DoesNotExist:
        return False
@csrf_exempt
def generate_token(request,id,token):
    if not validate_user_session(id,token):
        return JsonResponse({'error':'Invalid session,please login again'})
    return JsonResponse({'client token': gateway.client_token.generate(), 'success': True})

@csrf_exempt
def payment_process(request,id,token):
    if not validate_user_session(id, token):
        return JsonResponse({'error': 'Invalid session,please login again'})
    nonce_from_the_client = request.POST['PaymentMethodNonce']
    amount_from_the_client = request.POST['amount']
    result = gateway.transaction.sale({
        "amount": amount_from_the_client,
        "payment_method_nonce": nonce_from_the_client,
        "options": {
            "submit_for_settlement": True
        }
    })
    if result.is_success:
        return JsonResponse({'success':result.is_success,
                             'transaction':result.transaction.id,
                             'amount':result.transaction.amount
                             })
    else:
        return JsonResponse({'error':True,'success':False})


