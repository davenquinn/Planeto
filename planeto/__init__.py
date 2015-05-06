def planetocentric_transform(semimajor, semiminor):
    """Converts a planetographic latitude to planetocentric
        using a shapefile as a guide for the projection
    """
    if semiminor is None:
        flattening_factor = 1
    else:
        flattening_factor = (semiminor/semimajor)**2

    def transform_func(x,y,z=None):
        assert abs(y) <= 90
        lat = N.tan(N.radians(y))*flattening_factor
        y = N.degrees(N.arctan(lat))
        return (x,y)

    return lambda s: transform(transform_func, s)

def axis_lengths(shapefile, inverse_flattening=None):
    """
    Gets the length of the geoid's semimajor and semiminor
    axes from a shapefile's projection.
    """
    prj = os.path.splitext(shapefile)[0]+".prj"
    with open(prj,"r") as proj:
        spatial_ref = osr.SpatialReference()
        spatial_ref.ImportFromWkt(proj.read())
    semimajor = spatial_ref.GetSemiMajor()
    semiminor = spatial_ref.GetSemiMinor()
    if inverse_flattening:
        # We allow the user to specify their own value for inverse
        # flattening, because this is required for Earth-Mars CRS
        # translations
        semiminor = semimajor-semimajor/inverse_flattening
    return semimajor, semiminor
