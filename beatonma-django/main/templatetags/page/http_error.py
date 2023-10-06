import random

from django import template

register = template.Library()


@register.simple_tag(name="http_400_message")
def http_400_message():
    return random.choice(
        [
            "Please check your arguments.",
            "What are you up to? 🧐",
        ]
    )


@register.simple_tag(name="http_403_message")
def http_403_message():
    return random.choice(
        [
            "Please check your arguments.",
            "What are you up to? 🧐",
        ]
    )


@register.simple_tag(name="http_404_message")
def http_404_message():
    return random.choice(
        [
            "Sorry, that page does not exist.",
            "Pls chek yuor speling.",
        ]
    )
