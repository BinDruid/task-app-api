from rest_framework.response import Response
from rest_framework.generics import GenericAPIView
from celery.result import AsyncResult

from api.core.tasks import send_single_email


class CeleryTaskView(GenericAPIView):

    def get(self, request, pk):
        task_result = AsyncResult(pk)
        result = {
            "task_id": pk,
            "task_status": task_result.status,
            "task_result": task_result.result
        }
        return Response(result, status=200)

    def post(self, request):
        task = send_single_email.delay()
        resp_json = {"message": f"calling celery task with id: {task.id}"}
        return Response(resp_json)


