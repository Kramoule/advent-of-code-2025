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
        clicks = self.clicks % (DIAL_MAX + 1)
        if self.direction is Direction.R:
            return init + clicks
        else:
            return init - clicks

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
        # How many full rotations we've done (== how many time we went over 0)
        full_rotations = int(abs(instruction.clicks // (DIAL_MAX + 1)))
        result += full_rotations
        
        prev_num = dial_num
        dial_num = instruction.op(prev_num)
        
        # If we didn't go over the max or below the min value (> 0) of the dial,
        # we didn't didn't click on 0
        if prev_num != 0 and dial_num not in range(1, DIAL_MAX + 1):
            # if the new dial number is out of the 1-100 boundary, this mean we pointed at 0 once
            # EXCEPT if the old position is 0 (Going left from 0 will go out of range but not point on 0)
            result += 1
            dial_num %= (DIAL_MAX + 1)
            

        print(instruction, prev_num, dial_num, result)

    return result

def main(input: Path)-> None:

    dial_num = 50
    result = 0
    commands = parse_input(input)

    result = turn_dial_new(commands)
    
    print(f"Dial was '0' {result} times !")

if __name__ == "__main__":
    filename = "input.txt"
    input = Path(filename)
    if not input.exists():
        print("File doesn't exist")
        exit(1)

    main(input)