from ninja import NinjaAPI

from .global_state import router as global_state_router
from .posts import router as posts_router
from .status import router as status_router
from .tags import router as tags_router

public_api = NinjaAPI(urls_namespace="public_api", title="BMA Public API", docs_url="/")
public_api.add_router("", posts_router)
public_api.add_router("", status_router)
public_api.add_router("", global_state_router)
public_api.add_router("", tags_router)
