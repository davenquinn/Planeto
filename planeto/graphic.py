import click
import fiona
import rasterio
import numpy as N
from sys import stdout
from json import dumps
from shapely.geometry import shape, mapping
from shapely.ops import transform

def features(srcfile):
    with fiona.open(srcfile) as src:
        for feature in src:
            yield feature

def planetocentric_transform(semimajor, semiminor):
    flattening_factor = (semiminor/semimajor)**2

    def planetocentric(latitude):
        """Converts a planetographic latitude to planetocentric
        """
        assert abs(latitude) <= 90
        _ = N.tan(N.radians(latitude))/flattening_factor
        return N.degrees(N.arctan(_))

    def tfunc(x,y,z=None):
        y = planetocentric(y)
        return tuple(
            i for i in (x,y,z)
            if i is not None)

    def transform_feature(f):
        g = shape(f['geometry'])
        g2 = transform(tfunc,g)
        f['geometry'] = mapping(g2)
        return f

    return transform_feature

@click.command()
@click.argument('infile', default='-')
@click.argument('outfile', default='-')
@click.option('--axes','-a', default=(3396190,3376200), nargs=2,
    help="Specify major and minor axes directly (takes precedence over other arguments)",
    type=float)
@click.option('--proj','-p', help="Projection definition from which to extract axes lengths.")
@click.option('--format','-f',default='GeoJSON')
def cli(infile,outfile, axes=None, proj=None, format='GeoJSON'):
    """
    Converts from planetocentric to planetographic coordinate systems.
    If OUTFILE is not specified, dumps GeoJSON to stdout.
    """
    source = features(infile)
    func = planetocentric_transform(*axes)

    if outfile=='-':
        with stdout as sink:
            coll = dict(
                type='FeatureCollection',
                features=[func(f) for f in source])
            sink.write(dumps(coll))
