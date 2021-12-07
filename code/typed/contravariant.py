from typing import TypeVar, Generic

T = TypeVar('T', contravariant=True)

class JsonSerializer(Generic[T]):
    def serialize(self, value: T) -> str:
        pass

class Animal: pass
class Cat(Animal): pass

class Controller(Generic[T]):
    def __init__(self, serializer: JsonSerializer[T]) -> None:
        self.__serializer = serializer
    
    def view(self, value: T) -> str:
        return f"Page with {self.__serializer.serialize(value)}"

class AnimalSerializer(JsonSerializer[Animal]):
    def serialize(self, value: Animal) -> str:
        return "Animal"

class CatSerializer(JsonSerializer[Cat]):
    def serialize(self, value: Cat) -> str:
        return "Cat"       

Controller[Cat](CatSerializer())
Controller[Cat](AnimalSerializer())