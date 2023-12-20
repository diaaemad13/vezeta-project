from ast import Not
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from .models import Profile
from .forms import Login_Form , UpdateUserForm , UserCreationForms , UpdateProfileForm
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required

# Create your views here.


def doctor_list(request):
    doctors = User.objects.all()
    return render(request, 'users/doctor_list.html', {
        'doctors' : doctors,})

def doctors_detail(request, slug):
    doctors_detail = Profile.objects.get(slug = slug)
    return render(request, 'users/doctors_detail.html', {'doctors_detail': doctors_detail})

def user_login(request):
    if request.method == 'POST':
        form = Login_Form()
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username , password=password)
        if user is not None:
            login(request , user)
            return redirect('accounts:doctor_list')
    else:
        form = Login_Form()

    return render(request, 'users/login.html', {'form': form})

@login_required()
def my_profile(request):
    return render(request, 'users/myprofile.html', {})


def update_profile(request):
    user_form = UpdateUserForm(instance=request.user)
    profile_form = UpdateProfileForm(instance=request.user.profile) 
    if request.method == 'POST':
        user_form = UpdateUserForm(request.POST, instance=request.user)
        profile_form = UpdateProfileForm(request.POST, instance=request.user.profile) 
        if user_form.is_valid and profile_form.is_valid:
            user_form.save()
            profile_form.save()
            return redirect('accounts:doctor_list')

    return render(request, 'users/update_profile.html', {'user_form':user_form, 'profile_form':profile_form})


def signup(request):
    if request.method == 'POST':
        form = UserCreationForms(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username , password=password)
            login(request , user)
            return redirect('accounts:doctor_list')
    else:
        form = UserCreationForms()
    return render(request, 'users/signup.html', {'form':form})
#########################################################################################
    
from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework import status
from django.shortcuts import get_object_or_404
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from .models import Profile
from .serializers import UserSerializer, ProfileSerializer, UserCreationSerializer
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

# Import your serializers, UpdateUserForm, and UpdateProfileForm here

@api_view(['POST'])
def user_login_api(request):
    if request.method == 'POST':
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return Response({'detail': 'Login successful'}, status=status.HTTP_200_OK)
        else:
            return Response({'detail': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def my_profile_api(request):
    serializer = UserSerializer(request.user)
    return Response(serializer.data)

@api_view(['PUT'])
@permission_classes([permissions.IsAuthenticated])
def update_profile_api(request):
    user = request.user
    user_serializer = UserSerializer(user, data=request.data, partial=True)
    profile_serializer = ProfileSerializer(user.profile, data=request.data.get('profile'), partial=True)

    if user_serializer.is_valid() and profile_serializer.is_valid():
        user_serializer.save()
        profile_serializer.save()
        return Response({'detail': 'Profile updated successfully'}, status=status.HTTP_200_OK)
    else:
        return Response({'detail': 'Invalid data'}, status=status.HTTP_400_BAD_REQUEST)

class DoctorListView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class DoctorDetailView(generics.RetrieveAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    lookup_field = 'slug'

@method_decorator(csrf_exempt, name='dispatch')
class SignupView(generics.CreateAPIView):
    serializer_class = UserCreationSerializer
    permission_classes = [permissions.AllowAny]

    def perform_create(self, serializer):
        user = serializer.save()
        login(self.request, user)