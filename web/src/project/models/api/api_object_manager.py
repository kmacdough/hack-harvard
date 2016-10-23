import uuid


class ApiObjectManager(object):
    def __init__(self, factory):
        self.factory = factory
        self.objects = {}

    def new_object(self):
        return self.factory()

    def add_object(self, new_object, object_id=None):
        if object_id is None:
            object_id = str(uuid.uuid4())
        self.objects[object_id] = new_object
        return object_id

    def add_new_object(self, object_id=None):
        return self.add_object(self.new_object(), object_id)

    def get_object(self, object_id):
        return self.objects.get(object_id, None)

    def get_object_dict(self):
        return dict(self.objects)