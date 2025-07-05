from item import Item

class Hub:
    _instance = None

    def __new__(cls, _items,  _date):
        if cls._instance is None:
            cls._instance = object.__new__(cls)
        return cls._instance

    def __init__(self, _items:list,  _date):
        self._items = _items
        self._date = _date

    def __getitem__(self, index):
        if index < len(self._items):
            return self._items[index]
        else:
            raise IndexError('Ошибка индекса')

    def __iter__(self):
        return iter(self._items)

    def __str__(self):
        names = [item.name for item in self._items]
        return f'Предметы: {names}, дата: {self._date}'

    def __repr__(self):
        return f'Hub({repr(self._items[:3])}, {repr(self._date)})'

    def __len__(self):
        print(f'Кол-во предметов: {len(self._items)}')
        return len(self._items)

    def add_item(self, item):
        'Добавляем name из Item, дату создания'
        if isinstance(item, Item):
            self._items.append(item)
            self._date = item.dispatch_time
        else:
            raise TypeError("Не является типом Item")

    def find_by_id(self, id_item):
        'Поиск имени и позиции предмета по id'
        for i in range(len(self._items)):
            if id_item == self._items[i]._id:
                return f'{i}, {self._items[i].name}'
        return (-1, None)

    def find_by_tags(self, tags_list):
        'Поиск предметов по списку тэгов'
        lst_items = []

        for i in range(len(self._items)):
            if len(set(tags_list).difference(set(self._items[i]._tags))) == 0:
                lst_items.append(self._items[i])
        return lst_items

    def rm_item(self, i):
        'Удаляет item с id=i или удаляет item=i, если i - Item'
        if isinstance(i, Item):
            self._items.remove(i)
        else:
            self._items = [item for item in self._items if item._id != i]

        return self._items

    def drop_items(self, items:list):
        'Удаляет все items из Hub'
        for elem in items:
            if isinstance(elem, Item):
                self._items.remove(elem)
            else:
                self._items = [item for item in self._items if item._id != elem]

        return self._items

    def clear(self):
        'Чистит весь _items'
        self._items.clear()
        return self._items

    @property
    def date(self):
        return self._date

    @date.setter
    def date(self, value):
        if not isinstance(value, str):
            raise ValueError("Дата должна быть строкой")
        self._date = value

    def find_by_date(self, *args):
        'Возвращает лист всех Item, подходящих по дате'
        item = []
        for i in range(len(self._items)):
            if len(args) == 1:
                if args[0] == self._items[i].dispatch_time:
                    item.append(self._items[i])
            elif len(args) == 2:
                date_start = min(args)
                date_end = max(args)
                item_date = self._items[i].dispatch_time
                if date_start <= item_date <= date_end:
                    item.append(self._items[i])
            else:
                raise ValueError("Нужно передать 1 или 2 даты")

        return item

    def find_most_valuable(self, amount=2):
        'Возвращает первые amount самых дорогих предметов на складе'
        sorted_items = sorted(self._items, key=lambda item: item.cost, reverse=True)
        return sorted_items[:amount]
















