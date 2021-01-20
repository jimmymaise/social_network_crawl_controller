class StoredObjectBuilder:
    def __init__(self):
        self.mappings = {}
        self.stored_object = {}
        self.get_all_fields = {}

    def _build(self, mapping, collected_object):
        for collected_object_field, stored_object_field in mapping.items():
            self.stored_object[stored_object_field] = collected_object.get(collected_object_field)

    def _set_get_all_fields(self, collected_object, excluded_fields):
        for collected_object_field, collected_object_value in collected_object.items():
            if not excluded_fields or collected_object_field not in excluded_fields:
                self.stored_object[collected_object_field] = collected_object_value

    def set_get_all_fields_from_collected_object(self, collected_object_name, excluded_fields):
        self.get_all_fields[collected_object_name] = excluded_fields

    def add_mapping(self, collected_object_name, mapping):
        self.mappings[collected_object_name] = mapping
        return self

    def build(self, **collected_objects):
        for collected_object_name, collected_object in collected_objects.items():
            if not collected_object:
                continue
            if collected_object_name in self.mappings:
                self._build(self.mappings[collected_object_name], collected_object)
            if collected_object_name in self.get_all_fields:
                self._set_get_all_fields(collected_object, self.get_all_fields[collected_object_name])
        return self.stored_object
