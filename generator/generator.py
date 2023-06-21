"""
This module contains the MovieGenerator class, which is responsible for generating a sequence of frames, simulating molecular dynamics
"""
from typing import Tuple, Dict, Set, List
import numpy as np


# enumerate the particle types - TCR, DC45, LCK
class ParticleType:
    TCR = 1
    DC45 = 2
    LCK = 3


class SimulationParameters:
    # properties
    # D-coefficients
    # interaction coefficients

    # constructor
    def __init__(self, d_coefficients: Dict[int, float],
                 interaction_coefficients: Dict[Tuple[int, int], Tuple[float, float, float]]):
        self.d_coefficients = d_coefficients
        self.interaction_coefficients = interaction_coefficients


class MovieGenerator:
    # properties
    # simulation parameters (D-coefficients, interaction coefficients)
    # delta_t (seconds)
    # number of frames
    # number of particles (of each type)
    # frame dimensions

    # constructor
    def __init__(self, simulation_parameters, delta_t: float, number_of_frames: int,
                 number_of_particles: Tuple[int, int, int], frame_dimensions: Tuple[float, float]):
        self.simulation_parameters = simulation_parameters
        self.number_of_frames = number_of_frames
        self.delta_t = delta_t
        self.number_of_particles = number_of_particles
        self.frame_dimensions = frame_dimensions

        self.frames: List[np.ndarray] = []

    # methods
    # generate a sequence of frames
    def generate(self):
        # initialize the first frame
        self.init_simulation()

        # for i in range(1, self.number_of_frames):
        #     self.frames.append(self.generate_frame())

    def save(self, path: str):
        # save the frames to a file, in the following format:
        # header lines:
        #   <number_of_frames (int)>
        #   <frame_width (double)> <frame_length (double)>
        #   <number_of_molecules_in_frame (int)>
        # frame lines:
        #   <frame_number (int)>
        #   <molecule_type (int)> <x (double)> <y (double)>

        # write the header lines
        with open(path, 'w') as f:
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
        pass

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
        2] = ParticleType.DC45

        # generate the LCK particles
        frame[self.number_of_particles[0] + self.number_of_particles[1]:, 0] = \
            np.random.uniform(0, self.frame_dimensions[0], self.number_of_particles[2])
        frame[self.number_of_particles[0] + self.number_of_particles[1]:, 1] = \
            np.random.uniform(0, self.frame_dimensions[1], self.number_of_particles[2])
        frame[self.number_of_particles[0] + self.number_of_particles[1]:, 2] = ParticleType.LCK
        self.frames.append(frame)


if __name__ == '__main__':
    parameters = SimulationParameters({ParticleType.LCK: 0.1, ParticleType.DC45: 0.2, ParticleType.TCR: 0.3},
                                      {(ParticleType.LCK, ParticleType.DC45): (0.1, 0.2, 0.3),
                                       (ParticleType.LCK, ParticleType.TCR): (0.4, 0.5, 0.6),
                                       (ParticleType.DC45, ParticleType.TCR): (0.7, 0.8, 0.9)})
    generator = MovieGenerator(parameters, 0.1, 100, (100, 100, 100), (100, 100))

    generator.generate()

    print(generator.frames[0])

    generator.save('test.txt')
