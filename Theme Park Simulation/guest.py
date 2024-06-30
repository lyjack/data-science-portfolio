import numpy as np
import random

import startingconditions


class Guest:
    def __init__(self):
        self.in_queue = False
        self.doing_task = False
        self.task_time = 0
        self.in_park = False
        self.arrival_time = 0
        self.max_time = startingconditions.hours_open
        self.time_in_park = 0
        # self.attraction_preference = random.uniform(0, 1)


class Tourist(Guest):
    def __init__(self):
        super().__init__()
        self.balk_time = np.random.normal(120, 30)
        self.arrival_time = np.random.beta(2, 8) * startingconditions.hours_open / startingconditions.period
        self.max_time = np.random.normal(8, 2) * 60


class Local(Guest):
    def __init__(self):
        super().__init__()
        self.balk_time = np.random.normal(60, 15)
        self.arrival_time = random.uniform(0, 1) * startingconditions.hours_open / startingconditions.period
        self.max_time = np.random.normal(4, 2) * 60


def construct_guest_list():
    guest_list = []
    for i in range(startingconditions.number_of_guests):
        guest_type = random.uniform(0, 1)
        if guest_type < 0.25:
            guest_list.append(Local())
        else:
            guest_list.append(Tourist())

    return guest_list
