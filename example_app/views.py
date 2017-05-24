from django.http import HttpResponse
from rest_framework import schemas
from rest_framework import response
from rest_framework import permissions
from rest_framework.decorators import api_view
from rest_framework.decorators import renderer_classes
from rest_framework.decorators import permission_classes
from rest_framework.views import APIView
from rest_framework_swagger.renderers import OpenAPIRenderer
from rest_framework_swagger.renderers import SwaggerUIRenderer


@permission_classes((permissions.AllowAny,))
class HelloWorld(APIView):

    def get(self, request):
        # <view logic>
        return HttpResponse(content='hello world !', status=200)


@api_view()
@renderer_classes([OpenAPIRenderer, SwaggerUIRenderer])
@permission_classes((permissions.AllowAny,))
def schema_view(request):
    generator = schemas.SchemaGenerator(title='Example Application API Documentation')
    return response.Response(generator.get_schema(request=request))
