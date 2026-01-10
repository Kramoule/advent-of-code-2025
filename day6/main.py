from pathlib import Path

from dataclasses import dataclass, field

from functools import reduce

INPUT_FILE = "input.txt"


def add(a, b):
    return a + b

def sub(a, b):
    return a - b

def mul(a, b):
    return a * b

def div(a, b):
    if b == 0:
        raise ValueError("Division par zéro")
    return a / b

OPS = {
    "+": add,
    "-": sub,
    "/": div,
    "*": mul
}

@dataclass
class Equation:
    numbers: list[int] = field(default_factory=list)
    op: str = ""

    def compute(self):
        return reduce(lambda a ,b: OPS[self.op](a,b), self.numbers)



def parse_input(input: Path) -> list[list[str]]:
    lines = None
    with input.open("r") as f:
        lines = f.readlines()

    matrix = [l.split() for l in lines]

    return matrix

def create_equations(matrix):

    equations = [] 
    for line in matrix[:-1]:
        for index, col in enumerate(line):
            if len(equations) < index +1:
                equations.append(Equation())
            print(index, col)
            equations[index].numbers.append(int(col))
    
    for i, op in enumerate(matrix[-1]):
        equations[i].op = op
    return equations


def main(file: Path):
    matrix = parse_input(file)
    equations = create_equations(matrix)
    print(equations)
    res = [eq.compute() for eq in equations]
    print(sum(res))


if __name__ == "__main__":
    f = Path(INPUT_FILE)
    if not f.exists():
        print(f"File {INPUT_FILE} doesn't exist. Exiting....")
        exit(1)
    
    main(f)