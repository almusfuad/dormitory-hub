from django.views.decorators.csrf import csrf_exempt
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from django.http import HttpResponse

schema_view = get_schema_view(
      openapi.Info(
            title="Dormitory API",
            default_version = 'v1'
      ),
      public=True
)


def swagger_ui_view(request):
     response = schema_view.with_ui('swagger', cache_timeout=0)(request)
     response.delete_cookie('csrftoken')
     return response