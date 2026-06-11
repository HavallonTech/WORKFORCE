from datetime import time


def get_current_punch(now_time):

    windows = [

        (1, time(7, 30), time(8, 20)),

        (2, time(8, 50), time(9, 20)),

        (3, time(9, 50), time(10, 20)),

        (4, time(10, 50), time(11, 20)),

        (5, time(11, 50), time(12, 20)),

        (6, time(12, 50), time(13, 20)),

        (7, time(13, 50), time(14, 20)),

        (8, time(14, 50), time(15, 20))

    ]

    for punch, start, end in windows:

        if start <= now_time <= end:

            return punch

    return None