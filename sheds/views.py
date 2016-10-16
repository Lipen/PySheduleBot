from django.shortcuts import render
from django.http import HttpResponseForbidden, HttpResponseBadRequest, JsonResponse
from django.template import loader
from django.views.generic import View

from sheds.models import Day, Lesson

import datetime
import json
import telepot

token = '294289451:AAEjcnW1o4b4zsJTGI9MG46z4cock-sWC_M'
TelegramBot = telepot.Bot(token)
weekdays = ['Понедельник', 'Вторник', 'Среда', 'Четверг', 'Пятница', 'Суббота', 'Воскресенье']
weekdays_b = ['Понедельник', 'Вторник', 'Среду', 'Четверг', 'Пятницу', 'Субботу', 'Воскресенье']


def index(request, **kwargs):
    weekday = kwargs.get('day')

    if weekday == 'today':
        context = {
            'title': 'Расписание на сегодня',
            'days_list': Day.objects.filter(weekday=weekday)
        }
    elif weekday == 'all':
        context = {
            'title': 'Расписание',
            'days_list': Day.objects.all()
        }
    else:
        try:
            dayname = weekdays_b[int(weekday)]
        except:
            dayname = weekdays_b[datetime.datetime.now().weekday()]

        context = {
            'title': 'Расписание на {}'.format(dayname.lower()),
            'days_list': Day.objects.filter(weekday=weekday)
        }

    return render(request, 'sheds/index.html', context)


def tbotcmd_start(*args):
    return loader.render_to_string('sheds/start.md')


def tbotcmd_help(*args):
    return loader.render_to_string('sheds/help.md')


def tbotcmd_schedule(weekday):
    if weekday == 'today':
        context = {
            'title': 'Расписание на сегодня',
            'days_list': Day.objects.filter(weekday=weekday)
        }
    elif weekday == 'all':
        context = {
            'title': 'Расписание',
            'days_list': Day.objects.all()
        }
    else:
        try:
            dayname = weekdays_b[int(weekday)]
        except:
            dayname = weekdays_b[datetime.datetime.now().weekday()]

        context = {
            'title': 'Расписание на {}'.format(dayname.lower()),
            'days_list': Day.objects.filter(weekday=weekday)
        }

    return loader.render_to_string('sheds/schedule.md', context)


class TelegramBotReceiverView(View):

    def post(self, request, bot_token):
        if bot_token != token:
            return HttpResponseForbidden('Invalid token')

        raw = request.body.decode('utf-8')
        # logger.info(raw)
        try:
            payload = json.loads(raw)
        except ValueError:
            return HttpResponseBadRequest('Invalid request body')
        else:
            msg = payload['message']
            chat_id = msg['chat']['id']
            cmd = msg.get('text')

            if cmd == '/start':
                TelegramBot.sendMessage(chat_id, tbotcmd_start(), parse_mode='Markdown')
            elif cmd == '/help':
                TelegramBot.sendMessage(chat_id, tbotcmd_help(), parse_mode='Markdown')
            else:
                cmd_name, *cmd_args = cmd.split()
                if cmd_name == 'schedule':
                    TelegramBot.sendMessage(chat_id, tbotcmd_schedule(*cmd_args), parse_mode='Markdown')
                else:
                    TelegramBot.sendMessage(chat_id, 'I do not understand you, Sir!')

        return JsonResponse({}, status=200)

    # return HttpResponse(template.render(context, request))

    # str_telegrambot = '<h3>>> TelegramBot</h3>'
    # for k, v in TelegramBot.getMe().items():
    #     str_telegrambot += '<p>[*] {}: {}</p>'.format(k, v)

    # updates = TelegramBot.getUpdates()
    # messages = []
    # for upd in updates:
    #     if 'message' in upd:
    #         msg = upd['message']
    #         name = msg['from']['username']
    #         text = msg['text']
    #         timestamp = msg['date']
    #         messages.append((name, text, timestamp))

    # str_messages = '<h3>>> Telegram messages</h3>'
    # for name, text, timestamp in messages:
    #     str_messages += '<p>[{time}]@{name}: {text}</p>'.format(time=datetime.datetime.fromtimestamp(timestamp).strftime('%H:%M:%S'), name=name, text=text)

    # return HttpResponse(str_days + str_telegrambot + str_messages)
