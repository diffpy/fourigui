|Icon| |title|_
===============

.. |title| replace:: diffpy.fourigui
.. _title: https://diffpy.github.io/fourigui

.. |Icon| image:: https://avatars.githubusercontent.com/diffpy
        :target: https://diffpy.github.io/fourigui
        :height: 100px

|PyPi| |Forge| |PythonVersion| |PR|

|CI| |Codecov| |Black| |Tracking|

.. |Black| image:: https://img.shields.io/badge/code_style-black-black
        :target: https://github.com/psf/black

.. |CI| image:: https://github.com/diffpy/fourigui/actions/workflows/main.yml/badge.svg
        :target: https://github.com/diffpy/fourigui/actions/workflows/main.yml

.. |Codecov| image:: https://codecov.io/gh/diffpy/fourigui/branch/main/graph/badge.svg
        :target: https://codecov.io/gh/diffpy/fourigui

.. |Forge| image:: https://img.shields.io/conda/vn/conda-forge/diffpy.fourigui
        :target: https://anaconda.org/conda-forge/diffpy.fourigui

.. |PR| image:: https://img.shields.io/badge/PR-Welcome-29ab47ff

.. |PyPi| image:: https://img.shields.io/pypi/v/diffpy.fourigui
        :target: https://pypi.org/project/diffpy.fourigui/

.. |PythonVersion| image:: https://img.shields.io/pypi/pyversions/diffpy.fourigui
        :target: https://pypi.org/project/diffpy.fourigui/

.. |Tracking| image:: https://img.shields.io/badge/issue_tracking-github-blue
        :target: https://github.com/diffpy/fourigui/issues

Tool for visualizing 3D diffraction and PDF Images

Fourigui is an interactive visualization tool with an embedded Fourier transformation functionality, designed to
process 3D reciprocal space scattering volumes to 3D atomic pair distribution functions (3D PDFs).

Fourigui is a tool to visualize and process 3D data sets written with the python programming language. Fourigui always
displays one slice perpendicular to one axis and allows scrolling through the 3D data set along the given axis with a
slider. It shows feedback values such as global and local maxima, minima or NAN ratios. The matplotlib panel e.g. for
zooming and saving figures is featured. Fourigui is designed for the processing of 3D atomic pair distribution
functions (PDFs). One can load a 3D reciprocal space scattering volume which can be Fourier transformed to the 3D PDF.
Thereby, one can apply cut off frequencies beyond and below given Q values, compare the results and switch between the
scattering volume in reciprocal space and 3D PDF in real space.


For more information about the diffpy.fourigui library, please consult our `online documentation <https://diffpy.github.io/fourigui>`_.

Citation
--------
If you use diffpy.fourigui in a scientific publication, we would like you to cite this package as

        diffpy.fourigui Package, https://github.com/diffpy/fourigui

Installation
------------
The diffpy.fourigui package requires Python 3.10 or later and
the following software:

* ``matplotlib`` - graphing tool
* ``Scipy`` - scientific computing tool for python
* ``h5py`` - pythonic interface to the HDF5 binary data format

The preferred method is to use `Miniconda Python
<https://docs.conda.io/projects/miniconda/en/latest/miniconda-install.html>`_
and install from the "conda-forge" channel of Conda packages.

To add "conda-forge" to the conda channels, run the following in a terminal. ::

        conda config --add channels conda-forge

We want to install our packages in a suitable conda environment.
The following creates and activates a new environment named ``diffpy.fourigui_env`` ::

        conda create -n diffpy.fourigui_env python=3
        conda activate diffpy.fourigui_env

Then, to fully install ``diffpy.fourigui`` in our active environment, run ::

        conda install diffpy.fourigui

Another option is to use ``pip`` to download and install the latest release from
`Python Package Index <https://pypi.python.org>`_.
To install using ``pip`` into your ``diffpy.fourigui_env`` environment, we will also have to install dependencies ::

        pip install -r https://raw.githubusercontent.com/diffpy/fourigui/main/requirements/run.txt

and then install the package ::

        pip install diffpy.fourigui

If you prefer to install from sources, after installing the dependencies, obtain the source archive from
`GitHub <https://github.com/diffpy/fourigui/>`_. Once installed, ``cd`` into your ``fourigui`` directory
and run the following ::

        pip install .

Support and Contribute
----------------------
diffpy.fourigui is an open-source software developed as a part of the
DiffPy-CMI complex modeling initiative at the Brookhaven National
Laboratory.

`Diffpy user group <https://groups.google.com/g/diffpy-users>`_ is the discussion forum for general questions and discussions about the use of diffpy.fourigui. Please join the diffpy.fourigui users community by joining the Google group. The diffpy.fourigui project welcomes your expertise and enthusiasm!

If you see a bug or want to request a feature, please `report it as an issue <https://github.com/diffpy/fourigui/issues>`_ and/or `submit a fix as a PR <https://github.com/diffpy/fourigui/pulls>`_. You can also post it to the `Diffpy user group <https://groups.google.com/g/diffpy-users>`_. 

Feel free to fork the project and contribute. To install diffpy.fourigui
in a development mode, with its sources being directly used by Python
rather than copied to a package directory, use the following in the root
directory ::

        pip install -e .

To ensure code quality and to prevent accidental commits into the default branch, please set up the use of our pre-commit
hooks.

1. Install pre-commit in your working environment by running ``conda install pre-commit``.

2. Initialize pre-commit (one time only) ``pre-commit install``.

Thereafter your code will be linted by black and isort and checked against flake8 before you can commit.
If it fails by black or isort, just rerun and it should pass (black and isort will modify the files so should
pass after they are modified). If the flake8 test fails please see the error messages and fix them manually before
trying to commit again.

Improvements and fixes are always appreciated.

Before contribuing, please read our `Code of Conduct <https://github.com/diffpy/fourigui/blob/main/CODE_OF_CONDUCT.rst>`_.

Contact
-------

For more information on diffpy.fourigui please visit the project `web-page <https://diffpy.github.io/>`_ or email Prof. Simon Billinge at sb2896@columbia.edu.
