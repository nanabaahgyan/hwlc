from django import template
from django.db import connection

from hashlib import sha1
from ..models import Savings

register = template.Library()


@register.inclusion_tag('contribution/total_contributions.html')
def tag_total_contributions(id, type):
    # make sure type is same as db type
    if type == 'health':
        type = 'HF'
    elif type == 'pension':
        type = 'PF'

    # build query
    cursor = connection.cursor()
    cursor.execute(
        "select extract(year from created) as year, sum(amount) as amount from savings where type=%s and member_id=%s group by year", [type, id])
    data = [dict(zip([col[0] for col in cursor.description], row))
            for row in cursor.fetchall()]
    return {'total_contributions': data}
