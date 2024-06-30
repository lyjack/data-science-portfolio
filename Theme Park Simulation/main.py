import rides
import guest
import simulation
import matplotlib.pyplot as plt

if __name__ == '__main__':
    list_of_rides = rides.construct_ride_list()
    guest_list = guest.construct_guest_list()
    simulation = simulation.Simulator(guest_list, list_of_rides)
    simulation.run_simulation()
    simulation.wait_times.plot()

    plt.show()
