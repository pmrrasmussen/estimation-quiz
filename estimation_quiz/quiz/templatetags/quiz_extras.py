from django import template
from django.urls import reverse, NoReverseMatch
import logging

logger = logging.getLogger(__name__)

register = template.Library()

@register.filter(name="remaining_guesses")
def remaining_guesses(user) -> int:
    user_answers = user.useranswer_set.all()
    guesses_spent = len(user_answers)

    return total_guesses(user)-guesses_spent

@register.filter(name="total_guesses")
def total_guesses(user) -> int:
    return 25

@register.simple_tag(takes_context=True)
def is_active(context, url_name):
    if url_name == context['request'].resolver_match.url_name:
        return 'current'
    return ''
