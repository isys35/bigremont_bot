import json

from django.conf import settings
from django.core.handlers.wsgi import WSGIRequest
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from pydantic import ValidationError

from bigremont_app.bot.bot import Bot
from bigremont_app.bot.router import Router
from bigremont_app.bot.telegram_context import TelegramContext
from bigremont_app.bot.urls import urls
from bigremont_app.serializers import UpdateTelegramSerializer


@csrf_exempt
@require_http_methods(["POST"])
def webhook(request: WSGIRequest):
    json_data = json.loads(request.body)
    try:
        update = UpdateTelegramSerializer(**json_data)
    except ValidationError as e:
        error_data = json.loads(e.json())
        return JsonResponse(data=error_data, status=400, safe=False)
    telegram_context = TelegramContext(settings.TELEGRAM_TOKEN)
    bot = Bot(telegram_context, update)
    router = Router(urls)
    router.url_dispatcher(bot)
    return JsonResponse(data={"success": True}, status=200)