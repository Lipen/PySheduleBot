## {{ title }}
{% if days_list %}
    {% for day in days_list %}
        * {{ day }}
        {% for lesson in day.lesson_set.all %}
            + {{ lesson }}
        {% endfor %}
    {% endfor %}
{% else %}
    ### Выходной!
{% endif %}
