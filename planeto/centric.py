from __future__ import division, print_function
import click
import numpy as N

# Mars projection parameters
semimajor = 3396190
semiminor = 3376200
flattening_factor = (semiminor/semimajor)**2

mars2000 = dict(
    no_defs= True,
    proj='longlat',
    units='m',
    a=semimajor,
    b=semiminor)

def planetocentric(latitude):
    """Converts a planetographic latitude to planetocentric
    """

    assert abs(latitude) <= 90
    _ = N.tan(N.radians(latitude))*flattening_factor
    return N.degrees(N.arctan(_))

@click.command()
@click.argument("srcfile",type=click.Path())
@click.argument("dstfile",type=click.Path())
def cli(srcfile, dstfile):
    """
    Transforms a raster dataset from
    planetographic to planetocentric coordinate
    systems. Currently specialized to Mars, with
    data in the Mars2000 (geodetic) coordinate
    system.
    """
    import rasterio
    from affine import Affine

    with rasterio.open(srcfile) as src:

        kwargs = src.meta
        kwargs.pop("transform")
        affine = kwargs.pop("affine")


        aff = list(affine[:6])
        top = aff[5]
        btm = top + src.shape[0]*aff[4]

        # Change top and bottom to planetocentric
        top_new = planetocentric(top)
        btm_new = planetocentric(btm)

        # Construct new affine transform
        aff[5] = top_new
        aff[4] = (btm_new - top_new)/src.shape[0]

        kwargs.update(
            transform = Affine(*aff),
            nodata = 0,
            driver = "GTiff",
            compress = 'lzw',
            crs=mars2000)

        with rasterio.open(dstfile, 'w', **kwargs) as dst:
            xs = N.ceil(src.shape[0]/src.meta["blockysize"])
            ys = N.ceil(src.shape[1]/src.meta["blockxsize"])
            length = int(xs*ys)

            with click.progressbar(src.block_windows(), length=length) as bar:
                for n,window in bar:
                    _ = src.read(1,window=window)
                    dst.write(_,indexes=1,window=window)
