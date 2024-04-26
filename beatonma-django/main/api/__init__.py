from ninja import NinjaAPI

from .search import router as search_router
from .status import router as status_router

public_api = NinjaAPI(urls_namespace="public_api", title="BMA Public API", docs_url="/")
public_api.add_router("", status_router)
public_api.add_router("/search/", search_router)
