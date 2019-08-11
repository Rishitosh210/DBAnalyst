from audtech_app.serializers import UserSerializer
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from rest_framework import generics
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response


@api_view(['POST'])
def login_view(request):
    username = request.data.get("username")
    password = request.data.get("password")
    user = authenticate(username=username, password=password)
    print(user)
    if user:
        login(request, user)
        return Response(f"working properly{request.user}", status=status.HTTP_201_CREATED)

    return Response({"error": "unknown"}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def logout_view(request):
    logout(request)
    return Response("logout", status=status.HTTP_200_OK)


class UserList(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserUpdate(generics.RetrieveUpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserDetail(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserDelete(generics.RetrieveDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

# import io
#
# @api_view(['POST'])
# def process_file(request):
#     s = str(request.body, 'utf-8')
#     data = io.StringIO(s)
#     df = pd.read_csv(data)
#     return Response("sss", status=status.HTTP_201_CREATED)
