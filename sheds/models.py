import datetime

from django.db import models

# weekdays = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
weekdays = ['Понедельник', 'Вторник', 'Среда', 'Четверг', 'Пятница', 'Суббота', 'Воскресенье']


class Day(models.Model):
    # name = models.CharField('weekday', max_length=32)
    weekday = models.IntegerField('weekday number', default=-1)

    def __str__(self):
        return weekdays[self.weekday]

    def is_today(self):
        return datetime.date.today().weekday() == self.weekday


class Lesson(models.Model):
    name = models.CharField('lesson name', max_length=200)
    day = models.ForeignKey(Day, on_delete=models.CASCADE)
    time_start = models.TimeField('lesson start time')
    time_end = models.TimeField('lesson end time')
    week_odd = models.BooleanField('whether odd week lesson', default=False)
    week_even = models.BooleanField('whether even week lesson', default=False)

    def __str__(self):
        s = '{} ({}-{})'.format(self.name, self.time_start.strftime('%H:%M'), self.time_end.strftime('%H:%M'))
        if self.week_even and not self.week_odd:
            s += ' [Чёт]'
        elif not self.week_even and self.week_odd:
            s += ' [Нечёт]'
        elif not self.week_even and not self.week_odd:
            s += ' [НИКОГДА]'
        return s

    def is_today(self):
        if self.day.is_today():
            (_, weeknumber, _) = datetime.datetime.now().isocalendar()
            weeknumber -= 34
            even = weeknumber % 2 == 0

            return even and self.week_even or \
                not even and self.week_odd
        else:
            return False

    def is_now(self):
        return self.is_today() and \
            self.time_start <= datetime.datetime.now().time() <= self.time_end
