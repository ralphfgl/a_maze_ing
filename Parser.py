from __future__ import annotations
from pydantic import BaseModel, Field, model_validator, ValidationError
from typing import Tuple
import io
import sys
from typing import List, Dict


class ConfigFile(BaseModel):
    WIDTH: int = Field(ge=1)
    HEIGHT: int = Field(ge=1)
    ENTRY: Tuple[int, int] = Field(ge=1)
    EXIT: Tuple[int, int] = Field(ge=1)
    OUTPUT_FILE: str = Field(min_length=1)
    PERFECT: bool = True

    @model_validator(mode="after")
    def validate_config(self) -> "ConfigFile":
        if not (self.ENTRY[0] <= self.HEIGHT and self.ENTRY[1] <= self.WIDTH):
            raise ValueError("Entry is out of bound")
        if not (self.EXIT[0] <= self.HEIGHT and self.EXIT[1] <= self.WIDTH):
            raise ValueError("Exit is out of bound")
        return self


if __name__ == "__main__":
    try:
        if len(sys.argv) != 2:
            raise ValueError("Expected exactly one argument")
        with open(sys.argv[1]) as f:
            content: List[str] = f.readlines()
    except Exception as e:
        print(e)
        exit(1)

    try:
        stored: Dict = {}
        for line in content:
            combo: List[str] = line.lower().split("=")
            if len(combo) != 2:
                raise ValueError(
                    f"wrong declaration of flag: {'='.join(combo)}"
                )
            stored[combo[0].strip()] = combo[1].strip()
        config = ConfigFile(
            WIDTH=int(stored["width"]),
            HEIGHT=int(stored["height"]),
            ENTRY=tuple(stored["entry"]),
            EXIT=tuple(stored["exit"]),
            OUTPUT_FILE=stored["output_file"],
            PERFECT=stored["perfect"],
        )
    except KeyError:
        print("INCOMPLETE config file")
        exit(1)
    except (ValidationError, ValueError) as e:
        print(f"INVALID value in config file: {e}")
        exit(1)
