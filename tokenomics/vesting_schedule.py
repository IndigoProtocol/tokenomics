from typing import Final, List, NamedTuple


class VestingSchedule(NamedTuple):
    """Holds information about each of Indigo's vesting schedules"""

    gd: List[float]
    ld: List[float]
    sd: List[float]
    td: float


MAP: Final[VestingSchedule] = VestingSchedule(
    gd=[0.005, 0.0075, 0.01, 0.0125, 0.015],
    ld=[0.01, 0.02, 0.03, 0.04, 0.05],
    sd=[0.06, 0.07, 0.08, 0.09, 0.1],
    td=0.225,
)
