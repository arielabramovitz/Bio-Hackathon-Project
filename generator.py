"""
This module contains the MovieGenerator class, which is responsible for generating a sequence of frames, simulating molecular dynamics
"""
import json
from typing import Tuple, Dict, List

import numpy as np

import dynamics as dynamics


# enumerate the particle types - TCR, DC45, LCK
class ParticleType:
    TCR = 1
    CD45 = 2
    LCK = 3


class SimulationParameters:
    # properties
    # D-coefficients
    # interaction coefficients

    # constructor
    def __init__(self, d_coefficients: Dict[int, float],
                 interaction_coefficients: Dict[Tuple[int, int], Tuple[float, float, float]]):
        self.D_TCR = d_coefficients[ParticleType.TCR]
        self.D_CD45 = d_coefficients[ParticleType.CD45]
        self.D_LCK = d_coefficients[ParticleType.LCK]

        self.R_TCR_CD45 = interaction_coefficients[(ParticleType.TCR, ParticleType.CD45)][0]
        self.R_TCR_LCK = interaction_coefficients[(ParticleType.TCR, ParticleType.LCK)][0]
        self.R_CD45_LCK = interaction_coefficients[(ParticleType.CD45, ParticleType.LCK)][0]

        self.DREST_TCR_CD45 = interaction_coefficients[(ParticleType.TCR, ParticleType.CD45)][1]
        self.DREST_TCR_LCK = interaction_coefficients[(ParticleType.TCR, ParticleType.LCK)][1]
        self.DREST_CD45_LCK = interaction_coefficients[(ParticleType.CD45, ParticleType.LCK)][1]

        self.K_TCR_CD45 = interaction_coefficients[(ParticleType.TCR, ParticleType.CD45)][2]
        self.K_TCR_LCK = interaction_coefficients[(ParticleType.TCR, ParticleType.LCK)][2]
        self.K_CD45_LCK = interaction_coefficients[(ParticleType.CD45, ParticleType.LCK)][2]


