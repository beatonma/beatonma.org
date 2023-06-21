from django.views import View


class BaseView(View):
    reverse_name = "you-should-override-reverse_name"
