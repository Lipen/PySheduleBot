from django.shortcuts import render
from django.http import HttpResponseForbidden, HttpResponseBadRequest, JsonResponse
from django.template import loader
from django.views.generic import View
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

from .models import Day

import datetime
import json
import telepot
import logging

token = '294289451:AAEjcnW1o4b4zsJTGI9MG46z4cock-sWC_M'
TelegramBot = telepot.Bot(token)
weekdays_ru = ['понедельник', 'вторник', 'среда', 'четверг', 'пятница', 'суббота', 'воскресенье']
weekdays_en = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
weekdays_b = ['Понедельник', 'Вторник', 'Среду', 'Четверг', 'Пятницу', 'Субботу', 'Воскресенье']


def index(request, **kwargs):
    weekday = kwargs.get('day')

    if weekday == 'today':
        weekday = datetime.datetime.now().weekday()
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
            weekday = weekdays_en.find(weekday.lower())
        except:
            try:
                weekday = int(weekday)
            except:
                weekday = datetime.datetime.now().weekday()
        dayname = weekdays_b[weekday]

        context = {
            'title': 'Расписание на {}'.format(dayname.lower()),
            'days_list': Day.objects.filter(weekday=weekday)
        }

    return render(request, 'sheds/index.html', context)


def tbotcmd_start(*args):
    return loader.render_to_string('sheds/start.html')


def tbotcmd_help(*args):
    return loader.render_to_string('sheds/help.html')


def tbotcmd_schedule(*args):
    weekday = args[0]

    if weekday in ['today', 'сегодня']:
        weekday = datetime.datetime.now().weekday()
        context = {
            'title': 'Расписание на сегодня',
            'days_list': Day.objects.filter(weekday=weekday)
        }
    elif weekday in ['all', 'все', 'всё']:
        context = {
            'title': 'Расписание',
            'days_list': Day.objects.all()
        }
    elif weekday in ['tomorrow', 'завтра']:
        weekday = (datetime.datetime.now().weekday() + 1) % 7
        context = {
            'title': 'Расписание на завтра',
            'days_list': Day.objects.filter(weekday=weekday)
        }
    elif weekday in ['yesterday', 'вчера']:
        weekday = (datetime.datetime.now().weekday() - 1) % 7
        context = {
            'title': 'Расписание на вчера',
            'days_list': Day.objects.filter(weekday=weekday)
        }
    else:
        try:
            weekday = weekdays_en.find(weekday.lower())
        except:
            try:
                weekday = weekdays_ru.find(weekday.lower())
            except:
                try:
                    weekday = int(weekday)
                except:
                    weekday = datetime.datetime.now().weekday()
        dayname = weekdays_b[weekday]

        context = {
            'title': 'Расписание на {}'.format(dayname.lower()),
            'days_list': Day.objects.filter(weekday=weekday)
        }

    return loader.render_to_string('sheds/schedule.html', context)


class TelegramBotReceiverView(View):

    def post(self, request, bot_token):
        if bot_token != token:
            return HttpResponseForbidden('Invalid token')

        raw = request.body.decode('utf-8')
        logging.getLogger('telegram.bot.requests').debug(raw)
        try:
            payload = json.loads(raw)
        except ValueError:
            return HttpResponseBadRequest('Invalid request body')
        else:
            try:
                msg = payload['message']
            except KeyError:
                try:
                    msg = payload['edited_message']
                except KeyError:
                    return HttpResponseBadRequest('Where is the message?')
            chat_id = msg['chat']['id']
            # chat_id = msg['from']['id']
            cmd = msg.get('text')

            if cmd == '/start':
                TelegramBot.sendMessage(chat_id, tbotcmd_start(), parse_mode='HTML')
            elif cmd == '/help':
                TelegramBot.sendMessage(chat_id, tbotcmd_help(), parse_mode='HTML')
            else:
                cmd_name, *cmd_args = cmd.split()
                if cmd_name == '/schedule':
                    if len(cmd_args) == 0:
                        cmd_args = ['today']
                    TelegramBot.sendMessage(chat_id, tbotcmd_schedule(*cmd_args), parse_mode='HTML')
                else:
                    TelegramBot.sendMessage(chat_id, 'I do not understand you, Sir!')

        return JsonResponse({}, status=200)

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(TelegramBotReceiverView, self).dispatch(request, *args, **kwargs)
