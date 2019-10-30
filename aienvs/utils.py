import yaml
import logging
from numpy import array, array_equal


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
