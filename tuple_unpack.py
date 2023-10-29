def tuple_unpack(data: tuple) -> list:
    if isinstance(data, tuple):
        return [tuple_unpack(part) for part in data]
    else:
        return data


a = ((('item1', 'item2'), ('item1', 'item2'), 'item2'), ('item1', 'item2'), ('item1', 'item2'),
     (('item1', 'item2'), ('item1', 'item2'), 'item2'))

unpacked = tuple_unpack(a)
print(unpacked)
