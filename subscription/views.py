from django.shortcuts import render,get_object_or_404
from django.http import HttpResponseBadRequest
from django.views import View
from account.mixins import TrainerRequiredMixin,PlatformUserRequiredMixin
from .models import SubscriptionPlanTrainer,SubscribedTrainer,PaymentRecord
from account.models import Trainer
from django.contrib import messages as message
from django.views.decorators.csrf import csrf_exempt
import razorpay
from django.conf import settings
import uuid
from datetime import datetime, timedelta


# Create your views here.
class SubscriptionPlan(TrainerRequiredMixin,View):
    def get(self,request):
        plans = SubscriptionPlanTrainer.objects.all()
        return render(request,'subscription/subscription_plan.html',{'plans':plans})

class BuySubscription(TrainerRequiredMixin,View):
    
    def get_or_create_subscription_data(self,request,plan_id):
        """
        
        This method is use to get or create subscription if doesn't exist one based on plan & status of subscription  
        
        """
        trainer_instance= get_object_or_404(Trainer,user=request.user)
        plan_instance= get_object_or_404(SubscriptionPlanTrainer,id=plan_id)
        print("===================>",trainer_instance)
        
        subscriber_info=SubscribedTrainer.objects.filter(trainer=trainer_instance,plan=plan_instance)
        for sub in subscriber_info:
            
            if sub.subscription_status == 'Active':
                message.warning(request, 'Subscription already exist & its active')
                created = False
                print(f"====================>data from get oe create    trainer_instance:{trainer_instance} \n plan_instance:{plan_instance} \n subscriber_info:{sub} \n created:{created}")
                return trainer_instance,plan_instance,sub,created
            elif sub.subscription_status == 'Pending':
                created = False
                print(f"====================>data from get oe create    trainer_instance:{trainer_instance} \n plan_instance:{plan_instance} \n subscriber_info:{sub} \n created:{created}")
                return trainer_instance,plan_instance,sub,created
            else:
                sub = SubscribedTrainer.objects.create(trainer=trainer_instance,plan=plan_instance,subscription_status='Pending')
                created = True
                print(f"====================>data from get oe create    trainer_instance:{trainer_instance} \n plan_instance:{plan_instance} \n subscriber_info:{sub} \n created:{created}")
                return trainer_instance,plan_instance,subscriber_info,created
        return trainer_instance,plan_instance,subscriber_info,created
        
    def get(self,request,plan_id):
        """
        
        Handles get request and calls get_or_create_subscription_data for creating or retrieving subscribed trainer object
        
        """
        data = self.get_or_create_subscription_data(request,plan_id)
        
        trainer_instance,plan_instance,subscriber_info,created = data
        
        print(f"====================>data from get     trainer_instance:{trainer_instance} \n plan_instance:{plan_instance} \n subscriber_info:{subscriber_info} \n created:{created}")
        
        if created:
            message.success(request, 'Subscription created successfully')
        else:
            message.error(request, 'Subscription already exists, retrieved last pending payment')
            
        return render(request,"subscription/subscription_buy.html",{'subscriber_info':subscriber_info})
    
    def post(self,request,plan_id):
        """
        
        handles post request, Mainly it handles the logic of order creation & razor pay validation
        
        """
        print("=================>",plan_id)
        data = self.get_or_create_subscription_data(request,plan_id)
        
        trainer_instance,plan_instance,subscriber_info,created = data        
        client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))
        print(f"======================> {settings.RAZORPAY_KEY_ID} and {settings.RAZORPAY_KEY_SECRET}",)
        
        # generating unique id for receipt
        receipt_id = f"r_{subscriber_info.id}_{uuid.uuid4().hex}"
        
        # payment details such as amount and receipt 
        data  = {
            "amount": int(subscriber_info.plan.price*100),
            "currency": "INR",
            "receipt": receipt_id,
            "payment_capture": 1
        }
        #generating payment order for razor_pay
        payment = client.order.create(data=data )
        subscriber_info.payment_id = payment.get('id')
        print("=======================>",payment.get('id'))
        print("=======================>",subscriber_info.payment_id)
        print("=======================>",data)
        subscriber_info.save()
        
        return render(request,"subscription/payment.html",{'subscriber_info':subscriber_info,'payment':payment,'data':data})


@csrf_exempt
def success(request):
    if request.method == "POST":
        print("=================> post method of success")
        try :
            print("==================> try block")
            client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))

            client.utility.verify_payment_signature({
                'razorpay_order_id': request.POST.get("razorpay_order_id"),
                'razorpay_payment_id':request.POST.get("razorpay_payment_id"),
                'razorpay_signature': request.POST.get("razorpay_signature")
            })
            order_id = request.POST.get("razorpay_order_id")
            payment_id = request.POST.get("razorpay_payment_id")
            
            Subscriber_info = SubscribedTrainer.objects.get(payment_id=order_id)
            Subscriber_info.payment_id = payment_id
            Subscriber_info.subscription_status = 'Active'
            Subscriber_info.subscription_date = datetime.now()
            Subscriber_info.termination_date = datetime.now() + timedelta(days=30)
            
            
            payment_instance = PaymentRecord.objects.create(
                payment_id=payment_id,
                payment_signature=request.POST.get('razorpay_signature'),
                user= request.user,
                amount = Subscriber_info.plan.price,
                status = 'completed',
                method = 'Razor Pay'
            )
            Subscriber_info.save()
            return render(request,'subscription/success.html')
        except razorpay.errors.SignatureVerificationError:
            print("====================> signature verification failed")
            return HttpResponseBadRequest("Signature verification failed")
    else :
        return HttpResponseBadRequest("INVALID REQUEST")
    
    
    