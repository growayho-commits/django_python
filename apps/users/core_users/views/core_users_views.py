from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from apps.users.core_users.serializers.core_users_serializer import UserRegistrationSerializer, UserProfileSerializer
from apps.users.core_users.models import CustomUser
from django.contrib.auth import authenticate
from django.shortcuts import render

class SignUpAPIView(APIView):
    """Handles User Sign Up / Registration"""
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({
                "message": "User registered successfully!",
                "user_id": user.id,
                "email": user.email,
                "role": user.role
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SignInAPIView(APIView):
    """Handles User Sign In / Login and returns JWT tokens"""
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get("email")
        password = request.data.get("password")
        
        user = authenticate(email=email, password=password)
        if user is not None and user.is_active:
            refresh = RefreshToken.for_user(user)
            return Response({
                "message": "Signed in successfully!",
                "refresh": str(refresh),
                "access": str(refresh.access_token),
                "email": user.email,
                "role": user.role
            }, status=status.HTTP_200_OK)
        
        return Response({"error": "Invalid email or password"}, status=status.HTTP_401_UNAUTHORIZED)


class SignOutAPIView(APIView):
    """Handles User Sign Out / Logout by blacklisting the refresh token"""
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.data.get("refresh")
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({"message": "Signed out successfully!"}, status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response({"error": "Invalid token or token missing"}, status=status.HTTP_400_BAD_REQUEST)


class UserDetailAPIView(APIView):
    """Fetches logged-in user profile"""
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        profile = UserSelector.get_user_profile(user)
        return Response({
            "email": user.email,
            "role": user.role,
            "profile": UserProfileSerializer(profile).data
        }, status=status.HTTP_200_OK)


class AuthPageView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        return render(request, 'core_users/signup.html')