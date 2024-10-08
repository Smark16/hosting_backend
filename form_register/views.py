from django.shortcuts import render
from django.shortcuts import render
from django.http import JsonResponse
from django.http import HttpResponse, FileResponse
from rest_framework.response import Response
from rest_framework import generics
from .models import *
from rest_framework.views import APIView
from .serializers import *
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import *
from rest_framework import status
from django.views.decorators.csrf import csrf_exempt
from rest_framework import viewsets
from rest_framework.parsers import MultiPartParser, FormParser
from datetime import date
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from rest_framework.permissions import BasePermission
from django.http import FileResponse, Http404
from collections import defaultdict
from .models import User
from rest_framework.authentication import TokenAuthentication
import logging
import os
from django.conf import settings
from django.utils.dateparse import parse_duration
from django.db.models import Avg
from rest_framework.parsers import MultiPartParser, FormParser
from django.core.mail import send_mail
from django.conf import settings

# Create your views here.
class ObtainPairView(TokenObtainPairView):
    serializer_class = ObtainSerializer

class AllUsers(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class registrationView(generics.CreateAPIView):
    queryset = UserAccount.objects.all()
    permission_classes = [AllowAny]
    serializer_class = RegisterSerializer

class getUser(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class updateUser(generics.UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return get_object_or_404(User, pk=self.kwargs["pk"])
    
    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.serializer_class(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)


# basic info view
class AllBasic(generics.ListAPIView):
    queryset = BasicInformation.objects.all()
    serializer_class = basicSerializer

class post_basic(APIView):
    queryset = BasicInformation.objects.all()
    serializer_class = basicSerializer

    def post(self, request, format=None):
        user = request.data.get('user')
        if BasicInformation.objects.filter(user=user).exists():
            return Response({"error": "Basic information already exists for this user."}, status=status.HTTP_400_BAD_REQUEST)
        
        serializers = basicSerializer(data=request.data)
        if serializers.is_valid():
            serializers.save()
            return Response(serializers.data, status=status.HTTP_201_CREATED)
        return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def retrieveBasic(request, user):
    try:
        basic = BasicInformation.objects.get(user=user)
    except BasicInformation.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        serializer = basicSerializer(basic)
        return Response(serializer.data)
    

class updateBasic(APIView):
    serializer_class = basicSerializer

    def get_object(self, user_id):
        try:
            return BasicInformation.objects.get(user=user_id)
        except BasicInformation.DoesNotExist:
            return None

    def put(self, request, user_id):
        instance = self.get_object(user_id)
        if not instance:
            return Response({"error": "Basic information not found for this user."}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = self.serializer_class(instance, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
# physical Address views
class AllPhysicalAdress(generics.ListAPIView):
    queryset = PhysicalAddress.objects.all()
    serializer_class = PhysicalSerializer

class postPhysical(APIView):
    queryset = PhysicalAddress.objects.all()
    serializer_class = PhysicalSerializer

    def post(self, request, format=None):
        user = request.data.get("user")
        if PhysicalAddress.objects.filter(user=user).exists():
            return Response({"error":"Physical Address Arleady Exists"}, status=status.HTTP_400_BAD_REQUEST)
        serializers = PhysicalSerializer(data=request.data)
        if serializers.is_valid():
            serializers.save()
            return Response(serializers.data, status=status.HTTP_201_CREATED)
        return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def retrievePhysical(request, user):
    try:
        basic = PhysicalAddress.objects.get(user=user)
    except PhysicalAddress.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        serializer = PhysicalSerializer(basic)
        return Response(serializer.data)
    
class updatePhysical(APIView):
    serializer_class = PhysicalSerializer

    def get_object(self, user_id):
        try:
            return PhysicalAddress.objects.get(user=user_id)
        except PhysicalAddress.DoesNotExist:
            return None

    def put(self, request, user_id):
        instance = self.get_object(user_id)
        if not instance:
            return Response({"error": "Basic information not found for this user."}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = self.serializer_class(instance, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# capacity views
class AllCapacity(generics.ListAPIView):
    queryset = Capacity.objects.all()
    serializer_class = CapacitySerializer
    parser_classes = [MultiPartParser, FormParser]
    permission_classes = [AllowAny]

class post_Capacity(APIView):
    serializer_class = CapacitySerializer

    def post(self, request, format=None):
        user = request.data.get("user")
        if Capacity.objects.filter(user=user).exists():
            return Response({"error":"This Credential Arleady Exists!"}, status=status.HTTP_400_BAD_REQUEST)
        serializers = CapacitySerializer(data=request.data)
        if serializers.is_valid():
            serializers.save()
            return Response(serializers.data, status=status.HTTP_201_CREATED)
        return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)
    

@api_view(['GET'])
def retrieveCapacity(request, user):
    try:
        basic = Capacity.objects.get(user=user)
    except Capacity.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        serializer = CapacitySerializer(basic)
        return Response(serializer.data)
    
class updateCapacity(APIView):
    serializer_class = CapacitySerializer
    parser_classes = [MultiPartParser, FormParser]
    permission_classes = [AllowAny]

    def get_object(self, user_id):
        try:
            return Capacity.objects.get(user=user_id)
        except Capacity.DoesNotExist:
            return None

    def put(self, request, user_id):
        instance = self.get_object(user_id)
        if not instance:
            return Response({"error": "Basic information not found for this user."}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = self.serializer_class(instance, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
  
    
# eduction view
class AllEducation(generics.ListAPIView):
    queryset = EducationCount.objects.all()
    serializer_class = EducationSerializer

class post_Education(APIView):
    serializer_class = EducationSerializer

    def post(self, request, format=None):
        user = request.data.get("user")
        if EducationCount.objects.filter(user=user).exists():
           return Response({"error":"This Credential Arleady Exists!"}, status=status.HTTP_400_BAD_REQUEST)
        serializers = EducationSerializer(data=request.data)
        if serializers.is_valid():
            serializers.save()
            return Response(serializers.data, status=status.HTTP_201_CREATED)
        return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)
    

@api_view(['GET'])
def retrieveEducation(request, user):
    try:
        basic = EducationCount.objects.get(user=user)
    except EducationCount.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        serializer = EducationSerializer(basic)
        return Response(serializer.data)
    
class updateEducation(APIView):
    serializer_class = EducationSerializer

    def get_object(self, user_id):
        try:
            return EducationCount.objects.get(user=user_id)
        except EducationCount.DoesNotExist:
            return None

    def put(self, request, user_id):
        instance = self.get_object(user_id)
        if not instance:
            return Response({"error": "Basic information not found for this user."}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = self.serializer_class(instance, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
  

class CategoryView(generics.ListAPIView):
    queryset = EmployeeCategory.objects.all()
    serializer_class = CategorySerializer

class postCategory(APIView):
    serializer_class = CategorySerializer

    def post(self, request, format=None):
        user = request.data.get("user")
        if EmployeeCategory.objects.filter(user=user).exists():
           return Response({"error":"You Arleady Provided these Details!"}, status=status.HTTP_400_BAD_REQUEST)
        serializers = CategorySerializer(data=request.data)
        if serializers.is_valid():
            serializers.save()
            return Response(serializers.data, status=status.HTTP_201_CREATED)
        return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)
    

@api_view(['GET'])
def retrieveCategory(request, user):
    try:
        basic = EmployeeCategory.objects.get(user=user)
    except EmployeeCategory.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        serializer = CategorySerializer(basic)
        return Response(serializer.data)
    
class updateCategory(APIView):
    serializer_class = CategorySerializer

    def get_object(self, user_id):
        try:
            return EmployeeCategory.objects.get(user=user_id)
        except EmployeeCategory.DoesNotExist:
            return None

    def put(self, request, user_id):
        instance = self.get_object(user_id)
        if not instance:
            return Response({"error": "Basic information not found for this user."}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = self.serializer_class(instance, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
  

# trade views
class TradeCreate(generics.CreateAPIView):
    queryset = Trade.objects.all()
    serializer_class = TradeSerializer

class postTrade(APIView):
    serializer_class = TradeSerializer

    def post(self, request, format=None):
        user = request.data.get("user")
        if Trade.objects.filter(user=user).exists():
           return Response({"error":"You Arleady Provided these Details!"}, status=status.HTTP_400_BAD_REQUEST)
        serializers = TradeSerializer(data=request.data)
        if serializers.is_valid():
            serializers.save()
            return Response(serializers.data, status=status.HTTP_201_CREATED)
        return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['GET'])
def retrieveTrade(request, user):
    try:
        basic = Trade.objects.get(user=user)
    except Trade.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        serializer = TradeSerializer(basic)
        return Response(serializer.data)
    
class updateTrade(APIView):
    serializer_class = TradeSerializer

    def get_object(self, user_id):
        try:
            return Trade.objects.get(user=user_id)
        except Trade.DoesNotExist:
            return None

    def put(self, request, user_id):
        instance = self.get_object(user_id)
        if not instance:
            return Response({"error": "Basic information not found for this user."}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = self.serializer_class(instance, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# hosting experience
class AllHosted(generics.ListAPIView):
    queryset = HostingExperience.objects.all()
    serializer_class = HostingExperienceSerializer

class HostingExperienceCreateView(APIView):
    serializer_class = HostingExperienceSerializer

    def post(self, request, format=None):
        user = request.data.get("user")
        if HostingExperience.objects.filter(user=user).exists():
           return Response({"error":"You Arleady Provided these Details!"}, status=status.HTTP_400_BAD_REQUEST)
        serializers = HostingExperienceSerializer(data=request.data)
        if serializers.is_valid():
            serializers.save()
            return Response(serializers.data, status=status.HTTP_201_CREATED)
        return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)
    

@api_view(['GET'])
def retrieveHosted(request, user):
    try:
        basic = HostingExperience.objects.get(user=user)
    except HostingExperience.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        serializer = HostingExperienceSerializer(basic)
        return Response(serializer.data)
    
class UpdateHost(APIView):
    serializer_class = HostingExperienceSerializer

    def get_object(self, user_id):
        try:
            return HostingExperience.objects.get(user=user_id)
        except HostingExperience.DoesNotExist:
            return None

    def put(self, request, user_id):
        instance = self.get_object(user_id)
        if not instance:
            return Response({"error": "Basic information not found for this user."}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = self.serializer_class(instance, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Additionamal view
class AdditionalView(generics.ListAPIView):
    queryset = AdditionalInformation
    serializer_class = AdditionalSerializer

class postMore(APIView):
    serializer_class = AdditionalSerializer

    def post(self, request, format=None):
        user = request.data.get("user")
        if AdditionalInformation.objects.filter(user=user).exists():
            return Response({"error":"You Already Provided these Details!"}, status=status.HTTP_400_BAD_REQUEST)
        serializers = AdditionalSerializer(data=request.data)
        if serializers.is_valid():
            additional_info = serializers.save()
            send_welcome_email(additional_info.user)  # Pass the actual user object
            return Response(serializers.data, status=status.HTTP_201_CREATED)
        return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST) 
    
@api_view(['GET'])
def retrieveAdd(request, user):
    try:
        basic = AdditionalInformation.objects.get(user=user)
    except AdditionalInformation.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        serializer = AdditionalSerializer(basic)
        return Response(serializer.data)
    
class updateAdd(APIView):
    serializer_class = AdditionalSerializer

    def get_object(self, user_id):
        try:
            return AdditionalInformation.objects.get(user=user_id)
        except AdditionalInformation.DoesNotExist:
            return None

    def put(self, request, user_id):
        instance = self.get_object(user_id)
        if not instance:
            return Response({"error": "Basic information not found for this user."}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = self.serializer_class(instance, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# change password
class ChangePasswordView(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user

    def put(self, request, *args, **kwargs):
        user = self.get_object()
        serializer = ChangePasswordSerializer(data=request.data, context={'request': request})

        if serializer.is_valid():
            serializer.update(user, serializer.validated_data)
            return Response({"message": "Password updated successfully"}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
def send_welcome_email(user):
    subject = "Welcome to Grow"
    message = f"Dear {user.first_name},\n\nWelcome to Grow. Your Application has beeen successfully received thank you for applying with GROW we promise you all the best."
    from_email = settings.EMAIL_HOST_USER
    to_email = [user.email]
    send_mail(subject, message, from_email, to_email, fail_silently=False)

    
@api_view(['GET'])
def retrieveUserInfo(request, pk):
    try:
        user_info = BasicInformation.objects.get(user=pk)
    except BasicInformation.DoesNotExist:
        return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

    serializer = UserInfoSerializer(user_info)
    return Response(serializer.data)

class AllFiles(generics.ListAPIView):
    queryset = Files.objects.all()
    serializer_class = FileSerializer

class UploadFile(APIView):
    permission_classes = [AllowAny]
    parser_classes = [MultiPartParser, FormParser]

    def post(self, request, format=None):
        user = request.data.get("user")
        if Files.objects.filter(user=user).exists():
            return Response({"error":"You Already uploaded a file!"}, status=status.HTTP_400_BAD_REQUEST)
        serializer = FileSerializer(data=request.data)
        if serializer.is_valid():
            file_instance = serializer.save()
            file_url = request.build_absolute_uri(file_instance.name.url)
            return Response({
                "file_id": file_instance.id,
                "file_url": file_url
            }, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
class updateFile(APIView):
    serializer_class = FileSerializer

    def get_object(self, user_id):
        try:
            return Files.objects.get(user=user_id)
        except Files.DoesNotExist:
            return None

    def put(self, request, user_id):
        instance = self.get_object(user_id)
        if not instance:
            return Response({"error": "Basic information not found for this user."}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = self.serializer_class(instance, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def retrieve_File(request, user):
    try:
       file = Files.objects.get(user=user)
    except Files.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        serializer = FileSerializer(file)
        return Response(serializer.data)
    
#Enviroment
class EnvironmentView(generics.ListAPIView):
    queryset = Environment
    serializer_class = EnvironmentSerializer

class postEnvironment(APIView):
    serializer_class = EnvironmentSerializer

    def post(self, request, format=None):
        user = request.data.get("user")
        if Environment.objects.filter(user=user).exists():
            return Response({"error":"You Already Provided these Details!"}, status=status.HTTP_400_BAD_REQUEST)
        serializers = EnvironmentSerializer(data=request.data)
        if serializers.is_valid():
            serializers.save()
            return Response(serializers.data, status=status.HTTP_201_CREATED)
        return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST) 
    
@api_view(['GET'])
def retrieveEnv(request, user):
    try:
        basic = Environment.objects.get(user=user)
    except Environment.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        serializer = EnvironmentSerializer(basic)
        return Response(serializer.data)
    
class updateEnv(APIView):
    serializer_class = EnvironmentSerializer

    def get_object(self, user_id):
        try:
            return Environment.objects.get(user=user_id)
        except Environment.DoesNotExist:
            return None

    def put(self, request, user_id):
        instance = self.get_object(user_id)
        if not instance:
            return Response({"error": "Information not found for this user."}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = self.serializer_class(instance, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class AgricultureListView(generics.ListCreateAPIView):
    queryset = Agriculture.objects.all()
    serializer_class = AgricultureSerializer

class AgroProcessingListView(generics.ListCreateAPIView):
    queryset = AgroProcessing.objects.all()
    serializer_class = AgroProcessingSerializer

class Creative_and_Performing_ArtListView(generics.ListCreateAPIView):
    queryset = Creative_and_Performing_Art.objects.all()
    serializer_class = Creative_and_Performing_ArtSerializer

class Hotel_and_HospitalityListView(generics.ListCreateAPIView):
    queryset = Hotel_and_Hospitality.objects.all()
    serializer_class = Hotel_and_HospitalitySerializer

class Beauty_and_CosmetologyListView(generics.ListCreateAPIView):
    queryset = Beauty_and_Cosmetology.objects.all()
    serializer_class = Beauty_and_CosmetologySerializer

class ManufacturingListView(generics.ListCreateAPIView):
    queryset = Manufacturing.objects.all()
    serializer_class = ManufacturingSerializer

class ConstructionListView(generics.ListCreateAPIView):
    queryset = Construction.objects.all()
    serializer_class = ConstructionSerializer

class Food_ProcessingListView(generics.ListCreateAPIView):
    queryset = Food_Processing.objects.all()
    serializer_class = Food_ProcessingSerializer

class Social_ServicesListView(generics.ListCreateAPIView):
    queryset = Social_Services.objects.all()
    serializer_class = Social_ServicesSerializer

class Professional_TechnicalServicesListView(generics.ListCreateAPIView):
    queryset = Professional_TechnicalServices.objects.all()
    serializer_class = Professional_TechnicalServicesSerializer

class EngineeringListView(generics.ListCreateAPIView):
    queryset = Engineering.objects.all()
    serializer_class = EngineeringSerializer

class Tourism_and_HospitalityListView(generics.ListCreateAPIView):
    queryset = Tourism_and_Hospitality.objects.all()
    serializer_class = Tourism_and_HospitalitySerializer

class Environment_ProtectionListView(generics.ListCreateAPIView):
    queryset = Environment_Protection.objects.all()
    serializer_class = Environment_ProtectionSerializer
    

class FishingListView(generics.ListCreateAPIView):
    queryset = Fishing.objects.all()
    serializer_class = FishingSerializer

class ICT_and_DigitalMediaListView(generics.ListCreateAPIView):
    queryset = ICT_and_DigitalMedia.objects.all()
    serializer_class = ICT_and_DigitalMediaSerializer

class TradeRetail_and_WholesaleListView(generics.ListCreateAPIView):
    queryset = TradeRetail_and_Wholesale.objects.all()
    serializer_class = TradeRetail_and_WholesaleSerializer

class MechanicalListView(generics.ListCreateAPIView):
    queryset = Mechanical.objects.all()
    serializer_class = MechanicalSerializer

class Tailoring_and_TextilesListView(generics.ListCreateAPIView):
    queryset = Tailoring_and_Textiles.objects.all()
    serializer_class = Tailoring_and_TextilesSerializer

class finished(generics.ListAPIView):
    queryset = Finish.objects.all()
    serializer_class = FinishSerialier
