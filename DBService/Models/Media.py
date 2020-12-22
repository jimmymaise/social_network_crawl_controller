# Import Libs

# Import Models
from DBService.Models.BaseModel import BaseModel
from DBService.Models.MediaTypeEnum import MediaTypeEnum
from DBService.Models.MediaStatusEnum import MediaStatusEnum

# Import utils
from SuperUtils.HashHelper import HashHelper


class MediaModel(BaseModel):
    structure = [
        ['_id', 'id', int],  # media_id
        ['link', 'link', str],  # link to download
        ['path', 'path', str],  # location on disk
        ['type', 'type', str],  # type of media: image, video
        ['status', 'status', str],  # status of media: error / downloaded / not download
    ]

    required_fields = ['_id', 'link']

    default_values = [
        ['path', ''],
        ['type', MediaTypeEnum.Image],
        ['status', MediaStatusEnum.NotDownload]
    ]

    @classmethod
    def get_type(cls,
                 _link):
        for _type in ['.jpg']:
            if _type in _link:
                return MediaTypeEnum.Image
        for _type in ['.mp4']:
            if _type in _link:
                return MediaTypeEnum.Video
        return MediaTypeEnum.Image

    @classmethod
    def create_with(cls, _link, _s3_link=None):
        media_obj = cls._create_empty()
        media_obj = cls._set_default(media_obj)
        media_obj['_id'] = HashHelper.hash_url(_link)
        media_obj['link'] = _link
        media_obj['s3_link'] = _s3_link
        media_obj['type'] = cls.get_type(_link)
        return media_obj
