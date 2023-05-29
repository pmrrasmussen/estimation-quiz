from django import template

register = template.Library()


@register.filter(name="has_group")
def has_group(user, group_name):
    return user.is_authenticated and user.groups.filter(name=group_name).exists()

@register.filter(name="remaining_guesses")
def remaining_guesses(user):
    guesses_spent = 10
    return total_guesses(user)-guesses_spent

@register.filter(name="total_guesses")
def total_guesses(user):
    return 30
