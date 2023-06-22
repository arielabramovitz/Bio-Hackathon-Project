# -*- coding: utf-8 -*-
"""
Created on Wed Jun 21 10:12:28 2023

@author: Avishai
"""
import argparse
import sys

import up_scale


# import viewer # TODO complete API


def run_generator(config_file: str, output_file: str):
    pass


def run_up_res(input_file: str, output_file: str, resolution_factor: int = 10) -> None:
    metadata, original_frames = up_scale.parse(input_file)
    number_of_frames, frame_width, frame_length, number_of_molecules = metadata

    frame_dimensions = (frame_width, frame_length)
    original_delta_t = 1  # TODO: get from metadata?

    up_scaler = up_scale.UpScaler(original_frames, resolution_factor, original_delta_t, frame_dimensions)

    # TODO: call learning methods

    up_scaler.up_scale()
    up_scaler.save(output_file)


def run_viewer(input_file: str):
    pass


if __name__ == '__main__':

    # Create the parser and add arguments
    parser = argparse.ArgumentParser()
    parser.add_argument(dest='Tool_name', help="Name of desire tool")
    # parser.add_argument(dest='input', help="txt file", choices=glob.glob('*.txt'))
    parser.add_argument(dest='input', help="txt file")

    # optional arguments
    parser.add_argument(dest='output', help="txt file", nargs='?', default="")
    parser.add_argument(dest='resolution_factor', help="integer", nargs='?', default=1)

    # Parse and print the results
    cli_args = vars(parser.parse_args())
    tool_name = cli_args['Tool_name']
    input_file = cli_args['input']
    output_file = cli_args['output']
    resolution_factor = cli_args['resolution_factor']

    # TODO: validate args

    if tool_name == "generator":
        run_generator(input_file, output_file)
    elif tool_name == "upres":
        run_up_res(input_file, output_file, int(resolution_factor))
    elif tool_name == "viewer":
        run_viewer(input_file)
    else:
        sys.exit("please choose one from: Generator, Up-Res, Viewer")

    # all_tools = list(["Generator", "Up-Res", "Viewer"])
    # all_tools_str = ','.join([str(elem) for elem in all_tools])  # convert to string
    #
    # # exit if incorrect tool name
    # if (tool_name not in all_tools):
    #     sys.exit("please choose one from: " + all_tools_str)
    #
    # # TODO complete API
    # # if (cli_args['Tool_name'] == "Up-Res"):
    # #     up_res.run(input_file)
    #
    # # if (cli_args['Tool_name'] == "Viewer"):
    # #     viewer.run(input_file)
    # # else:
    #
    # # read file and split by "\n"
    # with open(input_file, 'r') as file:
    #     args = file.read().replace('\n', ',')
    # args = args.split(",")
    #
    # args_values = list()
    #
    # # find args values and append
    # pattern = "^.*= "
    # # Replace all occurrences of character s with an empty string
    # for i, arg in enumerate(args):
    #     args_values.append(re.sub(pattern, '', arg))
    #
    # # find args names and append
    # args_names = list()
    # pattern = " .*$"
    # # Replace all occurrences of character s with an empty string
    # for i, arg in enumerate(args):
    #     args_names.append(re.sub(pattern, '', arg))
    #
    # # create dict
    # dict = {args_names[i]: args_values[i] for i in range(len(args_names))}
    #
    # needed_args = ['TCR_D', 'CD45_D', 'LCK_D',
    #                'TCR_CD45_R', 'TCR_LCK_R', 'CD45_LCK_R',
    #                'TCR_CD45_DREST', 'TCR_LCK_DREST', 'CD45_LCK_DREST',
    #                'TCR_CD45_K', 'TCR_LCK_K', 'CD45_LCK_K',
    #                "number_of_frames", "frame_width", "frame_length",
    #                "number_of_molecules_in_frame"]
    #
    # # delete non relevant args
    # for key in dict.copy().keys():
    #     if (key not in needed_args):
    #         del dict[key]
    #
    # # check that all args is exiting
    # for needed_arg in needed_args:
    #     if (needed_arg not in dict.keys()):
    #         sys.exit("Please specify '" + needed_arg + "' arg")
    #
    # # TODO complete API
    # # generator.run(dict)
