import unittest
import numpy as np
import h5py
# from diffpy.fourigui import Gui
import sys, os, inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)
from fourigui import Gui

class Test_Gui_load_cube(unittest.TestCase):

    def test_load_cube(self):
        g = Gui()
        g.filename_entry.insert(0, 'testdata/sofq.h5')
        g.load_cube()
        data = h5py.File('testdata/sofq.h5', 'r')['data']
        self.assertTrue(np.allclose(g.cube, data))

class Test_Gui_fft(unittest.TestCase):

    def test_fft(self):
        g = Gui()
        g.plot_plane = lambda *a, **b: ()
        g.cube = h5py.File('testdata/sofq.h5', 'r')['data']
        g.fft()
        data = h5py.File('testdata/gofr.h5', 'r')['data']
        self.assertTrue(np.allclose(g.cube, data))

# class Test_Gui_cutoff(unittest.TestCase):
#
#     def test_applycutoff(self):
#         # g = Gui()
#         # g.plot_plane = lambda *a, **b: ()
#         # g.cube = h5py.File('testdata/sofq.h5', 'r')['data']
#         # g.qminentry.insert(0, '10')
#         # g.qmaxentry.insert(0, '90')
#         # g.applycutoff()
#         data1 = h5py.File('testdata/sofq_cut.h5', 'r')['data']
#         data2 = h5py.File('/Users/admin/Desktop/sofq_cut.h5', 'r')['data']
#         # f = h5py.File('/Users/admin/Desktop/sofq_cut.h5', 'w')
#         # f['data'] = g.cube
#         # f.close()
#         # self.assertTrue(np.allclose(g.cube, data))
#         self.assertTrue(np.allclose(data1, data2))

if __name__ == '__main__':
    unittest.main()

