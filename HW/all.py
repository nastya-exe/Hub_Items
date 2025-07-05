import random
from datetime import datetime

from hub import Hub
from item import Item


hub = Hub([], '2025-07-07')
hub.clear()


i1 = Item(4, "Apple", "Фрукт", "2025-07-05", ["food", "fruit"])
i2 = Item(5, "Banana", "Фрукт", "2025-07-06", ["food", "fruit"])
i3 = Item(6, "Avocado", "Фрукт", "2025-06-07", ["food"])
i4 = Item(7, "Carrot", "Овощ", "2025-07-03", ["food", "vegetable"])
i5 = Item(8, "Apricot", "Фрукт", "2025-07-08", ["fruit"])
i6 = Item(9, "Date", "Фрукт", "2025-07-04", ["fruit"])
i7 = Item(11, "Eggplant", "Овощ", "2025-07-09", ["vegetable"])
i8 = Item(12, "Fig", "Фрукт", "2025-07-10", ["fruit"])
i9 = Item(13, "Grape", "Фрукт", "2025-07-10", ["fruit"])
i10 = Item(14, "Honeydew", "Фрукт", "2025-07-04", ["fruit"])
i11 = Item(15, "Kiwi", "Фрукт", "2025-07-02", ["fruit"])
i12 = Item(16, "Lemon", "Фрукт", "2025-07-05", ["fruit"])
i13 = Item(17, "Mango", "Фрукт", "2025-07-06", ["fruit"])
i14 = Item(18, "Nectarine", "Фрукт", "2025-07-07", ["fruit"])
i15 = Item(19, "Orange", "Фрукт", "2025-07-08", ["fruit"])
i16 = Item(20, "Papaya", "Фрукт", "2025-07-09", ["fruit"])
i17 = Item(21, "Quince", "Фрукт", "2025-07-10", ["fruit"])
i18 = Item(22, "Raspberry", "Ягода", "2025-07-11", ["berry"])
i19 = Item(23, "Strawberry", "Ягода", "2025-07-12", ["berry"])
i20 = Item(24, "Tomato", "Овощ", "2025-07-13", ["vegetable"])
i21 = Item(25, "Ugli Fruit", "Фрукт", "2025-07-14", ["fruit"])
i22 = Item(26, "Vanilla Bean", "Пряность", "2025-07-15", ["spice"])
i23 = Item(27, "Watermelon", "Фрукт", "2025-07-16", ["fruit"])
i24 = Item(28, "Xigua", "Арбуз", "2025-07-17", ["fruit"])
i25 = Item(29, "Yam", "Овощ", "2025-07-18", ["vegetable"])
i26 = Item(30, "Zucchini", "Овощ", "2025-07-19", ["vegetable"])
i27 = Item(31, "Blackberry", "Ягода", "2025-07-20", ["berry"])
i28 = Item(32, "Cantaloupe", "Фрукт", "2025-07-21", ["fruit"])
i29 = Item(33, "Durian", "Фрукт", "2025-07-22", ["fruit"])
i30 = Item(34, "Elderberry", "Ягода", "2025-07-23", ["berry"])


items = [i1, i2, i3, i4, i5, i6, i7, i8, i9, i10, i11, i12, i13, i14, i15, i16, i17, i18, i19, i20, i21, i22, i23, i24, i25, i26, i27, i28, i29, i30]

for elem in items:
    hub.add_item(elem)

for elem in items:
    elem.cost = random.randint(500, 1000)

a = []
Outdated = []
MostValuable = []
Others = []

for item in hub:
    if item.name.lower().startswith("a"):
        a.append(item)
        hub.rm_item(item)


for item in hub:
    if item.dispatch_time < hub.date:
        Outdated.append(item)
        hub.rm_item(item)


for item in hub.find_most_valuable(10):
    MostValuable.append(item)
    hub.rm_item(item)

for item in hub:
    Others.append(item)








