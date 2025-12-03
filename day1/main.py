from pathlib import Path
from dataclasses import dataclass
from enum import Enum
from typing import Iterable

DIAL_MAX = 99

class Direction(Enum):
    L = "Left"
    R = "Right"

@dataclass
class Input:
    direction: Direction
    clicks: int

    def op(self, init: int) -> int:
        if self.direction is Direction.R:
            return init + self.clicks
        else:
            return init - self.clicks

    def __str__(self):
        return f"{self.direction.name}{self.clicks}"

def parse_input(input: Path) -> list[Input]:
    lines = None
    with input.open("r") as f:
        lines = f.readlines()

    return [Input(Direction[line[0]], int(line[1:])) for line in lines]

def turn_dial_simple(inputs: Iterable[Input]) -> int:
    dial_num = 50
    result = 0

    for instruction in inputs:
        dial_num = instruction.op(dial_num) % (DIAL_MAX + 1)
        if dial_num == 0:
            result += 1

    return result

def turn_dial_new(inputs: Iterable[Input]) -> int:
    dial_num = 50
    result = 0

    for instruction in inputs:
        prev_num = dial_num
        dial_num = instruction.op(prev_num)
        if dial_num <= 0 or dial_num > DIAL_MAX:
            full_rotations = int(abs(instruction.clicks // (DIAL_MAX + 1)))
            print(f"{dial_num // (DIAL_MAX + 1)} :{full_rotations}")
            result += full_rotations + (1 if dial_num == 0 else 0 )
            result = result - 1 if prev_num == 0 else result
        
        dial_num %= (DIAL_MAX + 1)
        #print(f"{instruction}: {dial_num} -> {result}")

    return result

def main(input: Path)-> None:

    dial_num = 50
    result = 0
    commands = parse_input(input)

    result = turn_dial_new(commands)
    
    print(f"Dial was '0' {result} times !")

if __name__ == "__main__":
    filename = "test.txt"
    input = Path(filename)
    if not input.exists():
        print("File doesn't exist")
        exit(1)

    main(input)