from rest_framework.response import Response
from rest_framework.views import APIView

from api.core.tasks import email_task


class CeleryTaskView(APIView):
    def post(self, request):
        task = email_task.delay()
        resp_json = {"message": f"calling celery task with id:{task.id}"}
        return Response(resp_json)
