from django import template
from django.db import connection
from django.db.models import Sum

from contribution.models import Withdrawal

register = template.Library()


@register.inclusion_tag('contribution/total_savings.html')
def tag_total_savings(id, type=''):
    # make sure type is same as db type
    if type == 'health':
        type = 'HF'
    elif type == 'pension':
        type = 'PF'

    cursor = connection.cursor()

    if type != '':
        # build query

        cursor.execute(
            "select extract(year from created) as year, sum(amount) as amount from savings where type=%s and member_id=%s group by year", [type, id])
        data = [dict(zip([col[0] for col in cursor.description], row))  # type: ignore
                for row in cursor.fetchall()]
        return {'total_savings': data}
    else:
        # build query
        cursor.execute(
            "select extract(year from created) as year, sum(amount) as amount from savings where member_id=%s group by year", [id])
        data = [dict(zip([col[0] for col in cursor.description], row))  # type: ignore
                for row in cursor.fetchall()]
        return {'total_savings': data}


@register.inclusion_tag('contribution/total_withdrawals.html')
def tag_total_withdrawals(id, type=''):
    # make sure type is same as db type
    if type == 'health':
        type = 'HF'
    elif type == 'pension':
        type = 'PF'

    cursor = connection.cursor()

    if type != '':
        cursor.execute(
            "select extract(year from withdrawn) as year, sum(amount) as amount from withdrawal where type=%s and member_id=%s group by year", [type, id])
        data = [dict(zip([col[0] for col in cursor.description], row))  # type: ignore
                for row in cursor.fetchall()]
        return {'total_withdrawals': data}
    else:
        cursor.execute(
            "select extract(year from withdrawn) as year, sum(amount) as amount from withdrawal where member_id=%s group by year", [id])
        data = [dict(zip([col[0] for col in cursor.description], row))  # type: ignore
                for row in cursor.fetchall()]
        return {'total_withdrawals': data}
