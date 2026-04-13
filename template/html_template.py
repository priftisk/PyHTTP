from .template_slot import TemplateSlot


class HTMLTemplate:
    def __init__(self, html, **kwargs):
        self.__html: str = html
        self.__slots: list[TemplateSlot] = self.__fill_slots(kwargs=kwargs)
        self.__parse()

    @property
    def html(self):
        return self.__html

    @html.setter
    def html(self, value):
        self.__html = value

    def __fill_slots(self, kwargs):
        return [TemplateSlot(k, v) for k, v in kwargs.items()]

    def __parse(self):
        left = self.__html.find("{{")
        right = self.__html[left::].find("}}")

        if left == -1 or right == -1:
            raise Exception("Error parsing value from template.")
        key = self.html[left + 2 : left + right]
        for s in self.__slots:
            print(s.field_name)
            if s.field_name == key:
                self.html = self.html[:left] + s.value + self.html[left + right + 2 :]
