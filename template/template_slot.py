class TemplateSlot:
    def __init__(self, field_name=None, value=None):
        self.__field_name = field_name
        self.__value = value

    @property
    def field_name(self):
        return self.__field_name

    @field_name.setter
    def field_name(self, value):
        self.__field_name = value

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, v):
        self.__value = v
