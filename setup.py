import os
from setuptools import setup

def package_data(pkg, root_list):
    """Generic function to find package_data for `pkg` under `root`."""
    data = []
    for root in root_list:
        for dirname, _, files in os.walk(os.path.join(pkg, root)):
            for fname in files:
                data.append(os.path.relpath(os.path.join(dirname, fname), pkg))

    return {pkg: data}

setup(
    name='xblock-js-parsons',
    version='0.2',
    author='Lassi Haaranen',
    description='XBlock - js-parsons',
    packages=['js_parsons'],
    install_requires=[
        'XBlock',
    ],
    entry_points={
        'xblock.v1': 'js-parsons = js_parsons:JSParsonsXBlock',
    },
    package_data=package_data("js_parsons", [ "public"]),
)
