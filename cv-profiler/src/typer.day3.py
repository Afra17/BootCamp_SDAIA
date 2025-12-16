import typer
import time 
start = time.perf_counter_ns()
time.sleep(1)
end=time.perf_counter_ns()
elaped_ms = (end - start) / 1_000_000
print(f"Time elaped: {elaped_ms} ms")


"""
app= typer.Typer()

@app.command()
def hello(name: str):
    print (f"Hello {name}")

@app.command()
def goodbye(name: str , formal : bool = False):
    if formal:
        print(f"Goodbye Mr/Ms {name}")
    else:
        print(f"Bye {name}")





if __name__ == "__main__":
    app()"""


class Person:
    def __init__(self, name: str, age: int)->None:
        self.name = name
        self.age = age

    @property
    def age(self)->int:
        return self._age
    
    @age.setter
    def age(self, value:int)->None:
        assert 0 <= value <= 200
        self._age=value 
     
person1= Person("Alice",30) 
person3=Person("Bob",20)  

   
def __eq__(self, other: object) -> bool:
    if not isinstance(other, Person):
        return NotImplemented
    return self.name == other.name and self.age == other.age

