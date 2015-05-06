import click
import fiona
import rasterio

@click.command()
@click.argument("dataset")
def cli(dataset):
    with rasterio.open(dataset) as ds:
        embed()
