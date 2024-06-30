import random
import pandas as pd
import startingconditions


class Simulator:
    def __init__(self, guest_list, list_of_rides):
        self.period = startingconditions.period
        self.hours_open = startingconditions.hours_open
        self.guest_list = guest_list
        self.list_of_rides = list_of_rides
        ride_names = []
        for ride in list_of_rides:
            ride_names.append(ride.name)
        self.wait_times = pd.DataFrame(columns=ride_names)

    def run_simulation(self):
        periods_open = (self.hours_open * 60) / self.period

        for i in range(round(periods_open)):
            wait =[]
            for ride in self.list_of_rides:
                wait.append(ride.wait_time)
                ride.update_queue(self.period)

            self.wait_times.loc[i] = wait

            for guest in self.guest_list:
                if guest.in_park and (guest.time_in_park < guest.max_time):
                    if guest.doing_task:
                        guest.task_time -= self.period
                        if guest.task_time <= 0:
                            guest.doing_task = False
                            guest.task_time = 0

                    task_or_ride = random.uniform(0, 1)
                    if task_or_ride < 0.5:
                        guest.doing_task = True
                        guest.task_time = random.uniform(0, 60)
                    elif ~guest.in_queue:
                        next_ride = random.choice(self.list_of_rides)
                        if next_ride.wait_time < guest.balk_time:
                            next_ride.join_queue(guest)

                    guest.time_in_park += startingconditions.period
                elif guest.time_in_park >= guest.max_time:
                    guest.in_park = False
                else:
                    if i >= guest.arrival_time:
                        guest.in_park = True
