from pyshiftsla.shifts_builder import ShiftsBuilder, DateRange, DailyShift, ShiftRange
from pyshiftsla.shift import Shift
from datetime import time, date
import holidays

def get_company_workdays_policy():
    return ShiftsBuilder(
        workdays_weekly=[0, 1, 2, 3, 4],  # Monday to Friday
        shifts_daily=DailyShift(
            # Morning workshift
            Shift(start=time(8, 30), end=time(11, 45)),
            # Afternoon workshift
            Shift(start=time(13, 30), end=time(17, 45)),
        ),
    )


def add_american_federal_holidays(
    shift_builder: ShiftsBuilder,
    year: int = 2024
) -> None:
    shift_builder.add_days_off_range(
        [
            DateRange(start=date(), end=date()),
            date()
        ],
        inplace=True
    )