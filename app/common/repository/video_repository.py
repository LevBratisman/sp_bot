from app.common.repository.crud_base_repository import CRUDBase
from app.common.models.video import Video

class VideoRepository(CRUDBase):
    model = Video