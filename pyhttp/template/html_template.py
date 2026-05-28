from .template_slot import TemplateSlot
from helper.filereader import Filereader


class HTMLTemplate:
    def __init__(self, filename, **kwargs):
        self.__freader: Filereader = Filereader()
        self.__slots: list[TemplateSlot] = self.__fill_slots(kwargs=kwargs)
        self.__html: str = self.__freader.read(filename).encode()
        self.__parse()

    @property
    def html(self):
        return self.__html

    @html.setter
    def html(self, value):
        self.__html = value

    def __fill_slots(self, kwargs):
        return [TemplateSlot(k, v) for k, v in kwargs.items()]

    def __parse(self, start=0):
        if start >= len(self.__html):
            return

        search_region = self.__html[start:]
        left = search_region.find("{{")
        if left == -1:
            return

        right = search_region.find("}}", left + 2)
        if right == -1:
            return

        abs_left, abs_right = start + left, start + right

        key = self.__html[abs_left + 2 : abs_right].strip()

        for s in self.__slots:
            if s.field_name == key:
                self.__html = (
                    self.__html[:abs_left] + s.value + self.__html[abs_right + 2 :]
                )
                # Resume after the substituted value
                return self.__parse(start=abs_left + len(s.value))

        # No slot matched — skip past this tag to avoid infinite loop
        return self.__parse(start=abs_right + 2)
