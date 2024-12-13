from pyshiftsla.shifts_builder import ShiftsBuilder, DailyShift, DateRange, ShiftRange
from pyshiftsla.shift import Shift
from datetime import time, date
import holidays
from typing import List

def get_whole_year_shifts(shift_builder: ShiftsBuilder, year:int = 2024) -> ShiftRange:
    return shift_builder.build_shifts_from_daterange(
        from_date=date(year,1,1),
        to_date=date(year,12,31)
    )

def count_shifts_in_range(shift_range: ShiftRange) -> int:
    return sum(
        daily_shift.get_shifts_num() for daily_shift in shift_range.root.values()
    )
    
def print_shifts_builder_info(shift_builder: ShiftsBuilder, year: int = 2024) -> None:
    wholeyear_shifts = get_whole_year_shifts(shift_builder, year)

    new_year_shifts = wholeyear_shifts.root.get(date(year,1,1))
    christmas_shifts = wholeyear_shifts.root.get(date(year,12,25))

    print(f"- Number of workdays in year {year}: {len(wholeyear_shifts.root)}")
    print(f"- Number of workshifts in year {year}: {count_shifts_in_range(wholeyear_shifts)}")
    print(f"- Number of Shifts in the New Year: {new_year_shifts.get_shifts_num() if new_year_shifts else None}")
    print(f"- Number of Shifts in Christmas: {christmas_shifts.get_shifts_num() if christmas_shifts else None}")


def main():
    # Basic workshifts, based on common companies' policies
    shift_builder = ShiftsBuilder(
        # Monday to Friday, weekly
        workdays_weekly=[0, 1, 2, 3, 4],

        # Common Morning and Afternoon daily shifts.
        shifts_daily=DailyShift([
            # Morning workshift starts at 09:00
            Shift(start=time(9), end=time(12)),
            # Afternoon workshift starts at 13:30
            Shift(start=time(13), end=time(17)),
        ]),
    )
    print("____Basic workshifts policies: 5 days a week, 9 to 5, 1 hour lunch break____")
    print_shifts_builder_info(shift_builder)

    # Add days-off: Holidays and Approved leave requests
    ## American Federal Holidays in 2024
    us_2024_holidays: List[date] = list(holidays.US(years=2024).keys())
    shift_builder.add_days_off_range(us_2024_holidays, inplace=True)
    print("____Workshifts, after adding the Federal Holidays___")
    print_shifts_builder_info(shift_builder)

    ## Employee's approved leave request for 5 days
    approved_4_days_off = DateRange(
        start=date(2024,7,9),
        end=date(2024, 7,12)
    )
    another_approved_day_off = date(2024, 8, 11)
    shift_builder.add_days_off_range(
        [approved_4_days_off, another_approved_day_off],
        inplace=True
    )
    print("____Workshifts, after approving 5 days off___")
    print_shifts_builder_info(shift_builder)

    # Add Overtime Shifts in the new year, and in the Christmas Holiday
    shift_builder.update_special_shifts(ShiftRange({
        # Night Shift, in the New Year
        date(2024,1,1): DailyShift([
            Shift(start=time(22,30), end=time(23,30))
        ]),
        # A full workday (morning and afternoon shift)
        # in the Christmas Holiday
        date(2024,12,25):DailyShift([
            Shift(start=time(8, 30), end=time(11, 30)),
            Shift(start=time(13, 30), end=time(17, 30)),
            Shift(start=time(19, 30), end=time(20))
        ])
    }), inplace=True)

    print("___Workshifts, after adding Overtime Shifts in the New Year and Christmas___")
    print_shifts_builder_info(shift_builder)

    print("___Getting workshifts, in specific days___")
    generated_shifts = get_whole_year_shifts(shift_builder, 2024)
    print(f"{generated_shifts.get(date(2024, 7,12)) = }")
    print(f"{generated_shifts.get(date(2024, 12,25)) = }")

if __name__ == "__main__":
    main()