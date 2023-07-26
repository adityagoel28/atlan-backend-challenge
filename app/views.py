from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response as APIResponse
from app.models import *

# Create your views here.
def home(request):
    return APIResponse("Home", status=200)

class HealthCheck(APIView):
    def get(self, request):
        return APIResponse("Health OK", status=200)
    
