# class Evented(object):
import pprint

from collections import defaultdict
import dictdiffer

class Collection(object):
    """
    A collection is a simple wrapper around a list.

    - When an item is added, an 'add' event is fired with the .
    - When an item is removed, a 'remove' event is fired with the details.
    - When an item inside is modified, a 'change' event in the is bubbled up to the collection.

    """

    _events = ('all', 'add', 'remove', 'change', )
    _handlers = defaultdict(list)
    _items = []

    def __init__(self, items=None):
        self._items = self.convert_items(items) if items else []

    def __iter__(self):
        return iter(self._items)

    def __contains__(self, item):
        return item in self._items

    def __len__(self):
        return len(self._items)

    def __getitem__(self, key):
        return self._items[key]

    def __repr__(self):
        return repr(self._items)

    def convert_items(self, items):
        if isinstance(items, dict):
            items = [items]
        return [ Item(attributes=i, collection=self) for i in items ]

    def on(self, event, handler):
        if event in self._events:
            self._handlers[event].append(handler)

    def emit(self, event, item, extra=None):
        for handler in self._handlers[event]:
            handler(event, item, extra)

        for handler in self._handlers['all']:
            handler(event, item, extra)

    def append(self, item):
        if not isinstance(item, Item):
            item = Item(attributes=item, collection=self)

        self._items.append(item)

        self.emit('add', item)

    def replace(self, items):
        new = self.convert_items(items)
        old = self._items

        pprint.pprint(dict(old=old))
        pprint.pprint(dict(new=new))


class Item(object):
    """
    An item is a simple wrapper around a dict, it could be a disk or loadavg.

    If an item belongs to a collection, that collection is notified of its events.

    - When an item is created, a create event is fired.
    - When an item is destroyed, a destroy event is fired.
    - When an item is changed, a change event is fired.

    """

    _reserved = ('_reserved', '_events', '_handlers', '_attributes', '_collection', )
    _events = ('all', 'add', 'remove', 'change', )
    _handlers = defaultdict(list)

    def __init__(self, attributes=None, collection=None):
        self._attributes = attributes if attributes else {}
        self._collection = collection if collection else None

        if self._collection:
            self.on('change', lambda event, item, extra: self._collection.emit(event, item, extra))

    def on(self, event, handler):
        if event in self._events:
            self._handlers[event].append(handler)

    def emit(self, event, extra=None):
        for handler in self._handlers[event]:
            handler(event, self, extra)

    def __repr__(self):
        return '<Item %s>' % ', '.join( [ "'%s': '%s'" % (x,y) for x,y in self._attributes.iteritems() ] )

    def __eq__(self, other):
        return self._attributes == other._attributes

    def __getitem__(self, key):
        if key in self._reserved:
            return object.__getattr__(self, key)

        if key in self._attributes.keys():
            return self._attributes.get(key, None)

    def __getattr__(self, key):
        if key in self._reserved:
            return object.__getattr__(self, key)

        if key in self._attributes.keys():
            return self._attributes.get(key, None)

    def __setattr__(self, key, value):
        if key in self._reserved:
            return object.__setattr__(self, key, value)

        old = self._attributes.get(key, None)
        self._attributes[key] = value
        self.emit('change', { 'key': key, 'old': old, 'new': value })

    def __iter__(self):
        return self._attributes.iteritems()

    def __contains__(self, key):
        return key in self._attributes.keys()



class Sensor(object):
    # connections           []      add/remove/change
    # disks                 []      add/remove/change
    # distro                {}      change
    # hostname              {}      change
    # libc_version          {}      change
    # loadavg               {}      change
    # memory                {}      change
    # processes             []      add/remove/change
    # python_version        {}      change
    # sessions              []      add/remove/change
    # uname                 {}      change
    # users                 []      add/remove/change
    pass
