import datetime

holidays = ['2023-4-29', '2023-4-30', '2023-5-1', '2023-5-2', '2023-5-3', '2023-6-22', '2023-6-23', '2023-6-24', '2023-9-29',
            '2023-9-30', '2023-10-1', '2023-10-2', '2023-10-3', '2023-10-4', '2023-10-5', '2023-10-6']
min_date = datetime.datetime(year=2023, month=4, day= 24)
max_date = datetime.datetime.now()


def if_weekend(date):
    if date.weekday == 5 or date.weekday == 6:
        return True
    else:
        return False


if __name__ == '__main__':
    print(holidays)