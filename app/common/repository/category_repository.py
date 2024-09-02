from app.common.repository.crud_base_repository import CRUDBase
from app.common.models.category import Category

class CategoryRepository(CRUDBase):
    model = Category