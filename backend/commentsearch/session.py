from commentsearch.models import SessionUpdateParams


class Session():
    def __init__(self):
        self.elements: List[ConceptElement] = []

    @property
    def elements(self):
        return self.__elements

    @elements.setter
    def elements(self, elements):
        self.__elements = elements

    def remove_element(self, param: SessionUpdateParams):
        del self.elements[param.id]
