import sys
from datetime import date, datetime
from typing import Final, Optional

import click

from tokenomics import unlocked
from tokenomics.aqb import calculate_yes_votes, has_passed
from tokenomics.csv import generate as csv_generate
from tokenomics.vars import GD_DELAY, ITD, LAUNCH, LD_DELAY, SD_DELAY
from tokenomics.vesting_schedule import MAP

DATE: Final[click.types.DateTime] = click.DateTime(formats=["%Y-%m-%d"])
TODAY: Final[str] = str(date.today())


@click.group()
def tokenomics() -> None:
    """An interface for illustrating Indigo’s tokenomics."""
    pass


@tokenomics.group()
def aqb() -> None:
    """Commands related to Indigo’s Adaptive Quorum Biasing."""
    pass


@tokenomics.command()
@click.option(
    "--date",
    type=DATE,
    default=TODAY,
    help="The date to calculate the supply for",
)
@click.option(
    "--delay",
    type=int,
    default=GD_DELAY,
    help="The number of epochs the GD will be delayed for after launch",
)
@click.option(
    "--launch-epoch-date",
    type=DATE,
    default=LAUNCH,
    help="The date of the first epoch after launch",
)
def gd(date: datetime, delay: int, launch_epoch_date: datetime) -> None:
    """Gets the circulating supply from the Governance Distribution."""
    click.echo(unlocked.per_epoch(date, delay, launch_epoch_date, MAP.gd))


@tokenomics.command()
@click.option(
    "--date",
    type=DATE,
    default=TODAY,
    help="The date to calculate the supply for",
)
@click.option(
    "--delay",
    type=int,
    default=LD_DELAY,
    help="The number of epochs the LD will be delayed for after launch",
)
@click.option(
    "--launch-epoch-date",
    type=DATE,
    default=LAUNCH,
    help="The date of the first epoch after launch",
)
def ld(date: datetime, delay: int, launch_epoch_date: datetime) -> None:
    """Gets the circulating supply from the Liquidity Distribution."""
    click.echo(unlocked.per_epoch(date, delay, launch_epoch_date, MAP.ld))


@tokenomics.command()
@click.option(
    "--date",
    type=DATE,
    default=TODAY,
    help="The date to calculate the supply for",
)
@click.option(
    "--delay",
    type=int,
    default=SD_DELAY,
    help="The number of epochs the SD will be delayed for after launch",
)
@click.option(
    "--launch-epoch-date",
    type=DATE,
    default=LAUNCH,
    help="The date of the first epoch after launch",
)
def sd(date: datetime, delay: int, launch_epoch_date: datetime) -> None:
    """Gets the circulating supply from the Stability Distribution."""
    click.echo(unlocked.per_epoch(date, delay, launch_epoch_date, MAP.sd))


@tokenomics.command()
@click.option(
    "--date",
    type=DATE,
    default=TODAY,
    help="The date to calculate the supply for",
)
@click.option(
    "--launch-epoch-date",
    type=DATE,
    default=LAUNCH,
    help="The date of the first epoch after launch",
)
def td(date: datetime, launch_epoch_date: datetime) -> None:
    """Gets the circulating supply from the Team Distribution."""
    click.echo(unlocked.per_month(date, launch_epoch_date, MAP.td))


@tokenomics.command()
@click.option(
    "--date",
    type=DATE,
    default=TODAY,
    help="The date to calculate the supply for",
)
@click.option(
    "--gd-delay",
    type=int,
    default=GD_DELAY,
    help="The number of epochs the GD will be delayed for after launch",
)
@click.option(
    "--ld-delay",
    type=int,
    default=LD_DELAY,
    help="The number of epochs the LD will be delayed for after launch",
)
@click.option(
    "--sd-delay",
    type=int,
    default=SD_DELAY,
    help="The number of epochs the SD will be delayed for after launch",
)
@click.option(
    "--launch-epoch-date",
    type=DATE,
    default=LAUNCH,
    help="The date of the first epoch after launch",
)
def total(
    date: datetime,
    gd_delay: int,
    ld_delay: int,
    sd_delay: int,
    launch_epoch_date: datetime,
) -> None:
    """Gets the circulating supply from all distributions."""
    click.echo(
        unlocked.total(
            date,
            gd_delay,
            MAP.gd,
            ld_delay,
            MAP.ld,
            sd_delay,
            MAP.sd,
            MAP.td,
            launch_epoch_date,
            ITD,
        )
    )


@aqb.command()
@click.argument("vn", type=int)
@click.argument("e", type=int)
def vy(vn: int, e: int) -> None:
    """Calculates how many yes votes are required for a proposal to pass
    AQB."""
    click.echo(calculate_yes_votes(vn, e))


@aqb.command()
@click.argument("vy", type=int)
@click.argument("vn", type=int)
@click.argument("e", type=int)
def proposal(vy: int, vn: int, e: int) -> None:
    """Evaluates whether a proposal has passed AQB."""
    if has_passed(vy, vn, e):
        click.echo("Passed")

    else:
        click.echo("Failed")
        sys.exit(1)


@tokenomics.command()
@click.option(
    "--gd-delay",
    type=int,
    default=GD_DELAY,
    help="The number of epochs the GD will be delayed for after launch",
)
@click.option(
    "--ld-delay",
    type=int,
    default=LD_DELAY,
    help="The number of epochs the LD will be delayed for after launch",
)
@click.option(
    "--sd-delay",
    type=int,
    default=SD_DELAY,
    help="The number of epochs the SD will be delayed for after launch",
)
@click.option(
    "--launch-epoch-date",
    type=DATE,
    default=LAUNCH,
    help="The date of the first epoch after launch",
)
@click.option(
    "--excel",
    type=click.Path(),
    help="A filepath to save the CSV output as xlsx format",
)
def csv(
    gd_delay: int,
    ld_delay: int,
    sd_delay: int,
    launch_epoch_date: datetime,
    excel: Optional[str],
) -> None:
    """Ouputs tokenomics details in CSV format."""
    csv = csv_generate(gd_delay, ld_delay, sd_delay, launch_epoch_date, ITD)

    if not excel:
        click.echo(csv.to_csv(index=False))

    else:
        csv.to_excel(excel, index=False)
