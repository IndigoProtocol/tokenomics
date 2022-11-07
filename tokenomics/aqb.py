from math import sqrt
from typing import Final

START_PERCENT: Final[float] = 0.7


def has_passed(yes_votes: int, no_votes: int, circulating_supply: int) -> bool:
    """Determines if a proposal has passed according to Adaptive Quorum
    Biasing

    Args:
        yes_votes: The number of "yes" votes
        no_votes: The number of "no" votes
        circulating_supply: The current circulating supply of INDY

    Return:
        True is the proposal passed; False otherwise
    """
    return (
        True
        if (
            int(
                (yes_votes / sqrt(circulating_supply))
                - (no_votes / sqrt(yes_votes + no_votes))
            )
        )
        > 0
        else False
    )


def calculate_yes_votes(no_votes: int, circulating_supply: int) -> int:
    """Calculates how many "yes" votes are required for a proposal to pass
    AQB.

    Args:
        no_votes: The current number of "no" votes for the proposal
        circulating_supply: The current circulating supply of INDY

    Return:
        The number of "yes" votes required for a proposal to pass
    """
    if no_votes < 0:
        no_votes = 0

    start = int(no_votes * START_PERCENT)
    end = circulating_supply

    def _q(yes_votes: int) -> int:
        return int(
            yes_votes / sqrt(circulating_supply)
            - no_votes / sqrt(yes_votes + no_votes)
        )

    while start <= end:
        yes_votes = int((start + end) / 2)
        q = _q(yes_votes)

        if q < 0:
            start = yes_votes + 1

        elif q > 0:
            end = yes_votes - 1

        else:
            if _q(yes_votes + 1) > 0:
                return yes_votes + 1

            else:
                start = yes_votes + 1

    return end + 1
