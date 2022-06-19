#!/usr/bin/env python
"""
An example of a step using MLflow and Weights & Biases
"""
import argparse
import logging
import os

import pandas as pd
import wandb


logging.basicConfig(level=logging.INFO, format="%(asctime)-15s %(message)s")
logger = logging.getLogger()


def go(args):

    run = wandb.init(job_type="basic_cleaning")
    run.config.update(args)

    # Download input artifact. This will also log that this script is using this
    # particular version of the artifact
    # artifact_local_path = run.use_artifact(args.input_artifact).file()

    ######################
    # YOUR CODE HERE     #
    ######################
    saved_file = 'cleaned_file.csv'

    run = wandb.init(job_type=args.output_type)

    logger.info(f"Getting raw_data")
    artifact = run.use_artifact(args.input_artifact)
    input_path = artifact.file()
    raw_data = pd.read_csv(input_path)

    logger.info(f"Cleaning raw_data")
    cols_to_remove = ['id', 'host_name', 'host_id', 'neighbourhood']
    for col in cols_to_remove:
        raw_data = raw_data.drop(col, axis=1)
    cleaned_data = raw_data
    cleaned_data.to_csv(saved_file, index=False)

    logger.info(f"Saving output artifact")
    artifact = wandb.Artifact(
        name=args.output_artifact,
        type=args.output_type,
        description=args.output_description
    )
    artifact.add_file(saved_file)
    run.log_artifact(artifact_or_path=artifact)
    os.remove(saved_file)


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="cleaning data basicly")


    parser.add_argument(
        "--input_artifact", 
        type=str, #'## INSERT TYPE HERE: str, float or int,
        help='', # '## INSERT DESCRIPTION HERE,
        required=True
    )

    parser.add_argument(
        "--output_artifact", 
        type= str, ## INSERT TYPE HERE: str, float or int,
        help='', ## INSERT DESCRIPTION HERE,
        required=True
    )

    parser.add_argument(
        "--output_type", 
        type=str, ## INSERT TYPE HERE: str, float or int,
        help='', ## INSERT DESCRIPTION HERE,
        required=True
    )

    parser.add_argument(
        "--output_description", 
        type=str, ## INSERT TYPE HERE: str, float or int,
        help='', ## INSERT DESCRIPTION HERE,
        required=True
    )

    args = parser.parse_args()

    go(args)
