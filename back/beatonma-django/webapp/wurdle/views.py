import datetime
import logging
from typing import List, Optional

from django.http import JsonResponse
from django.views import View

from common.views.logged import LoggedView
from webapp.wurdle.models import ValidWurd, Wurd

log = logging.getLogger(__name__)

DAY_ZERO = datetime.date(2021, 6, 19)


def _get_day() -> int:
    now = datetime.date.today()
    return (now - DAY_ZERO).days


def _get_wurd(day=None):
    if day is None:
        day = _get_day()

    return Wurd.objects.get(day=day).wurd


class WurdleView(LoggedView):
    def get(self, request, *args, **kwargs):
        print(f"wurd is {_get_wurd()}")


class WurdView(View):
    def get(self, request, *args, **kwargs):
        return JsonResponse(
            {
                "day": _get_day(),
                "wurd_length": 5,
                "num_guesses": 6,
            }
        )


class GuessView(LoggedView):
    def get(self, request, *args, **kwargs):
        guess = request.GET.get("guess")

        wurd = _get_wurd()
        result = _check_guess(guess, wurd)
        log.error(f"[{wurd}] Guessed {guess} -> {result}")

        return JsonResponse(
            {
                "result": result,
            }
        )


def _check_guess(guess: str, wurd: str = None) -> Optional[List[str]]:
    try:
        ValidWurd.objects.get(wurd=guess)
    except:
        # Guess is not a valid word
        return None

    result = []
    for index, correct_letter in enumerate(wurd):
        if guess[index] == correct_letter:
            result.append("correct")
        elif guess[index] in wurd:
            result.append("present")
        else:
            result.append("absent")

    return result
