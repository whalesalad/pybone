import sys
import unittest
import logging
import pprint

from core import Item, Collection

def format_event(event, item, extra):
    return {
        'event': event,
        'item': item,
        'extra': extra
    }

class TestCollections(unittest.TestCase):
    def setUp(self):
        self.events = []

        self.collection = Collection({ 'hello': 'world' })

        self.collection.on('all', self.handle_event)

    def handle_event(self, event, item, extra):
        self.events.append(format_event(event, item, extra))

    def test_changing_existing_item(self):
        item = self.collection[0]

        item.hello = 'goodbye'

        event = self.events.pop()

        self.assertEqual(event['event'], 'change')
        self.assertEqual(event['extra']['old'], 'world')
        self.assertEqual(event['extra']['new'], 'goodbye')

    def test_adding_item(self):
        self.collection.append({ 'x': 1, 'y': 2 })

        # make sure that there is one item in the collection
        self.assertEqual(len(self.collection), 2)

        # make sure that item is the same as the above
        self.assertEqual(self.collection[1], Item({ 'x': 1, 'y': 2 }))

        # make sure we have an event
        self.assertEqual(len(self.events), 1)

        event = self.events.pop()

        self.assertEqual(event['event'], 'add')

    def test_diffing_collection(self):
        events = []

        collection = Collection()
        collection.on('all', lambda event, item, extra: events.append(format_event(event,item,extra)))

        for x in xrange(3):
            collection.append({ 'disk': '/dev/sda%s' % x })

        self.assertTrue(len(events), 3)

        collection.replace({ 'disk': '/dev/sda1' })

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
        self.item.on('change', self.handle_event)
        self.item.version = '12.04'

        self.assertEqual(len(self.events), 1)

        event = self.events.pop()

        self.assertEqual(event['event'], 'change')
        self.assertEqual(event['extra']['old'], '14.04')
        self.assertEqual(event['extra']['new'], '12.04')


if __name__ == '__main__':
    # logging.basicConfig(stream=sys.stderr)
    # logging.getLogger(__name__).setLevel(logging.DEBUG)

    unittest.main()