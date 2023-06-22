from typing import List, Tuple

import numpy as np

import dynamics
import generator


class UpScaler:
    """
    This class is responsible for up scaling a given movie.

    :param frames: the frames of the original movie
    :param resolution_factor: the factor by which to increase the resolution
    :param delta_t: the time step of the original movie
    :param frame_dimensions: the dimensions of the frames
    """

    def __init__(self, frames: List[np.ndarray], resolution_factor: int, delta_t: float,
                 frame_dimensions: Tuple[float, float]):

        self.original_frames = frames
        self.resolution_factor = resolution_factor
        self.delta_t = delta_t / self.resolution_factor
        self.frame_dimensions = frame_dimensions  # TODO: fill using parser

        # self.simulation_parameters = SimulationParameters({}, {})  # TODO: fill using learning (MSD, ...)
        self.simulation_parameters = generator.SimulationParameters(
            {generator.ParticleType.LCK: 0.1, generator.ParticleType.CD45: 0.2, generator.ParticleType.TCR: 0.3},
            {(generator.ParticleType.TCR, generator.ParticleType.CD45): (0.1, 0.2, 0.3),
             (generator.ParticleType.TCR, generator.ParticleType.LCK): (0.4, 0.5, 0.6),
             (generator.ParticleType.CD45, generator.ParticleType.LCK): (0.7, 0.8, 0.9)})

        self.frames = [self.original_frames[0]]
        self.rng = np.random.default_rng()  # TODO: seed?

        # calculate the number of particles of each type
        self.number_of_particles = np.zeros(3, dtype=int)
        for i in range(self.frames[0].shape[0]):
            self.number_of_particles[int(self.frames[0][i, 2]) - 1] += 1

    def up_scale(self) -> None:
        """
        This method up scales the movie.
        """

        # loop over the frames, and add resolution_factor frames between each pair of frames
        for i in range(1, len(self.original_frames)):

            # a vector that points from the previous frame to the current frame
            direction_force_vector = self.original_frames[i][:, :2] - self.original_frames[i - 1][:, :2]

            for j in range(self.resolution_factor):

                self.frames.append(
                    self.generate_frame(self.frames[-1], direction_force_vector)
                )

                # every 5 frames, update the direction_force_vector
                if j % 5 == 0:
                    direction_force_vector = self.original_frames[i][:, :2] - self.frames[-1][:, :2]

            self.frames.append(self.original_frames[i])

    def generate_frame(self, frame: np.ndarray, direction_force_vector: np.ndarray):
        """
        This method generates a new frame, based on the previous frame and the direction_force_vector
        """
        # TODO: take into account the interaction between the particles
        force = direction_force_vector + self.calculate_interaction_force(frame)

        new_frame = np.zeros((frame.shape[0], 3))

        for i in range(frame.shape[0]):
            diffusion = (
                self.simulation_parameters.D_TCR if frame[i, 2] == generator.ParticleType.TCR
                else self.simulation_parameters.D_DC45 if frame[i, 2] == generator.ParticleType.CD45
                else self.simulation_parameters.D_LCK
            )

            new_frame[i, :2] = self.keep_in_bounds(
                frame[i, :2] + self.compute_position_change(force[i, :], diffusion))
            new_frame[i, 2] = frame[i, 2]

        return new_frame

    def calculate_interaction_force(self, frame: np.ndarray) -> np.ndarray:
        """
        This method calculates the interaction force between the particles in the given frame.
        """
        # calculate distances between all particles
        distances = np.zeros((frame.shape[0], frame.shape[0]))
        for i in range(frame.shape[0]):
            for j in range(i + 1, frame.shape[0]):
                distances[i, j] = np.linalg.norm(frame[i, :2] - frame[j, :2])
                distances[j, i] = distances[i, j]

        # calculate the forces on each particle
        forces = np.zeros((frame.shape[0], 2))

        # calculate the forces on the TCR particles
        for i in range(self.number_of_particles[0]):
            # calculate the forces from the DC45 particles
            for j in range(self.number_of_particles[0], self.number_of_particles[0] + self.number_of_particles[1]):
                # calculate the force
                if self.simulation_parameters.DREST_TCR_DC45 < distances[i, j] < self.simulation_parameters.R_TCR_DC45:
                    d_vec = frame[i, :2] - frame[j, :2]
                    force = self.calculate_force(
                        distances[i, j], d_vec,
                        self.simulation_parameters.DREST_TCR_DC45, self.simulation_parameters.K_TCR_DC45
                    )
                    forces[i, :] += force
                    forces[j, :] -= force

            # calculate the forces from the LCK particles
            for j in range(self.number_of_particles[0] + self.number_of_particles[1],
                           self.number_of_particles[0] + self.number_of_particles[1] + self.number_of_particles[2]):
                # calculate the force
                if self.simulation_parameters.DREST_TCR_LCK < distances[i, j] < self.simulation_parameters.R_TCR_LCK:
                    d_vec = frame[i, :2] - frame[j, :2]
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
                if self.simulation_parameters.DREST_DC45_LCK < distances[i, j] < self.simulation_parameters.R_DC45_LCK:
                    d_vec = frame[i, :2] - frame[j, :2]
                    force = self.calculate_force(
                        distances[i, j], d_vec,
                        self.simulation_parameters.DREST_DC45_LCK, self.simulation_parameters.K_DC45_LCK
                    )
                    forces[i, :] += force
                    forces[j, :] -= force

        return forces

    def calculate_force(self, distance: float, d_vec: np.ndarray, r0: float, k: float) -> np.ndarray:
        """
        This method calculates the force between two particles, based on the given distance, d_vec, d_rest and k.
        """
        f_magnitude = dynamics.harmonic_potential_derivative(distance, r0, k)

        return -f_magnitude * d_vec / distance

    def keep_in_bounds(self, location: np.ndarray):  # TODO: make static function in generator
        """
        This method keeps the given location in the bounds of the frame.
        """
        for i in range(2):
            if location[i] < 0:
                location[i] = -location[i]
            elif location[i] > self.frame_dimensions[i]:
                location[i] = 2 * self.frame_dimensions[i] - location[i]

        return location

    def compute_position_change(self, force: np.ndarray, diffusion: float):
        """
        This method computes the change in position of a particle, based on the given force and diffusion.
        """

        random_vector = self.rng.normal(0, 1, 2)
        return self.delta_t * diffusion / dynamics.kT * force + np.sqrt(
            2 * diffusion * self.delta_t) * random_vector  # TODO verify BD equation

    def learn_D(self):
        for mol_type in ["CD45", "LCK", "TCR"]:
            # TODO: add func
            pass

    def learn_r(self):
        for couple in ["CD45_LCK", "CD45_TCR", "LCK_TCR"]:
            # TODO: add func
            pass

    def learn_k(self):
        for couple in ["CD45_LCK", "CD45_TCR", "LCK_TCR"]:
            # TODO: add func
            pass

    def learn_drest(self):
        for couple in ["CD45_LCK", "CD45_TCR", "LCK_TCR"]:
            # TODO: add func
            pass

    def save(self, path: str):

        with open(path, 'w') as f:
            # write the header lines
            f.write(str(len(self.frames)) + '\n')
            f.write(str(self.frame_dimensions[0]) + ' ' + str(self.frame_dimensions[1]) + '\n')
            f.write(str(self.frames[0].shape[0]) + '\n')

            # write the frame lines
            for i in range(len(self.frames)):
                f.write(str(i) + '\n')
                for j in range(self.frames[0].shape[0]):
                    f.write(str(int(self.frames[i][j, 2])) + ' ' + str(self.frames[i][j, 0]) + ' ' + str(
                        self.frames[i][j, 1]) + '\n')


