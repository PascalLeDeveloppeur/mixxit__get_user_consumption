class Metadata:
    def __init__(self,
                 fk_batch_id=None,
                 key="",
                 lastmodified="",
                 datetime_from_keyname="",
                 full_info=''):
        self.fk_batch_id = fk_batch_id
        self.key = key
        self.lastmodified = lastmodified
        self.datetime_from_keyname = datetime_from_keyname
        self.full_info = full_info