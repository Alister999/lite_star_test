from advanced_alchemy.extensions.litestar.dto import SQLAlchemyDTO
from app.models.user import User

class UserDTO(SQLAlchemyDTO[User]):
    pass
    #exclude = {"password"}