from rest_framework import generics, permissions
from rest_framework.response import Response
from .models import Notification

class NotificationListView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        notifications = Notification.objects.filter(recipient=request.user).order_by('-timestamp')
        data = [{
            'actor': n.actor.username,
            'verb': n.verb,
            'target': str(n.target),
            'timestamp': n.timestamp,
            'read': n.read,
        } for n in notifications]
        return Response(data)
