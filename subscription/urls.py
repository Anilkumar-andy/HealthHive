from django.urls import path 
from .views import SubscriptionPlan,BuySubscription,success

urlpatterns=[
    path('plans/',SubscriptionPlan.as_view(),name='subscription_plans'),
    path('buy/<int:plan_id>',BuySubscription.as_view(),name='buy_subscription'),
    path('payment_success/',success,name='payment_successful'),
]