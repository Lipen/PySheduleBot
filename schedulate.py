import os
import django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "PyShed.settings")
django.setup()

from sheds.models import Day
from datetime import datetime
import json

dryrun = False
weekdays = ['Понедельник', 'Вторник', 'Среда', 'Четверг', 'Пятница', 'Суббота', 'Воскресенье']


def main():
    with open('schedule.json', encoding='utf-8') as f:
        schedule = json.load(f)

    if not dryrun:
        print('Deleting all Day objects...')
        Day.objects.all().delete()
        print('All previous objects deleted')

    for weekdayname, lessons in sorted(schedule.items(), key=lambda x: weekdays.index(x[0])):
        print('Processing {}...'.format(weekdayname))
        if not dryrun:
            day = Day(weekday=weekdays.index(weekdayname))
            day.save()

        for lesson in lessons:
            name, times, oddity = lesson.split(' @ ')
            ts, te = map(lambda t: datetime.strptime(t, '%H:%M').time(), times.split('-'))
            odd = even = False
            if 'both' in oddity:
                odd = even = True
            elif 'odd' in oddity:
                odd = True
            elif 'even' in oddity:
                even = True

            data = {'name': name, 'time_start': ts, 'time_end': te, 'week_odd': odd, 'week_even': even}
            if not dryrun:
                day.lesson_set.create(**data)

            # def json_serial(obj):
            #     """JSON serializer for objects not serializable by default json code"""
            #     from datetime import time

            #     if isinstance(obj, (datetime, time)):
            #         serial = obj.isoformat()
            #         return serial
            #     raise TypeError("Type not serializable")
            # print('Creating lesson with data:')
            # print(json.dumps(data, ensure_ascii=False, indent=4, default=json_serial))

if __name__ == '__main__':
    main()
