from rest_framework import generics, permissions
from tickerapp.models import User, Ticker
from .serializers import UserSerializer, TickerSerializer


class UserListView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAdminUser]


class UserDetailView(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        if self.request.user.is_staff:
            user_id = self.kwargs.get('pk')
            return User.objects.get(pk=user_id)
        return self.request.user

class TickerListView(generics.ListAPIView):
    queryset = Ticker.objects.all()
    serializer_class = TickerSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class TickerDetailView(generics.RetrieveAPIView):
    queryset = Ticker.objects.all()
    serializer_class = TickerSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]   
    