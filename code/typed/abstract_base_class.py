from abc import ABC, abstractmethod

class Class(ABC):
    
    @abstractmethod
    def method(self) -> str:
        pass

# Class()

class SubCLass(Class): pass

SubCLass()