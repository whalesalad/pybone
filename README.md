### Python Backbone

This is an experimental project that aims to bring the arbitrary model/collection system from Backbone into Python.

### Why?

I need a system that lets me track changes to objects and collections of those objects.

### API Examples

Let's create a collection with a single item:

```python
>>> collection = Collection({ 'hello': 'world' })
>>> collection
[<Item 'hello': 'world'>]
```

Now let's grab the first item and bind an event handler which is a simple method that will print an object describing the event:

```python
>>> item = collection[0]
>>> item
<Item 'hello': 'world'>
>>> import pprint
>>> def handle_event(event, item, extra):
...     pprint.pprint({
...         'event': event,
...         'item': item,
...         'extra': extra
...     })
>>> item.on('change', handle_event)
```

Right now the item is a simple `{ hello: world }` object:

```python
>>> item
<Item 'hello': 'world'>
```

Let's change the value of `hello` from `world` to `goodbye`:

```python
>>> item.hello = 'goodbye'
{'event': 'change',
 'extra': {'key': 'hello', 'new': 'goodbye', 'old': 'world'},
 'item': <Item 'hello': 'goodbye'>
```

You'll see that a `change` event was fired showing the `old` value as well as the `new` value.


### TODO / Goals

One of the goals of this project is to allow arbitrary collections of data to be updated where diffs will be automatically calculated and evented.