from rest_framework.views import APIView
from rest_framework.response import Response
from school.models import Notification

class NotificationListView(APIView):
    view_permissions = {
        'get': {'teacher': True, 'admin': True, 'student': True},
        'post': {'student': True}
    }

    def get(self, request):
        notifications = request.user.notifications.filter(is_read=False)
        return Response(
            [{"id": n.id, "message": n.message, "created_at": n.created_at} for n in notifications]
        )

    def post(self, request): 
        ids = request.data.get("ids", [])
        Notification.objects.filter(id__in=ids, user=request.user).update(is_read=True)
        return Response({"message": "Notifications marked as read"})