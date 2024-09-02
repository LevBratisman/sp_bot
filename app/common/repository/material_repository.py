from app.common.repository.crud_base_repository import CRUDBase
from app.common.models.material import Material

class MaterialRepository(CRUDBase):
    model = Material