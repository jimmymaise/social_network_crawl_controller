# Import Models
from DBService.Models.BaseModel import BaseModel

# Import utils
from SuperUtils.HashHelper import HashHelper


class PageModel(BaseModel):
    structure = [
        ['_id', 'id', int],  # page_id
        ['link', 'link', str]  # link to download
    ]

    required_fields = ['_id', 'link']

    default_values = []

    @classmethod
    def create_with(cls,
                    _link):
        media_obj = cls._create_empty()
        media_obj = cls._set_default(media_obj)
        media_obj['_id'] = HashHelper.hash(_link.encode('utf-8'))
        media_obj['link'] = _link
        return media_obj
