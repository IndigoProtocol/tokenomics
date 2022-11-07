from datetime import datetime
from typing import Final

import pandas
from dateutil.relativedelta import relativedelta

from tokenomics import EPOCH, unlocked
from tokenomics.vesting_schedule import MAP

VESTED_YEARS: Final[int] = max(len(MAP.gd), len(MAP.ld), len(MAP.sd))


def generate(
    gd_delay: int,
    ld_delay: int,
    sd_delay: int,
    launch_epoch_date: datetime,
    itd: int,
) -> pandas.DataFrame:
    """Generates the full INDY vesting schedule in a CSV-type format

    Args:
        gd_delay: The number of epochs after launch the Governance vesting
        schedule is delayed for
        ld_delay: The number of epochs after launch the Liquidity vesting
        schedule is delayed for
        sd_delay: The number of epochs after launch the Stability vesting
        schedule is delayed for
        launch_epoch_date: The date of the first epoch after mainnet launch
        itd: The number of INDY unlocked on mainnet launch
    """
    dates = pandas.Series(
        pandas.date_range(
            launch_epoch_date,
            (
                launch_epoch_date
                + relativedelta(years=VESTED_YEARS)
                + relativedelta(days=max(gd_delay, ld_delay, sd_delay) * EPOCH)
            ),
        )
    )

    df = pandas.DataFrame(
        {
            "Date": dates,
            "# INDY": dates.apply(
                lambda date: unlocked.total(
                    date,
                    gd_delay,
                    MAP.gd,
                    ld_delay,
                    MAP.ld,
                    sd_delay,
                    MAP.sd,
                    MAP.td,
                    launch_epoch_date,
                    itd,
                )
            ),
        }
    ).drop_duplicates(["# INDY"])

    df["ITD"] = itd
    df["SD"] = df["Date"].apply(
        lambda date: unlocked.per_epoch(
            date, sd_delay, launch_epoch_date, MAP.sd
        )
    )
    df["LD"] = df["Date"].apply(
        lambda date: unlocked.per_epoch(
            date, ld_delay, launch_epoch_date, MAP.ld
        )
    )
    df["GD"] = df["Date"].apply(
        lambda date: unlocked.per_epoch(
            date, gd_delay, launch_epoch_date, MAP.gd
        )
    )
    df["TD"] = df["Date"].apply(
        lambda date: unlocked.per_month(date, launch_epoch_date, MAP.td)
    )

    df.insert(len(df.columns) - 1, "# INDY", df.pop("# INDY"))

    return df.reset_index(drop=True)
