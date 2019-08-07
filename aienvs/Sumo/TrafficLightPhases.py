from _pyio import IOBase

import xml.etree.ElementTree as ElementTree


class TrafficLightPhases():
    '''
    Contains possible phases of all traffic lights.
    Usually read from a file.
    The file follows the SUMO format from
    https://sumo.dlr.de/wiki/Simulation/Traffic_Lights#Defining_New_TLS-Programs
    
    We search for <tlLogic> elements in the XML (can be at any depth) 
    and collect all settings.
    Each tlLogic element must have a unique id (traffic light reference).
    '''
    
    def __init__(self, filename:str):
        '''
        @param filename the file containing XML text. NOTE this really
        should not be a "filename" but a input stream; unfortunately 
        ElementTree does not support this.
        '''
        tree = ElementTree.parse(filename)
        self._phases = {}
        for element in tree.getroot().findall('tlLogic'):
            intersectionid = element.get('id')
            if intersectionid in self._phases:
                raise Exception('file ' + filename + ' contains multiple tlLogic elements with id=' + id)
            
            newphases = {}
            phasenr = 0
            for item in element:
                newphases[phasenr] = item.get('state')
                phasenr = phasenr + 1
            self._phases[intersectionid] = newphases
    
    def getLightIds(self) -> list:
        '''
        @return all traffic light ids
        '''
        return list(self._phases.keys())

    def getPhases(self, intersectionId:str) -> list:
        '''
        @param intersectionId the intersection id 
        @return all possible phasenrs for given lightid
        '''
        return list(self._phases[intersectionId].keys())
    
    def getPhase(self, intersectionId:str, phasenr: int):
        """
        @param intersectionId the intersection id 
        @param phasenr the short number given to this phase
        @return the phase for given lightid and phasenr. Usually this
        is the index number in the file, starting at 0.
        """
        return self._phases[intersectionId][phasenr]

