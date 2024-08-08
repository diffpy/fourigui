import unittest

import h5py

from ..fourigui.fourigui import Gui


class TestGui(unittest.TestCase):
    def setUp(self):
        # set up gui
        self.test_gui = Gui()

        # set up dummy data
        self.dummydata = h5py.File("diffpy/tests/testdata/dummydata.h5")["data"]

    def test_init(self):
        self.assertFalse(self.test_gui.loaded)
        self.assertFalse(self.test_gui.transformed)
        self.assertFalse(self.test_gui.cutted)
        self.assertFalse(self.test_gui.transcutted)
        self.assertFalse(self.test_gui.cutoff.get())
        self.assertFalse(self.test_gui.space.get())

    def test_load_cube_nothing_loaded(self):
        # given
        self.test_gui.filename_entry.delete(0, "end")
        self.test_gui.filename_entry.insert(0, "diffpy/tests/testdata/dummydata.h5")

        # when
        self.test_gui.load_cube()

        # then
        self.assertTrue(self.test_gui.loaded)

    def test_load_cube_something_loaded(self):
        # given
        self.test_gui.loaded
        self.test_gui.filename_entry.delete(0, "end")
        self.test_gui.filename_entry.insert(0, "diffpy/tests/testdata/dummydata.h5")

        # when
        self.test_gui.load_cube()

        # then
        self.assertTrue(self.test_gui.loaded)

    def test_fft_000(self):
        # given
        self.test_gui.cube = self.dummydata
        self.test_gui.plot_plane = (
            lambda *a, **b: ()
        )  # overwrite plot_plane which requires not initialized attribute im
        self.test_gui.transformed = False
        self.test_gui.transcutted = False
        self.test_gui.cutoff.set(0)

        # when
        self.test_gui.fft()

        # then
        self.assertTrue(self.test_gui.transformed and not self.test_gui.transcutted)

    def test_fft_010(self):
        # given
        self.test_gui.cube = self.dummydata
        self.test_gui.plot_plane = (
            lambda *a, **b: ()
        )  # overwrite plot_plane which requires not initialized attribute im
        self.test_gui.transformed = False
        self.test_gui.transcutted = False
        self.test_gui.cutoff.set(1)

        # when
        self.test_gui.fft()

        # then
        self.assertTrue(not self.test_gui.transformed and self.test_gui.transcutted)
        # self.assertTrue(self.test_gui.cutted)

    def test_fft_001(self):
        # given
        self.test_gui.cube = self.dummydata
        self.test_gui.cube_reci = self.dummydata
        self.test_gui.plot_plane = (
            lambda *a, **b: ()
        )  # overwrite plot_plane which requires not initialized attribute im
        self.test_gui.transformed = False
        self.test_gui.transcutted = True
        self.test_gui.cutoff.set(0)

        # when
        self.test_gui.fft()

        # then
        self.assertTrue(self.test_gui.transformed and self.test_gui.transcutted)

    def test_fft_011(self):
        # given
        self.test_gui.cube = self.dummydata
        self.test_gui.cube_realcut = self.dummydata
        self.test_gui.plot_plane = (
            lambda *a, **b: ()
        )  # overwrite plot_plane which requires not initialized attribute im
        self.test_gui.transformed = False
        self.test_gui.transcutted = True
        self.test_gui.cutoff.set(1)

        # when
        self.test_gui.fft()

        # then
        self.assertTrue(not self.test_gui.transformed and self.test_gui.transcutted)

    def test_fft_101(self):
        # given
        self.test_gui.cube = self.dummydata
        self.test_gui.cube_real = self.dummydata
        self.test_gui.plot_plane = (
            lambda *a, **b: ()
        )  # overwrite plot_plane which requires not initialized attribute im
        self.test_gui.transformed = True
        self.test_gui.transcutted = True
        self.test_gui.cutoff.set(0)

        # when
        self.test_gui.fft()

        # then
        self.assertTrue(self.test_gui.transformed and self.test_gui.transcutted)

    def test_fft_111(self):
        # given
        self.test_gui.cube = self.dummydata
        self.test_gui.cube_realcut = self.dummydata
        self.test_gui.plot_plane = (
            lambda *a, **b: ()
        )  # overwrite plot_plane which requires not initialized attribute im
        self.test_gui.transformed = True
        self.test_gui.transcutted = True
        self.test_gui.cutoff.set(1)

        # when
        self.test_gui.fft()

        # then
        self.assertTrue(self.test_gui.transformed and self.test_gui.transcutted)


if __name__ == "__main__":
    unittest.main()
