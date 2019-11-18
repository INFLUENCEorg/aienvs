import yaml
import logging
from numpy import array, array_equal, ndarray
from collections.abc import  Hashable


def getParameters(filename:str) -> dict:
    """
    @param filename yaml file
    @return: dictionary with parameters in given (yaml) file
    """
    with open(filename, 'r') as stream:
        try:
            parameters = yaml.safe_load(stream)['parameters']
        except yaml.YAMLError as exc:
            logging.error(exc)
    return parameters


def rm(array:list, element: array) -> list:
    """
    @param array the list to delete element from
    @param element a numpy array : the element to be deleted
    @return list with all occurences of element 
    deleted from array, if np is there
    """
    # np does not even support this standard?!? 
    return [x for x in array if not array_equal(element, x)]


def hashf(obj) -> int:
    """
    Forced computation of hash code. Also hashes dict and list
    """
    if isinstance(obj, list) or isinstance(obj, ndarray):
        total = 0
        for x in obj:
            total = total + hashf(x)
        return total
    if isinstance(obj, dict):
        total = 0
        for x in obj.keys():
            total = total + hashf(x) + hashf(obj[x]) 
        return total        
    return hash(obj)