def parse(file_name: str) -> Tuple[np.ndarray, List[np.ndarray]]:
    """
    This function parses the given file, and returns the information in it.

    :return: a tuple containing the basic information and the positions array
    the basic information is a numpy array containing the number of frames, the frame width, the frame length and the
    number of molecules
    """
    xyz_file = open(file_name, 'r')
    number_of_frames = int(xyz_file.readline())
    frame_info = xyz_file.readline().split()
    frame_width = int(frame_info[0])
    frame_length = int(frame_info[1])
    number_of_molecules = int(xyz_file.readline())

    movie_info = np.array([number_of_frames, frame_width, frame_length, number_of_molecules])  # basic information
    position_array = list()  # molecules positions

    for frame_index in range(number_of_frames):
        frame = np.zeros(shape=(number_of_molecules, 3))
        xyz_file.readline()  # frame number
        for molecule_index in range(number_of_molecules):
            current_molecule = xyz_file.readline().split()

            frame[molecule_index, 0] = float(current_molecule[1])
            frame[molecule_index, 1] = float(current_molecule[2])
            frame[molecule_index, 2] = float(current_molecule[0])

        position_array.append(frame)

    return movie_info, position_array


if __name__ == '__main__':
    # parameters = SimulationParameters({ParticleType.LCK: 0.1, ParticleType.CD45: 0.2, ParticleType.TCR: 0.3},
    #                                   {(ParticleType.TCR, ParticleType.CD45): (0.1, 0.2, 0.3),
    #                                    (ParticleType.TCR, ParticleType.LCK): (0.4, 0.5, 0.6),
    #                                    (ParticleType.CD45, ParticleType.LCK): (0.7, 0.8, 0.9)})
    # generator = MovieGenerator(parameters, 1, 50, (30, 30, 30), (50, 50))
    #
    # generator.generate()
    # generator.save("test_res_original.txt")

    movie_info, original_frames = parse("test_res_original")
    number_of_frames, frame_width, frame_length, number_of_molecules = movie_info

    up_scaler = UpScaler(original_frames, 10, 1, (frame_width, frame_length))
    up_scaler.up_scale()
    up_scaler.save("test_res_upscaled.txt")
