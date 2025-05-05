from litestar import Litestar
from litestar.plugins.sqlalchemy import SQLAlchemyPlugin
from app.config import db_config, init_db
from app.routes.user import user_routes

sqlalchemy_plugin = SQLAlchemyPlugin(config=db_config)

app = Litestar(
    route_handlers=[user_routes],
    plugins=[sqlalchemy_plugin],
    on_startup=[init_db],
    debug=True
)

