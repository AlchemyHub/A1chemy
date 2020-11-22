class Statistics(object):
    name=''
    symbol=''
    exchange=''

    def __init__(self, *initial_data, **kwargs):
        for dictionary in initial_data:
            for key in dictionary:
                setattr(self, key, dictionary[key])
        for key in kwargs:
            setattr(self, key, kwargs[key])
    
    def to_tag_id(self):
        return self.exchange + "_" + self.symbol