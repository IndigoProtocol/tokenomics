import os
from typing import Final

DATA: Final[str] = os.path.join(
    os.path.dirname(os.path.realpath(__file__)), "data"
)
