import uuid

import faust


class UID(faust.Record):
    @staticmethod
    def new():
        return UID(uid=uuid.uuid1())

    uid: uuid.UUID
