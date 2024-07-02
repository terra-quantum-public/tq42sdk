class PrettyList(list):
    def __repr__(self):
        if not self:
            return "[]"

        type_name = type(self[0]).__name__
        items = "\n  ".join([item.__repr__() for item in self])
        return f"{type_name}List: [\n  {items}\n]"

    def __str__(self):
        return self.__repr__()
