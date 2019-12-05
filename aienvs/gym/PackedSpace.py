from gym.spaces import Space, Dict, Discrete
from aienvs.gym.DecoratedSpace import DecoratedSpace, DictSpaceDecorator
from aienvs.gym.ModifiedActionSpace import ModifiedActionSpace
from aienvs.gym.DecoratedSpace import DictSpaceDecorator
from _collections import OrderedDict


class PackedSpace(ModifiedActionSpace):
    '''
    Modifies a Gym Dict space. Combines several 
    keys from the original space into 
    a new single key. This appears to the outside
    as a Dict with the keys merged.
    But you can call unpack to convert an action
    in this packed space back into an action
    for the original space.
    '''

    def __init__(self, actionspace: Dict, packing: dict):
        '''
        @actionspace the original actionspace
        @packing a dict that maps new dict keys 
        into a list of keys from actionspace.
        The keys in the list are to be removed from the 
        actionspace and the new dict keys are added. 
        IMPORTANT packing keys must NOT be in actionspace.
        example. Say your actionspace has keys a,b,c.
        Then packing could be {'a_b':['a','b']}. The new 
        space will then have keys 'a_b' and 'c'
        
        '''
        self._originalspace = DecoratedSpace.create(actionspace)
        self._subdicts = {}
        newdict = actionspace.spaces.copy()
        # now replace keys according to packing instructions.
        for id in packing:
            subdict = self._createSubspace(packing[id])
            self._subdicts[id] = subdict
            newdict[id] = subdict.getSpace()
            for oldkey in packing[id]:
                if not oldkey in newdict:
                    raise Exception("Packing instruction " + str(packing) + " refers unknown key " + oldkey)
                newdict.pop(oldkey)
        # we set this up as if it is a dict
        # NOTE    super(Dict, self).__init__(newdict) does NOT work as intended
        Dict.__init__(self, newdict)

    def _createSubspace(self, subids: list) -> DictSpaceDecorator:
        '''
        @param subids a list of key/ids in our Dict that 
        have to be merged into a Discrete.
        @return DictSpaceDecorator that contains only the subid's
        from the original space. For instance if subids=['a','b']
        then we return a decorated Dict space {'a':space a, 'b':space b}
        where space a and b are original gym Spaces.
        
        '''
        newdict = { id:space \
                   for id, space in self._originalspace.getSpace().spaces.items() \
                   if id in subids }
        return DictSpaceDecorator(Dict(newdict))

    # Override
    def pack(self, action:Dict) -> OrderedDict:
        '''
        @action a normal (not yet packed) action. Must be a Dict
        with the keys the entity labels. 
        Notice that this is a convenience function to support
        others (eg QCoordinator) in handling a PackedSpace. 
        @return a packed version of the given action in the unpacked space.
        For instance, if action ={'a':1, 'b':3,'c':2}  and this is 
        the packed space {'a_b':['a','b']} then the action may be packed
        to something like {'a_b':55, 'c':2}
        '''
        return { entity:subspace.getIndexOf(action) \
                for entity, subspace in self._subdicts.items()}

    # Override
    def unpack(self, action:OrderedDict) -> OrderedDict:
        '''
        @action a packed action. Utility function.
        action must be OrderedDict with the keys
        the packed-entity labels.
        @return an unpacked version of the packed action
        '''
        newactions = {}
        for actid, value in action.items():
            if actid in self._subdicts:
                origactions = self._subdicts[actid].getById(value)
                for origid, origact in origactions.items():
                    newactions[origid] = origact
            else:
                newactions[actid] = value
        return OrderedDict(newactions)
    
    def getOriginalSpace(self) -> OrderedDict: 
        return self._originalspace.getSpace()

    def get(self, id):
        return self._subdicts[id]
    
