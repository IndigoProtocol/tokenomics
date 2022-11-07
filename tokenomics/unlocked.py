from datetime import datetime
from math import floor
from typing import Final, List

from tokenomics import EPOCH, MILLION, YEAR_DAYS, YEAR_EPOCH, YEAR_MONTHS

TOTAL_SUPPLY: Final[int] = 35 * MILLION


def per_epoch(
    date: datetime, delay: int, launch: datetime, schedule: List[float]
) -> int:
    """Calculates how much INDY has been unlocked based on a per-epoch
    vesting schedule

    Args:
        date: The date to perform the calculation for
        delay: The number of epochs after launch the vesting schedule is
        delayed for
        launch: The date of the first epoch after mainnet launch
        schedule: The vesting schedule

    Return:
        The number of INDY that have been unlocked by the vesting schedule
        up until `date`
    """
    epochs_since_launch: Final[int] = min(
        floor((date - launch).days / EPOCH) - delay + 1,
        len(schedule) * YEAR_EPOCH,
    )

    if epochs_since_launch <= 0:
        return 0

    bonus_epochs: Final[int] = int(
        TOTAL_SUPPLY * sum(schedule)
        - sum(
            (
                floor(TOTAL_SUPPLY * vested / YEAR_EPOCH) * YEAR_EPOCH
                for vested in schedule
            )
        )
    )

    def vested(epoch: int) -> int:
        unlocked_in_year: Final[float] = schedule[floor(epoch / YEAR_EPOCH)]
        unlocked: Final[int] = floor(
            TOTAL_SUPPLY * (unlocked_in_year / YEAR_EPOCH)
        )

        return unlocked + 1 if epoch < bonus_epochs else unlocked

    return sum((vested(epoch) for epoch in range(epochs_since_launch)))


def per_month(
    date: datetime,
    launch: datetime,
    amount: float,
    total_years: int = 2,
    offset: int = 0,
) -> int:
    """Calculates how much INDY has been unlocked based on a per-month
    vesting schedule

    Args:
        date: The date to perform the calculation for
        launch: The date of mainnet launch
        amount: The percentage of INDY total supply distributed
        total_years: The number of years the vesting schedule runs for

    Return:
        The number of INDY that have been unlocked by the vesting schedule
        up until `date`
    """
    if not offset:
        offset = int(YEAR_DAYS / YEAR_MONTHS - launch.day)

    vested_months: Final[int] = YEAR_MONTHS * total_years
    months_since_launch: Final[int] = min(
        floor(((date - launch).days - offset) / (YEAR_DAYS / YEAR_MONTHS)) + 1,
        vested_months,
    )

    if months_since_launch < 0:
        return 0

    if months_since_launch == 0 and (date - launch).days >= 0:
        return int(TOTAL_SUPPLY * amount / vested_months)

    return int(months_since_launch * TOTAL_SUPPLY * amount / vested_months)


def total(
    date: datetime,
    gd_delay: int,
    gd_schedule: List[float],
    ld_delay: int,
    ld_schedule: List[float],
    sd_delay: int,
    sd_schedule: List[float],
    td_amount: float,
    launch: datetime,
    itd: int,
    offset: int = 0,
) -> int:
    """Calculates how much INDY has been unlocked

    Args:
        date: The date to perform the calculation for
        gd_delay: The number of epochs after launch the Governance vesting
        schedule is delayed for
        gd_schedule: The Governance vesting schedule
        ld_delay: The number of epochs after launch the Liquidity vesting
        schedule is delayed for
        ld_schedule: The Liquidity vesting schedule
        sd_delay: The number of epochs after launch the Stability vesting
        schedule is delayed for
        sd_schedule: The Stability vesting schedule
        td_amount: The percentage of INDY allocated to the team
        launch: The date of the first epoch after mainnet launch
        itd: The number of INDY unlocked on mainnet launch
        offset: The offset to use for the team distribution

    Return:
        The number of INDY that have been unlocked up until `date`
    """
    return (
        (itd if date >= launch else 0)
        + per_epoch(date, sd_delay, launch, sd_schedule)
        + per_epoch(date, ld_delay, launch, ld_schedule)
        + per_epoch(date, gd_delay, launch, gd_schedule)
        + per_month(date, launch, td_amount, offset=offset)
    )
