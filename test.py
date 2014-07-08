import sys
import unittest
import logging
import pprint

from core import Item

# class TestCollections(unittest.TestCase):
#     def setUp(self):
#         self.collection = Collection()

class TestItem(unittest.TestCase):
    def setUp(self):
        self.events = []

        self.properties = {
            "id": "trusty",
            "name": "Ubuntu",
            "version": "14.04"
        }

        self.item = Item(self.properties)

    def handle_event(self, event, item, extra):
        self.events.append({
            'event': event,
            'item': item,
            'extra': extra
        })

    def test_as_dict(self):
        self.assertEqual(dict(iter(self.item)), self.properties)

    def test_get_item_like_dict(self):
        self.assertEqual(self.item['name'], 'Ubuntu')

    def test_get_item_like_object(self):
        self.assertEqual(self.item.version, '14.04')

    def test_change_event_is_fired(self):
        self.item.on('change', lambda e,i,d: self.handle_event(e,i,d))
        self.item.version = '12.04'

        self.assertEqual(len(self.events), 1)

        event = self.events.pop()

        self.assertEqual(event['extra']['old'], '14.04')
        self.assertEqual(event['extra']['new'], '12.04')

if __name__ == '__main__':
    # logging.basicConfig(stream=sys.stderr)
    # logging.getLogger(__name__).setLevel(logging.DEBUG)

    unittest.main()