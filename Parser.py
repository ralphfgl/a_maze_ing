from __future__ import annotations
from pydantic import BaseModel, Field, model_validator, ValidationError
from typing import Optional, Tuple
import sys


class ConfigFile(BaseModel):
    """Parsing of maze configuration with validation"""

    width: int = Field(ge=1)
    height: int = Field(ge=1)
    entry: Tuple[int, int]
    exit: Tuple[int, int]
    output_file: str = Field(min_length=1)
    perfect: bool
    seed: Optional[int] = Field(default=None, ge=0)

    @model_validator(mode="after")
    def validate_config(self) -> "ConfigFile":
        if not (
            0 <= self.entry[0] <= self.height
            and 0 <= self.entry[1] <= self.width
        ):
            raise ValueError("Entry coordinates are out of bound")
        if not (
            0 <= self.exit[0] <= self.height
            and 0 <= self.exit[1] <= self.width
        ):
            raise ValueError("Exit coordinates are out of bound")
        if self.entry == self.exit:
            raise ValueError("Entry and exit have the same coordinates")
        return self


def parse_config(filename: str) -> ConfigFile:
    """Parse the config file and create the ConfigFile pydantic Model"""
    data: dict[str, object] = {}
    with open(filename, "r") as f:
        for i, line in enumerate(f):
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            if "=" not in line:
                raise ValueError(f"Missing '=' in line {i + 1}")
            key, value = line.split("=", 1)
            key = key.strip().lower()
            value = value.strip()
            if key in {"entry", "exit"}:
                try:
                    x, y = map(int, value.split(","))
                    data[key] = (x, y)
                except ValueError:
                    raise ValueError(
                        f"Line {i + 1}: INVALID coordinate: {value}, expected: x,y "
                    )
            else:
                data[key] = value
    return ConfigFile.model_validate(data)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python config.py <config_file>")
        sys.exit(1)

    try:
        config = parse_config(sys.argv[1])
        print("=== Config file parsed ===")
        print(config)
    except FileNotFoundError:
        print("File not found")
        exit(1)
    except (ValueError, ValidationError) as e:
        print(f"Invalid config file: {e}")
        exit(1)
