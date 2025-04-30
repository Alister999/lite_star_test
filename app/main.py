from litestar import Litestar
from litestar.openapi import OpenAPIConfig
from litestar.plugins.sqlalchemy import SQLAlchemyPlugin, SQLAlchemyAsyncConfig
from app.routes.user import user_routes
import os
from dotenv import load_dotenv


load_dotenv()

db_config = SQLAlchemyAsyncConfig(connection_string=os.environ["DATABASE_URL"])
sqlalchemy_plugin = SQLAlchemyPlugin(config=db_config)

openapi_config = OpenAPIConfig(
    title="My Litestar API",
    version="1.0.0",
    description="API with Swagger documentation",
)

app = Litestar(
    route_handlers=[user_routes],
    plugins=[sqlalchemy_plugin],
    openapi_config=openapi_config,
)

