========
diffpy.fourigui
========

.. image:: https://img.shields.io/travis/sbillinge/fourigui.svg
        :target: https://travis-ci.org/sbillinge/fourigui

.. image:: https://img.shields.io/pypi/v/fourigui.svg
        :target: https://pypi.python.org/pypi/fourigui


* Free software: 3-clause BSD license
* Documentation: (COMING SOON!) https://sbillinge.github.io/fourigui.

========================================================================
#TODO insert desciptions
{{Fourigui is an interactive visualization tool with an embedded Fourier transformation functionality, designed to process 3D reciprocal space scattering volumes to 3D atomic pair distribution functions (3D PDFs).}}

{{Fourigui is a tool to visualize and process 3D data sets written with the python programming language. Fourigui always displays one slice perpendicular to one axis and allows scrolling through the 3D data set along the given axis with a slider. It shows feedback values such as global and local maxima, minima or NAN ratios. The matplotlib panel e.g. for zooming and saving figures is featured.
Fourigui is designed for the processing of 3D atomic pair distribution functions (PDFs). One can load a 3D reciprocal space scattering volume which can be Fourier transformed to the 3D PDF. Thereby, one can apply cut off frequencies beyond and below given Q values, compare the results and switch between the scattering volume in reciprocal space and 3D PDF in real space.
}}
#TODO add docs to website?
To learn more about diffpy.{{cookiecutter.package_name}} library see the
user manual at http://diffpy.github.io/diffpy.{{cookiecutter.package_name}}.

REQUIREMENTS
------------------------------------------------------------------------

The diffpy.fourigui package requires Python 3.5 or later or 2.7 and
the following software:

* ``matplotlib`` - graphing tool
* ``Scipy`` - scientific computing tool for python
* ``h5py`` - pythonic interface to the HDF5 binary data format


We recommend to use `Anaconda Python <https://www.anaconda.com/download>`_
as it allows to install all software dependencies together with
diffpy.fourigui.  For other Python distributions it is necessary to
install the required software separately.  As an example on Ubuntu
Linux the required software can be installed with ::

   sudo get-apt install python3-matplotlib python3-Scipy python3-h5py


INSTALLATION
------------------------------------------------------------------------

The preferred method is to use Anaconda Python and install from the
"conda-forge" channel of Anaconda packages ::

   conda config --add channels conda-forge
   conda install diffpy.fourigui

Another installation option is to use ``easy_install`` to download and
install the latest release from
`Python Package Index <https://pypi.python.org>`_ ::

   pip install diffpy.fourigui

If you prefer to install from sources, navigate to the source archive
directory and run ::

   python setup.py install

You may need to use ``sudo`` with system Python so it is allowed to
copy files to system directories.  If sudo is not available, check
the usage info from ``python setup.py install --help`` for options to
install to user-writable locations.  


DEVELOPMENT
------------------------------------------------------------------------

diffpy.fourigui is an open-source software developed as a part of the
DiffPy-CMI complex modeling initiative at the Brookhaven National
Laboratory.  The diffpy.{{cookiecutter.package_name}} sources are hosted at
https://github.com/diffpy/diffpy.fourigui.

Feel free to fork the project and contribute.  To install diffpy.structure
in a development mode, where the sources are directly used by Python
rather than copied to a system directory, use ::

   python setup.py develop --user


ACKNOWLEDGEMENT
------------------------------------------------------------------------

{{cookiecutter.acknowledgements}}


CONTACTS
------------------------------------------------------------------------

For more information on diffpy.structure please visit the project web-page

http://www.diffpy.org/

or email Prof. Simon Billinge at sb2896@columbia.edu.

