from common.util.url import enforce_trailing_slash


def home():
    return "/"


def contact():
    return "/contact/"


def about(path: str | None = None):
    return enforce_trailing_slash(f"/about/{path}")


def app(slug: str):
    return f"/apps/{slug}/"


def app_live_instance(slug: str):
    return f"/apps/{slug}/live/"


def changelog(slug: str):
    return f"/changelog/{slug}/"


def post(slug: str):
    return f"/posts/{slug}/"


def posts(*, tag: str = None, query: str = None):
    params = {"tag": tag, "query": query}
    params = [f"{k}={v}" for k, v in params.items() if v]
    params = "&".join(params)
    return "?".join([f"/", params])


def tag(tag: str):
    return posts(tag=tag.removeprefix("#"))


def webmentions_test():
    return "/webmentions_tester/"
