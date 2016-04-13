import click
import fiona
import rasterio

from affine import Affine

from IPython import embed

@click.command()
@click.argument("dataset")
def cli(dataset):
    with rasterio.open(dataset) as ds:
        embed()