class MovieGenerator:
    # properties
    # simulation parameters (D-coefficients, interaction coefficients)
    # delta_t (seconds)
    # number of frames
    # number of particles (of each type)
    # frame dimensions

    # constructor
    def __init__(self, simulation_parameters: SimulationParameters, delta_t: float, number_of_frames: int,
                 number_of_particles: Tuple[int, int, int], frame_dimensions: Tuple[float, float]):
        self.simulation_parameters = simulation_parameters
        self.number_of_frames = number_of_frames
        self.delta_t = delta_t
        self.number_of_particles = number_of_particles
        self.frame_dimensions = frame_dimensions

        self.frames: List[np.ndarray] = []  # TODO: cut precision to X digits after the decimal point?

        self.rng = np.random.default_rng()  # TODO: seed?

    # methods
    # generate a sequence of frames
    def generate(self):
        # initialize the first frame
        self.init_simulation()

        for i in range(1, self.number_of_frames):
            self.frames.append(self.generate_frame())

    def save(self, path: str):
        # save the frames to a file, in the following format:
        # header lines:
        #   <number_of_frames (int)>
        #   <frame_width (double)> <frame_length (double)>
        #   <number_of_molecules_in_frame (int)>
        # frame lines:
        #   <frame_number (int)>
        #   <molecule_type (int)> <x (double)> <y (double)>

        with open(path, 'w') as f:
            # write the header lines
            f.write(str(self.number_of_frames) + '\n')
            f.write(str(self.frame_dimensions[0]) + ' ' + str(self.frame_dimensions[1]) + '\n')
            f.write(str(self.number_of_particles[0] + self.number_of_particles[1] + self.number_of_particles[2]) + '\n')

            # write the frame lines
            for i in range(len(self.frames)):
                f.write(str(i) + '\n')
                for j in range(self.number_of_particles[0] + self.number_of_particles[1] + self.number_of_particles[2]):
                    f.write(str(int(self.frames[i][j, 2])) + ' ' + str(self.frames[i][j, 0]) + ' ' + str(
                        self.frames[i][j, 1]) + '\n')

    # generate a single frame
    def generate_frame(self) -> np.ndarray:
        last_frame = self.frames[-1]

        # calculate distances between all particles
        distances = np.zeros((self.number_of_particles[0] + self.number_of_particles[1] + self.number_of_particles[2],
                              self.number_of_particles[0] + self.number_of_particles[1] + self.number_of_particles[2]))
        for i in range(self.number_of_particles[0] + self.number_of_particles[1] + self.number_of_particles[2]):
            for j in range(i + 1,
                           self.number_of_particles[0] + self.number_of_particles[1] + self.number_of_particles[2]):
                distances[i, j] = np.linalg.norm(last_frame[i, :2] - last_frame[j, :2])
                distances[j, i] = distances[i, j]

        # calculate the forces on each particle (only from particles of different types, and only if the distance is between DREST and R))
        forces = np.zeros((self.number_of_particles[0] + self.number_of_particles[1] + self.number_of_particles[2], 2))

        # calculate the forces on the TCR particles
        for i in range(self.number_of_particles[0]):
            # calculate the forces from the DC45 particles
            for j in range(self.number_of_particles[0], self.number_of_particles[0] + self.number_of_particles[1]):
                # calculate the force
                if self.simulation_parameters.DREST_TCR_CD45 < distances[i, j] < self.simulation_parameters.R_TCR_CD45:
                    d_vec = last_frame[i, :2] - last_frame[j, :2]
                    force = self.calculate_force(
                        distances[i, j], d_vec,
                        self.simulation_parameters.DREST_TCR_CD45, self.simulation_parameters.K_TCR_CD45
                    )
                    forces[i, :] += force
                    forces[j, :] -= force

            # calculate the forces from the LCK particles
            for j in range(self.number_of_particles[0] + self.number_of_particles[1],
                           self.number_of_particles[0] + self.number_of_particles[1] + self.number_of_particles[2]):
                # calculate the force
                if self.simulation_parameters.DREST_TCR_LCK < distances[i, j] < self.simulation_parameters.R_TCR_LCK:
                    d_vec = last_frame[i, :2] - last_frame[j, :2]
                    force = self.calculate_force(
                        distances[i, j], d_vec,
                        self.simulation_parameters.DREST_TCR_LCK, self.simulation_parameters.K_TCR_LCK
                    )
                    forces[i, :] += force
                    forces[j, :] -= force

        # calculate the forces on the DC45 particles
        for i in range(self.number_of_particles[0], self.number_of_particles[0] + self.number_of_particles[1]):
            # calculate the forces from the LCK particles
            for j in range(self.number_of_particles[0] + self.number_of_particles[1],
                           self.number_of_particles[0] + self.number_of_particles[1] + self.number_of_particles[2]):
                # calculate the force
                if self.simulation_parameters.DREST_CD45_LCK < distances[i, j] < self.simulation_parameters.R_CD45_LCK:
                    d_vec = last_frame[i, :2] - last_frame[j, :2]
                    force = self.calculate_force(
                        distances[i, j], d_vec,
                        self.simulation_parameters.DREST_CD45_LCK, self.simulation_parameters.K_CD45_LCK
                    )
                    forces[i, :] += force
                    forces[j, :] -= force

        # compute the new positions using brownian dynamics
        new_frame = np.zeros(
            (self.number_of_particles[0] + self.number_of_particles[1] + self.number_of_particles[2], 3))
        for i in range(self.number_of_particles[0] + self.number_of_particles[1] + self.number_of_particles[2]):
            diffusion = (
                self.simulation_parameters.D_TCR if i < self.number_of_particles[0]
                else self.simulation_parameters.D_CD45 if i < self.number_of_particles[0] + self.number_of_particles[1]
                else self.simulation_parameters.D_LCK
            )

            new_frame[i, :2] = self.keep_in_bounds(
                last_frame[i, :2] + self.compute_position_change(forces[i, :], diffusion))
            new_frame[i, 2] = last_frame[i, 2]

        return new_frame

    # calculate the new position of a particle using brownian dynamics
    def compute_position_change(self, force: np.ndarray, diffusion: float) -> float:

        random_vector = self.rng.normal(0, 1, 2)
        return self.delta_t * diffusion / dynamics.kT * force + np.sqrt(
            2 * diffusion * self.delta_t) * random_vector  # TODO verify BD equation

    # calculate the force between two particles
    def calculate_force(self, distance: float, d_vec: np.ndarray, r0: float, k: float) -> np.ndarray:
        f_magnitude = dynamics.harmonic_potential_derivative(distance, r0, k)

        return -f_magnitude * d_vec / distance

    def init_simulation(self):
        # initialize the first frame
        frame = np.zeros((self.number_of_particles[0] + self.number_of_particles[1] + self.number_of_particles[2], 3))
        # generate the TCR particles
        frame[:self.number_of_particles[0], 0] = np.random.uniform(0, self.frame_dimensions[0],
                                                                   self.number_of_particles[0])
        frame[:self.number_of_particles[0], 1] = np.random.uniform(0, self.frame_dimensions[1],
                                                                   self.number_of_particles[0])
        frame[:self.number_of_particles[0], 2] = ParticleType.TCR

        # generate the DC45 particles
        frame[self.number_of_particles[0]:self.number_of_particles[0] + self.number_of_particles[1], 0] = \
            np.random.uniform(0, self.frame_dimensions[0], self.number_of_particles[1])
        frame[self.number_of_particles[0]:self.number_of_particles[0] + self.number_of_particles[1], 1] = \
            np.random.uniform(0, self.frame_dimensions[1], self.number_of_particles[1])
        frame[self.number_of_particles[0]:self.number_of_particles[0] + self.number_of_particles[1],
        2] = ParticleType.CD45

        # generate the LCK particles
        frame[self.number_of_particles[0] + self.number_of_particles[1]:, 0] = \
            np.random.uniform(0, self.frame_dimensions[0], self.number_of_particles[2])
        frame[self.number_of_particles[0] + self.number_of_particles[1]:, 1] = \
            np.random.uniform(0, self.frame_dimensions[1], self.number_of_particles[2])
        frame[self.number_of_particles[0] + self.number_of_particles[1]:, 2] = ParticleType.LCK
        self.frames.append(frame)

    def keep_in_bounds(self, location: np.ndarray) -> np.ndarray:
        for i in range(2):
            if location[i] < 0:
                location[i] = -location[i]
            elif location[i] > self.frame_dimensions[i]:
                location[i] = 2 * self.frame_dimensions[i] - location[i]

        return location


