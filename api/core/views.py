from rest_framework.response import Response
from rest_framework.views import APIView

from api.core.tasks import email_task


class CeleryTaskView(APIView):
    def get(self, request):
        email_task.delay()
        resp_json = {"message": "calling celery task"}
        return Response(resp_json)
