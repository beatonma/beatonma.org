from common.views.logged import LoggedView
from django.shortcuts import render
from main.models.posts import About


class AboutView(LoggedView):
    def get(self, request):
        about = About.objects.get_current()

        return render(
            request,
            "pages/about.html",
            {
                "about": about,
            },
        )
