
import json

class MemStore(object):
 

    # a dictionary of obj keys (primary and alternate), and json object values
    valueList = dict()

    # a dictionary of obj primary key, and a list of alternate keys
    keyList = dict()

    def __init__(self, users, customers, tickets):
        self.users = users
        self.customers = customers
        self.tickets = tickets

    def __init__(self):
        self.users = dict()
        self.customers =  dict()
        self.tickets =  dict()

    def __repr__(self):
        return '<MemStore users=%r, customers=%r, tickets=%r >' % \
                (self.users, self.customers, self.tickets) 
     
    @staticmethod
    def jdefault(obj):

        if hasattr(obj, 'isoformat'):
           return obj.isoformat()
        return obj.__dict__ 

    @staticmethod
    def getValue(akey):
        jsonString = MemStore.valueList.get(akey)
        obj = json.loads(jsonString)
        print(repr(obj))
        return obj

    @staticmethod
    def addValue(pkey, altKeys, obj):
        jsonString = json.dumps(obj, indent=4, default=MemStore.jdefault)

        # Save Value using primary key
        MemStore.valueList[pkey] = jsonString

        # Save Value using alternate keys
        for akey in altKeys:
            MemStore.valueList[akey] = jsonString
        
        # Save key list for delete
        MemStore.keyList[pkey] = altKeys
        
    @staticmethod
    def removeValue(pkey):

        # get all alternate keys
        keys = MemStore.keyList.get[pkey]

        # remove the values indexed by alternate keys
        for akey in keys:
            del MemStore.valueList[akey]

        # remove the primary key
        del MemStore.valueList[pkey]

        # remove key list
        del MemStore.keyList[pkey]

