from rest_framework.views import APIView
from rest_framework.reverse import reverse
from rest_framework.response import Response


class ApiRootView(APIView):
    """
    Lists currently avaiable endpoints.
    """

    def get(self, request, format=None):
        return Response(
            {
                "tasks": reverse("tasks", request=request, format=format),
            }
        )
