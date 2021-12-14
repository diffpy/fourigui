import unittest
import numpy as np
import h5py
# from diffpy.fourigui import Gui
###
# temporary workaround since "from diffpy.fourigui import Gui" doesn't work yet
import sys, os, inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)
from fourigui import Gui
###

class Test_Gui_load_cube(unittest.TestCase):

    def test_load_cube(self):
        g = Gui()
        g.filename_entry.delete(0, 'end')
        g.filename_entry.insert(0, 'testdata/sofq.h5')
        g.load_cube()
        data = h5py.File('testdata/sofq.h5', 'r')['data']
        self.assertTrue(np.allclose(g.cube, data))

class Test_Gui_fft(unittest.TestCase):

    def test_fft(self):
        g = Gui()
        g.plot_plane = lambda *a, **b: () # overwrite plot_plane which requires not initialized attribute im
        g.cube = h5py.File('testdata/sofq.h5', 'r')['data']
        g.fft()
        data = h5py.File('testdata/gofr.h5', 'r')['data']
        self.assertTrue(np.allclose(g.cube, data))

class Test_Gui_cutoff(unittest.TestCase):

    def test_applycutoff_range1(self):
        g = Gui()
        g.plot_plane = lambda *a, **b: ()
        g.cube = h5py.File('testdata/sofq.h5', 'r')['data']
        g.qminentry.insert(0, '10')
        g.qmaxentry.insert(0, '40')
        g.applycutoff()
        data = h5py.File('testdata/sofq_cut_10to40px.h5', 'r')['data']
        self.assertTrue(np.allclose(np.nan_to_num(g.cube), np.nan_to_num(data)))

    def test_applycutoff_range2(self):
        g = Gui()
        g.plot_plane = lambda *a, **b: ()
        g.cube = h5py.File('testdata/sofq.h5', 'r')['data']
        g.qminentry.insert(0, '15')
        g.qmaxentry.insert(0, '35')
        g.applycutoff()
        data = h5py.File('testdata/sofq_cut_15to35px.h5', 'r')['data']
        self.assertTrue(np.allclose(np.nan_to_num(g.cube), np.nan_to_num(data)))

if __name__ == '__main__':
    unittest.main()

