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

    logger.info(f"Set price range [{args.min_price}, {args.max_price}]")
    idx = cleaned_data['price'].between(args.min_price, args.max_price)
    cleaned_data = cleaned_data[idx].copy()

    idx = cleaned_data['longitude'].between(-74.25, -73.50) & cleaned_data['latitude'].between(40.5, 41.2)
    cleaned_data = cleaned_data[idx].copy()
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
        help='path to the raw data artifact', # '## INSERT DESCRIPTION HERE,
        required=True
    )

    parser.add_argument(
        "--output_artifact", 
        type= str, ## INSERT TYPE HERE: str, float or int,
        help='path to cleaned data artifacts', ## INSERT DESCRIPTION HERE,
        required=True
    )

    parser.add_argument(
        "--output_type", 
        type=str, ## INSERT TYPE HERE: str, float or int,
        help='output artifact type', ## INSERT DESCRIPTION HERE,
        required=True
    )

    parser.add_argument(
        "--output_description", 
        type=str, ## INSERT TYPE HERE: str, float or int,
        help='description for the artifact', ## INSERT DESCRIPTION HERE,
        required=True
    )

    parser.add_argument(
        "--min_price",
        type=float, ## INSERT TYPE HERE: str, float or int,
        help='lower boundary for price', ## INSERT DESCRIPTION HERE,
        required=True
    )
    parser.add_argument(
        "--max_price",
        type=float, ## INSERT TYPE HERE: str, float or int,
        help='upper boundry for price', ## INSERT DESCRIPTION HERE,
        required=True
    )
    args = parser.parse_args()

    go(args)
