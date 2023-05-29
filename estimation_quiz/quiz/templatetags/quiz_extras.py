from django import template


register = template.Library()


@register.filter(name="has_group")
def has_group(user, group_name) -> bool:
    return user.is_authenticated and user.groups.filter(name=group_name).exists()


@register.filter(name="remaining_guesses")
def remaining_guesses(user) -> int:
    user_answers = user.useranswer_set.all()
    guesses_spent = len(user_answers)
    return total_guesses(user)-guesses_spent


@register.filter(name="total_guesses")
def total_guesses(user) -> int:
    return 30
