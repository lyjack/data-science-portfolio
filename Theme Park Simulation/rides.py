from collections import deque
import startingconditions


class Ride:
    def __init__(self, ride_name, has_fastpass, throughput):
        self.wait_time = 5
        self.guests_in_queue = 0
        self.name = ride_name
        self.fastpass = has_fastpass
        self.throughput = throughput
        self.queue = deque()

    def update_queue(self, time_in_period):
        riders_sat = self.throughput / time_in_period
        remaining_guests = self.guests_in_queue - riders_sat

        if remaining_guests > 0:
            self.guests_in_queue = remaining_guests
            self.wait_time = (self.guests_in_queue / self.throughput) * 60
        else:
            self.guests_in_queue = 0
            self.wait_time = 5

    def decrease_queue(self, number_guests):
        for i in range(number_guests):
            guest = self.queue.popleft()
            guest.in_queue = False

    def join_queue(self, guest):
        guest.in_queue = True
        self.queue.append(guest)
        self.guests_in_queue += 1
        self.wait_time = (self.guests_in_queue / self.throughput) * 60


def construct_ride_list():
    list_of_rides = []
    for ride in startingconditions.ride_features:
        (ride_name, fastpass, throughput) = ride
        list_of_rides.append(Ride(ride_name, fastpass, throughput))

    return list_of_rides
