from setuptools import setup, find_packages

install_requires = [
    'fiona',
    'rasterio',
    'Click'
    ]

setup(
    name='Planeto',
    version=0.1,
    description="Facilities for converting between"
                "planetographic and planetocentric"
                "coordinate systems.",
    license='MIT',
    install_requires=install_requires,
    packages=find_packages(),
    package_dir={'planeto':'planeto'},
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Science/Research',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Scientific/Engineering :: GIS',
    ],
    entry_points='''
        [console_scripts]
        planetocentric=planeto.centric:cli
        planetographic=planeto.graphic:cli
    ''',
)
