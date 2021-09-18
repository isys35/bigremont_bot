import json

from django.core.handlers.wsgi import WSGIRequest
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods


@csrf_exempt
@require_http_methods(["POST"])
def webhook(request: WSGIRequest):
    json_data = json.loads(request.body)
    return JsonResponse(data=json_data, status=200)

# class WebHook(APIView):
#     """
#     Вебхук для телеграмма
#     """
#     serializer_class = UpdateSerializer
#     permission_classes = [AllowAny]
#
#     def post(self, request):
#         serializer = self.serializer_class(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         if not serializer.data.get('message') and not serializer.data.get('callback_query'):
#             return Response({"success": False, 'error':'Not message' }, status=status.HTTP_400_BAD_REQUEST)
#         telegram_context = TelegramContext(settings.TELEGRAM_TOKEN)
#         bot = Bot(telegram_context, serializer)
#         router = Router(urls)
#         router.url_dispatcher(bot)
#         return Response({"success": True}, status=status.HTTP_200_OK)
