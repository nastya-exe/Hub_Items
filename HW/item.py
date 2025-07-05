class Item:
    ids_names = dict()

    def __new__(cls, _id, name, description, dispatch_time, _tags):
        if _id not in cls.ids_names:
            cls.ids_names[_id] = [name, _tags]
        else:
            raise IndexError('Повторяющийся id')
        return object.__new__(cls)

    def __init__(self, _id, name, description, dispatch_time, _tags):
        self._id = _id
        self.name = name
        self.description = description
        self.dispatch_time = dispatch_time
        self._tags = _tags
        self._cost = None

    def __str__(self):
        if self._cost == None:
            return f"""id {self._id}: {self.name},\nописание: {self.description}, дата: {self.dispatch_time},\nтэги: {self._tags}"""
        else:
            return f"""id {self._id}: {self.name},\nописание: {self.description}, дата: {self.dispatch_time},\nтэги: {self._tags}
стоимость: {self._cost}"""

    def __repr__(self):
        return f'Item({repr(self._id)}, {repr(self._tags[:3])})'

    def __len__(self):
        print(f'Кол-во тэгов: {len(self._tags)}')
        return len(self._tags)

    def add_tag(self, *args):
        'Добавление тэгов в _tags'
        for elem in args:
            if elem not in self._tags:
                self._tags.append(elem)
            else:
                continue

    def rm_tag(self, *args):
        'Удаление тэгов из _tags'
        for elem in args:
            if elem in self._tags:
                self._tags.remove(elem)
            else:
                continue

    @property
    def cost(self):
        return self._cost

    @cost.setter
    def cost(self, value):
        if value < 0:
            raise ValueError("Стоимость должна быть > 0")
        self._cost = value

    def __lt__(self, other):
        if self._cost < other._cost:
            return True
        else:
            return False

    def is_tagged(self, *args):
        'Проверка наличия тэгов у предмета'
        if len(set(args).difference(set(self._tags))) == 0:
            return True
        else:
            return False

    def copy(self):
        'Возвращает новый item c тем же атрибутами, но новый id'
        new_id = 1
        while True:
            if new_id in Item.ids_names:
                new_id += 1
            else:
                break

        new_item = Item(_id=new_id, name=self.name, description=self.description,
        dispatch_time=self.dispatch_time, _tags=self._tags.copy())
        new_item._cost = self._cost

        Item.ids_names[new_id] = new_item

        return new_item












