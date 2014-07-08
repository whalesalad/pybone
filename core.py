#!/usr/bin/env python

# class Evented(object):
import pprint
from collections import defaultdict

class Collection(object):
    """
    A collection is a simple wrapper around a list.

    - When an item is added, an 'add' event is fired with the .
    - When an item is removed, a 'remove' event is fired with the details.
    - When an item inside is modified, a 'change' event in the is bubbled up to the collection.

    """

    pass


class Item(object):
    """
    An item is a simple wrapper around a dict, it could be a disk or loadavg.

    If an item belongs to a collection, that collection is notified of its events.

    - When an item is created, a create event is fired.
    - When an item is destroyed, a destroy event is fired.
    - When an item is changed, a change event is fired.

    """

    _reserved = ('_reserved', '_events', '_handlers', '_attributes', '_collection', )
    _events = ('add', 'remove', 'change', )
    _handlers = defaultdict(list)

    def __init__(self, attributes=None, collection=None):
        self._attributes = attributes if attributes else {}
        self._collection = collection if collection else None

    def on(self, event, handler):
        if event in self._events:
            self._handlers[event].append(handler)

    def emit(self, event, extra=None):
        for handler in self._handlers[event]:
            handler(event, self, extra)

    def __repr__(self):
        return '<Item %s>' % (self._attributes)

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

def main():
    print "hello"

if __name__ == '__main__':
    main()