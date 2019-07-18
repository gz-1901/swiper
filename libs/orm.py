class ModelToDictMixin():
    def to_dict(self, exclude=None):
        if exclude is None:
            exclude = []

        attr_dict = {}
        fields = self._meta.fields

        for field in fields:
            field_name = field.attname
            if field_name not in exclude:
                attr_dict[field_name] = getattr(self, field_name)

        return attr_dict
