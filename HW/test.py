import unittest
from hub import Hub
from item import Item


class TestHub(unittest.TestCase):

    def setUp(self):
        Item.ids_names = {}

    def test_hub_singleton(self):
        self.assertTrue(Hub([1, 1, 9, 10, 55], '03-11-2021')
                        is Hub([1, 2, 9, 3], '04.05.2022'))

    def test_len_items(self):
        'Проверка того что при добавлении предметов меняется значение len(item)'
        hub = Hub([], '2025-07-06')
        for i in range(5):
            hub.add_item(Item(_id=i, name=f"TestItem", description="Тест", dispatch_time="2025-07-05", _tags=["test"]
        ))

        self.assertEqual(len(hub), 5)

    def test_find_by_id(self):
        hub = Hub([], '2025-07-06')
        item = Item(1, "Test", "Test", "2025-07-05", [])
        hub.add_item(item)
        self.assertIn("Test", hub.find_by_id(1))

    def test_find_by_id_not_found(self):
        hub = Hub([], "2025-07-06")
        result = hub.find_by_id(9)
        self.assertEqual(result, (-1, None))

    def test_find_by_tags(self):
        hub = Hub([], '2025-07-06')
        item = Item(1, "Test", "Test", "2025-07-05", ['fruit', 'sweet'])
        hub.add_item(item)
        result = hub.find_by_tags(['fruit', 'sweet'])
        self.assertIn(item, result)

    def test_rm_item(self):
        hub = Hub([], '2025-07-06')
        item1 = Item(1, "Test", "Test", "2025-07-05", ['fruit', 'sweet'])
        item2 = Item(2, "Test", "Test", "2025-07-05", ['fruit', 'sweet'])
        hub.add_item(item1)
        hub.add_item(item2)
        hub.rm_item(1)
        hub.rm_item(item2)
        self.assertEqual(len(hub), 0)

    def test_drop_items(self):
        hub = Hub([], '2025-07-06')
        item1 = Item(1, "Test", "Test", "2025-07-05", ['fruit', 'sweet'])
        hub.add_item(item1)
        hub.drop_items([1])
        self.assertEqual(len(hub), 0)

    def test_clear(self):
        hub = Hub([], '2025-07-06')
        item1 = Item(1, "Test", "Test", "2025-07-05", ['fruit', 'sweet'])
        item2 = Item(2, "Test", "Test", "2025-07-05", ['fruit', 'sweet'])
        hub.add_item(item1)
        hub.add_item(item2)
        hub.clear()
        self.assertEqual(len(hub), 0)

    def test_find_by_date_one(self):
        hub = Hub([], '2025-07-06')
        item1 = Item(1, "Test", "Test", "2025-07-05", ['fruit', 'sweet'])
        hub.add_item(item1)
        result = hub.find_by_date("2025-07-05")
        self.assertIn(item1, result)

    def test_find_by_date_range(self):
        hub = Hub([], '2025-07-06')
        item1 = Item(1, "Test", "Test", "2025-07-05", ['fruit', 'sweet'])
        item2 = Item(2, "Test", "Test", "2025-07-06", ['fruit', 'sweet'])
        item3 = Item(3, "Test", "Test", "2025-07-07", ['fruit', 'sweet'])
        hub.add_item(item1)
        hub.add_item(item2)
        hub.add_item(item3)
        result = hub.find_by_date("2025-07-05", "2025-07-06")
        self.assertIn(item1, result)
        self.assertIn(item2, result)
        self.assertNotIn(item3, result)

    def test_find_most_valuable(self):
        hub = Hub([], '2025-07-06')
        item1 = Item(1, "Test", "Test", "2025-07-05", ['fruit', 'sweet'])
        item2 = Item(2, "Test", "Test", "2025-07-06", ['fruit', 'sweet'])
        hub.add_item(item1)
        hub.add_item(item2)
        item2.cost = 5555
        item1.cost = 555
        result = hub.find_most_valuable(1)
        self.assertEqual(result[0], item2)


class TestItem(unittest.TestCase):

    def setUp(self):
        Item.ids_names = {}

    def test_item_id(self):
        'Проверка того что у разных Items разные id'
        Item.ids = []
        i1 = Item(1, 'TV', 'PH', '25.06.2025', [])
        i2 = Item(2, 'TV', 'PH', '25.06.2025', [])

        self.assertNotEqual(i1._id, i2._id)

    def test_len_tags(self):
        'Проверка того что при добавлении тэгов меняется значение len(item)'
        Item.ids = []
        i1 = Item(1, 'TV', 'PH', '25.06.2025', [])
        i1.add_tag('h', 'k', 'l')
        self.assertEqual(len(i1), 3)

    def test_equal_tags(self):
        'Проверка того что если к предмету добавить два идентичных тега - их колчество будет один'
        Item.ids = []
        i1 = Item(1, 'TV', 'PH', '25.06.2025', [])
        i1.add_tag('h', 'h')
        self.assertEqual(len(i1), 1)

    def test_rm_tag(self):
        Item.ids = []
        i1 = Item(1, 'TV', 'PH', '25.06.2025', ['h', 'k', 'l'])
        i1.rm_tag('h', 'k')
        self.assertEqual(len(i1), 1)

    def test_len(self):
        Item.ids = []
        i1 = Item(1, 'TV', 'PH', '25.06.2025', ['h', 'k', 'l'])
        self.assertEqual(len(i1), 3)

    def test_set_cost(self):
        Item.ids = []
        i1 = Item(1, 'TV', 'PH', '25.06.2025', ['h', 'k', 'l'])
        i1.cost = 555
        self.assertEqual(i1.cost, 555)

    def test_lt(self):
        Item.ids = []
        i1 = Item(1, 'TV', 'PH', '25.06.2025', ['h', 'k', 'l'])
        i2 = Item(2, 'TV', 'PH', '25.06.2025', ['h', 'k', 'l'])
        i1.cost = 555
        i2.cost = 5550
        self.assertTrue(i2 > i1)

    def test_is_tagged(self):
        Item.ids = []
        i1 = Item(1, 'TV', 'PH', '25.06.2025', ['h', 'k', 'l'])
        self.assertTrue(i1.is_tagged('h', 'k'))

    def test_copy(self):
        Item.ids = []
        i1 = Item(1, 'TV', 'PH', '25.06.2025', ['h', 'k', 'l'])
        i2 = i1.copy()
        self.assertNotEqual(i1._id, i2._id)
        self.assertEqual(i1.name, i2.name)
        self.assertEqual(i1.description, i2.description)
        self.assertEqual(i1.dispatch_time, i2.dispatch_time)
        self.assertEqual(i1._tags, i2._tags)



if __name__ == '__main__':
    unittest.main(argv=['first-arg-is-ignored'], exit=False)