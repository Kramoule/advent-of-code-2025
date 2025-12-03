from typing import Any, Callable


from pathlib import Path
from dataclasses import dataclass
from collections.abc import Sequence

type ValidationFunction = Callable[[int],bool]

def parse_input(file: Path) -> list[range]:

    content = file.read_text()
    ranges = content.split(",")
    ids = [range.split("-") for range in ranges]
    return [ range(int(id[0]),int(id[1]) + 1) for id in ids ]

def is_valid_1(id: int) -> bool:

    sid = str(id)
    sid_len = len(sid)

    # If id has an odd number of digit -> it's valid
    if sid_len % 2 != 0:
        return True

    half_len = int(sid_len / 2)    
    if sid[:half_len] == sid[half_len:]:
        return False

    return True

def is_valid_2(id: int) -> bool:

    sid = str(id)
    sid_len = len(sid)
    half_len = int(len(sid) / 2)

    pattern_len = 1
    
    while pattern_len <= half_len:
        pattern = sid[0:pattern_len]
        seek = 0
        #print(f"check pattern {pattern}")
        while (index := pattern_len*seek) < sid_len:
            next_check = sid[index:index+pattern_len]

            # Pattern is different -> check next pattern length
            if pattern != next_check:
                break
            
            # Pattern is indeed appearing multiple times -> is invalid
            if index+pattern_len == sid_len:
                return False

            seek += 1
        pattern_len += 1

    return True
            

def find_invalid_ids(range: range, validation_func: ValidationFunction) -> list[int]:

    return [id for id in range if not validation_func(id)]

def main(file: Path) -> int:

    ranges = parse_input(file)

    invalid_ids = [id for range in ranges for id in find_invalid_ids(range, is_valid_2)]

    return sum(invalid_ids)

if __name__ == "__main__":

    filename = "input.txt"
    file = Path(filename)

    print(main(file))