def parse(config_file: str):
    with open(config_file, 'r') as f:
        config = json.load(f)

    d_coefficients = {ParticleType.TCR: config["D_TCR"],
                      ParticleType.CD45: config["D_CD45"],
                      ParticleType.LCK: config["D_LCK"]}

    interaction_parameters = {(ParticleType.TCR, ParticleType.CD45):
                                  (config["TCR_CD45"]["R"], config["TCR_CD45"]["DREST"], config["TCR_CD45"]["K"]),
                              (ParticleType.TCR, ParticleType.LCK):
                                  (config["TCR_LCK"]["R"], config["TCR_LCK"]["DREST"], config["TCR_LCK"]["K"]),
                              (ParticleType.CD45, ParticleType.LCK):
                                  (config["CD45_LCK"]["R"], config["CD45_LCK"]["DREST"], config["CD45_LCK"]["K"])}
    parameters = SimulationParameters(d_coefficients, interaction_parameters)
    generator = MovieGenerator(parameters, config["delta_t"], config["number_of_frames"],
                               (config["TCR_count"], config["CD45_count"], config["LCK_count"]),
                               (config["frame_width"], config["frame_length"]))

    return generator


if __name__ == '__main__':
    # parameters = SimulationParameters({ParticleType.LCK: 0.1, ParticleType.CD45: 0.2, ParticleType.TCR: 0.3},
    #                                   {(ParticleType.TCR, ParticleType.CD45): (0.1, 0.2, 0.3),
    #                                    (ParticleType.TCR, ParticleType.LCK): (0.4, 0.5, 0.6),
    #                                    (ParticleType.CD45, ParticleType.LCK): (0.7, 0.8, 0.9)})
    # generator = MovieGenerator(parameters, 1, 50, (10, 10, 10), (30, 30))
    generator = parse('config.json')

    generator.generate()

    generator.save('test1.txt')
