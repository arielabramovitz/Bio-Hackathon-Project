# -*- coding: utf-8 -*-
"""
Created on Wed Jun 21 10:12:28 2023

@author: Avishai
"""
import argparse
import os
import sys
from typing import List, Tuple

import numpy as np

import generator
import up_scale
import viewer


def run_generator(config_file: str, output_file: str) -> generator.MovieGenerator:
    movie_generator = generator.parse(config_file)
    movie_generator.generate()
    movie_generator.save(output_file)

    return movie_generator


def run_up_res(input_file: str, output_file: str, resolution_factor: int = 10) -> None:
    metadata, original_frames = up_scale.parse(input_file)
    number_of_frames, frame_width, frame_length, number_of_molecules = metadata

    frame_dimensions = (frame_width, frame_length)
    original_delta_t = 0.1  # TODO: get from metadata?

    up_scaler = up_scale.UpScaler(original_frames, resolution_factor, original_delta_t, frame_dimensions)

    # TODO: call learning methods

    up_scaler.up_scale()
    up_scaler.save(output_file)


def run_viewer(input_file: str, is_3d: bool):
    if not is_3d:
        viewer.viewer(input_file)
    else:
        viewer.viewer_3d(input_file)


def save(frames: List[np.ndarray], frame_dimensions: Tuple[float, float], output: str):
    with open(output, 'w') as f:
        # write the header lines
        f.write(str(len(frames)) + '\n')
        f.write(str(frame_dimensions[0]) + ' ' + str(frame_dimensions[1]) + '\n')
        f.write(str(frames[0].shape[0]) + '\n')

        # write the frame lines
        for i in range(len(frames)):
            f.write(str(i) + '\n')
            for j in range(frames[0].shape[0]):
                f.write(str(int(frames[i][j, 2])) + ' ' + str(frames[i][j, 0]) + ' ' + str(frames[i][j, 1]) + '\n')


def cut_frames(original_movie: str, new_original: str, low_res: str, resolution_factor: int):
    metadata, original_frames = up_scale.parse(original_movie)
    number_of_frames, frame_width, frame_length, number_of_molecules = metadata

    low_res_number_of_frames = int((number_of_frames - 1) / resolution_factor + 1)
    new_high_res_number_of_frames = (low_res_number_of_frames - 1) * resolution_factor + 1

    new_high_res_frames = original_frames[:new_high_res_number_of_frames]
    low_res_frames = new_high_res_frames[::resolution_factor]

    save(new_high_res_frames, (frame_width, frame_length), new_original)
    save(low_res_frames, (frame_width, frame_length), low_res)


def run_pipeline(config_file: str, output_file: str, resolution_factor: int):
    run_generator(config_file, ".\\temp\\original.txt")

    cut_frames(".\\temp\\original.txt", ".\\temp\\new_original.txt", ".\\temp\\low_res.txt", resolution_factor)

    run_up_res(".\\temp\\low_res.txt", output_file, resolution_factor)


if __name__ == '__main__':

    # TODO: add delta_t to movie format metadata

    # Create the parser and add arguments
    parser = argparse.ArgumentParser()
    parser.add_argument(dest='tool_name')
    parser.add_argument(dest='first_arg')

    # optional arguments
    parser.add_argument(dest='second_arg', nargs='?', default="")
    parser.add_argument(dest='third_arg', nargs='?', default=1)

    # Parse and print the results
    cli_args = vars(parser.parse_args())

    tool_name = cli_args['tool_name']
    if tool_name not in {"generator", "upres", "viewer", "pipeline"}:
        print("please choose one from: generator, upres, viewer, pipeline")
        sys.exit(1)

    if tool_name == "generator":
        config_file = cli_args['first_arg']
        output_file = cli_args['second_arg']

        # validate config file (must be json, must exist)
        if not config_file.endswith(".json"):
            print("config file must be json")
            sys.exit(1)
        if not os.path.exists(config_file):
            print("config file does not exist")
            sys.exit(1)

        # validate output file (not empty)
        if output_file == "":
            print("output file must be specified")
            sys.exit(1)

        run_generator(config_file, output_file)

    elif tool_name == "upres":
        input_file = cli_args['first_arg']
        output_file = cli_args['second_arg']
        resolution_factor = cli_args['third_arg']

        # validate input file (must exist)
        if not os.path.exists(input_file):
            print("input file does not exist")
            sys.exit(1)

        # validate output file (not empty)
        if output_file == "":
            print("output file must be specified")
            sys.exit(1)

        # validate resolution factor (must be int, must be positive)
        if not resolution_factor.isdigit() or int(resolution_factor) <= 0:
            print("resolution factor must be positive integer")
            sys.exit(1)

        run_up_res(input_file, output_file, int(resolution_factor))

    elif tool_name == "viewer":
        input_file = cli_args['first_arg']
        is_3d = cli_args['second_arg']

        # validate input file (must exist)
        if not os.path.exists(input_file):
            # print("input file does not exist")
            print("input file does not exist")
            sys.exit(1)

        # validate is_3d (must be "" or "3d")
        if is_3d not in {"", "3d"}:
            print("is_3d must be empty or 3d")
            sys.exit(1)

        run_viewer(input_file, is_3d == "3d")

    elif tool_name == "pipeline":

        config_file = cli_args['first_arg']
        output_file = cli_args['second_arg']
        resolution_factor = cli_args['third_arg']

        # validate config file (must be json, must exist)
        if not config_file.endswith(".json"):
            print("config file must be json")
            sys.exit(1)
        if not os.path.exists(config_file):
            print("config file does not exist")
            sys.exit(1)

        # validate output file (not empty)
        if output_file == "":
            print("output file must be specified")
            sys.exit(1)

        # validate resolution factor (must be int, must be positive)
        if not resolution_factor.isdigit() or int(resolution_factor) <= 0:
            print("resolution factor must be positive integer")
            sys.exit(1)

        run_pipeline(config_file, output_file, int(resolution_factor))

    else:
        print("please choose one from: generator, upres, viewer")
        sys.exit(1)
