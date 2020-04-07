from aienvs.PredatorPrey.MovableItemOnMap import MovableItemOnMap


class Predator(MovableItemOnMap):
    """
    A preditor entity (called 'robot' in the paper) in the predatorprey environment.
    immutable.
    """
        
    def __str__(self):
     """
     for hashing
     """
     return "Predator[" + super().__str__(self) + "]" 
