import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from simulation.engine import Engine
from simulation.map import Map
from simulation.simulation import Simulation
from simulation.car import Car


class Statistics:
    def mean_v(self, v_map, cars_number):
        mask = (v_map >= 0)
        return np.sum(v_map[mask]) / cars_number

    def cars_stop_ratio(self, v_map, cars_number):
        # mask = (v_map == 0)
        # return np.sum(v_map[mask]) / car_number
        return (np.count_nonzero(v_map == 0) / cars_number) * 100

    def cars_move_ratio(self, v_map, cars_number):
        # mask = (v_map > 0)
        # return np.sum(v_map[mask]) / car_number
        return (np.count_nonzero(v_map > 0) / cars_number) * 100

    def min_value(self, vector):
        return min(vector)

    def max_value(self, vector):
        return max(vector)

    def mean_value(self, vector):
        return np.mean(vector)

    def standard_deviation(self, vector):
        return np.std(vector)

    def average_section_travel_time(self, cars, distance, cars_number, ticks_number):
        # cars = engine.simulation.cars
        cum_distance = 0
        for car in cars:
            cum_distance += car.odometer

        #the average number of times a given distance has been driven by all cars
        average_distance_driven_time = ((cum_distance/cars_number)/distance)

        # the average travel time for a given length section
        average_section_travel_time = ticks_number / average_distance_driven_time

        return average_section_travel_time

    def average_speed_plot(self, mean_vs, cars_number):
        mean_value = self.mean_value(mean_vs)
        plt.plot(mean_vs, label='mean velocity')
        plt.axhline(mean_value, color='red', linestyle='--', label='mean')
        plt.xlabel('tick')
        plt.ylabel('velocity')
        plt.legend()
        plt.title(f"Average speed ({cars_number} cars)")
        # plt.show()

    def average_speed_box_plot(self, mean_vs, cars_number):
        plt.boxplot(mean_vs)
        plt.ylabel('velocity')
        plt.title(f'Average velocity boxplot ({cars_number} cars)')
        # plt.show()

    def stop_moving_cars_plot(self, stop_cars, moving_cars, cars_number, ticks_number):
        red = '#ff1c1c'
        green = '#5aff00'
        blue = '#1c00ac'
        x = [i for i in range(1, ticks_number + 1)]
        y1 = stop_cars
        y2 = moving_cars
        mean_value_stop = self.mean_value(stop_cars)
        mean_value_moving = self.mean_value(moving_cars)

        where_greater = np.array(y2) > np.array(y1)
        where_less = np.array(y2) < np.array(y1)

        plt.plot(x, y1, label='stop cars ratio', color=red)
        plt.plot(x, y2, label='moving cars ratio', color=green)
        plt.axhline(mean_value_stop, color=blue, linestyle='--', label='mean stop')
        plt.axhline(mean_value_moving, color=blue, linestyle='-.', label='mean moving')
        plt.fill_between(x, y1, y2, where=where_greater, color='green', alpha=0.3)
        plt.fill_between(x, y1, y2, where=where_less, color='red', alpha=0.3)
        plt.xlabel('tick')
        plt.ylabel('% of cars')
        plt.legend()
        plt.title(f"Stop/Moving cars ratio ({cars_number} cars)")
        # plt.show()

    def stop_cars_box_plot(self, stop_cars_ratios, cars_number):
        plt.boxplot(stop_cars_ratios)
        plt.ylabel('velocity')
        plt.title(f'Stop cars ratio boxplot ({cars_number} cars)')
        # plt.show()

    def moving_cars_box_plot(self, moving_cars_ratios, cars_number):
        plt.boxplot(moving_cars_ratios)
        plt.ylabel('velocity')
        plt.title(f'Moving cars ratio boxplot ({cars_number} cars)')
        # plt.show()

    def heat_map(self, heatmap_matrix, cars_number):
        ax = sns.heatmap(heatmap_matrix, cbar=False)
        ax.set_title(f'Heatmap ({cars_number} cars)')
        # plt.show()

    def travel_time_plot(self, categories, values, distance):
        plt.bar(categories, values)
        plt.ylabel('ticks')
        plt.title(f'Time to travel {distance} tiles')
        # plt.show()

    def generate_average_speed_plots(self, mean_vs_lists, cars_numbers, to_png, png_name):
        num_rows = 4
        num_cols = 2
        fig, axes = plt.subplots(num_rows, num_cols, figsize=(20, 20), gridspec_kw={'width_ratios': [2, 1]})

        counter = 0
        for i in range(num_rows):
            for j in range(num_cols):
                ax = axes[i, j]  # Wybór odpowiedniej osi
                plt.sca(ax)  # Ustawienie bieżącej osi
                if j == 0:
                    self.average_speed_plot(mean_vs_lists[counter], cars_numbers[counter])
                if j == 1:
                    self.average_speed_box_plot(mean_vs_lists[counter], cars_numbers[counter])
            counter += 1

        plt.tight_layout()
        if to_png:
            plt.savefig(f'plots/{png_name}.png')
        plt.show()

    def generate_stop_moving_cars_plots(self, stop_cars_lists, moving_cars_list, cars_numbers, ticks_number, to_png, png_name):
        num_rows = 4
        num_cols = 3
        fig, axes = plt.subplots(num_rows, num_cols, figsize=(25, 20), gridspec_kw={'width_ratios': [3, 1, 1]})

        counter = 0
        for i in range(num_rows):
            for j in range(num_cols):
                ax = axes[i, j]  # Wybór odpowiedniej osi
                plt.sca(ax)  # Ustawienie bieżącej osi
                if j == 0:
                    self.stop_moving_cars_plot(stop_cars_lists[counter], moving_cars_list[counter], cars_numbers[counter], ticks_number)
                if j == 1:
                    self.stop_cars_box_plot(stop_cars_lists[counter],cars_numbers[counter])
                if j == 2:
                    self.moving_cars_box_plot(moving_cars_list[counter],cars_numbers[counter])
            counter += 1

        plt.tight_layout()
        if to_png:
            plt.savefig(f'plots/{png_name}.png')
        plt.show()

    def generate_heatmaps(self, hitmap_list, cars_numbers, to_png, png_name):
        num_rows = 2
        num_cols = 2
        fig, axes = plt.subplots(num_rows, num_cols, figsize=(20, 20))

        counter = 0
        for i in range(num_rows):
            for j in range(num_cols):
                ax = axes[i, j]  # Wybór odpowiedniej osi
                plt.sca(ax)  # Ustawienie bieżącej osi
                self.heat_map(hitmap_list[counter], cars_numbers[counter])
                counter += 1

        plt.tight_layout()
        if to_png:
            plt.savefig(f'plots/{png_name}.png')
        plt.show()

    def generate_travel_time_plots(self, average_section_travel_time_lists ,cars_numbers, distances,  to_png, png_name):
        categories = [f'{number} cars' for number in cars_numbers ]

        num_rows = 2
        num_cols = 2
        fig, axes = plt.subplots(num_rows, num_cols, figsize=(8, 8))

        counter = 0
        for i in range(num_rows):
            for j in range(num_cols):
                values = [sublist[counter] for sublist in average_section_travel_time_lists]

                ax = axes[i, j]  # Wybór odpowiedniej osi
                plt.sca(ax)  # Ustawienie bieżącej osi
                self.travel_time_plot(categories, values, distances[counter])
                counter += 1

        plt.tight_layout()
        if to_png:
            plt.savefig(f'plots/{png_name}.png')
        plt.show()