
class ReactionTypeEnum(object):
    Like    = 'Like'
    Love    = 'Love'
    Wow     = 'Wow'
    Haha    = 'Haha'
    Sad     = 'Sad'
    Angry   = 'Angry'
    Unknown = 'Unknown'

    @classmethod
    def parse_type(cls,
                   _str):
        if _str.upper() == 'LIKE':
            return cls.Like
        if _str.upper() == 'LOVE':
            return cls.Love
        if _str.upper() == 'WOW':
            return cls.Wow
        if _str.upper() == 'HAHA':
            return cls.Haha
        if _str.upper() == 'SAD':
            return cls.Sad
        if _str.upper() == 'ANGRY':
            return cls.Angry
        return cls.Unknown


