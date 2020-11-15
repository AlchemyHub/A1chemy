class Tag(object):
    id = ''
    parent = ''
    description = ''
    
    def __init__(self, *initial_data, **kwargs):
        for dictionary in initial_data:
            for key in dictionary:
                setattr(self, key, dictionary[key])
        for key in kwargs:
            setattr(self, key, kwargs[key])

    def to_dict(self):
        return {
            'id': self.id,
            'parent': self.parent,
            'description': self.description
        }
    