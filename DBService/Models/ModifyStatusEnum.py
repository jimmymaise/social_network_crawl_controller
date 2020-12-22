
class ModifyStatusEnum(object):
    Nothing = 'Nothing'     # Nothing to do here
    Moving  = 'Moving'      # If modify_status of normal user is moving, they will be moved to KOLs
                            # If modify_status of KOLs is moving, they will be moved back to normal_user
    Locking = 'Locking'
