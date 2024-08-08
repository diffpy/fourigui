import unittest

import h5py
import numpy as np

from src.diffpy.fourigui.fourigui import Gui


class TestGui(unittest.TestCase):
    def setUp(self):
        # set up gui
        self.test_gui = Gui()

        # set up test data
        self.test_sofq = h5py.File("diffpy/tests/testdata/sofq.h5")["data"]
        self.test_sofq_cut_10to40px = h5py.File(
            "diffpy/tests/testdata/sofq_cut_10to40px.h5"
        )["data"]
        self.test_sofq_cut_15to35px = h5py.File(
            "diffpy/tests/testdata/sofq_cut_15to35px.h5"
        )["data"]
        self.test_gofr = h5py.File("diffpy/tests/testdata/gofr.h5")["data"]
        self.test_gofr_cut_10to40px = h5py.File(
            "diffpy/tests/testdata/gofr_from_sofq_cut_10to40px.h5"
        )["data"]
        self.test_gofr_cut_15to35px = h5py.File(
            "diffpy/tests/testdata/gofr_from_sofq_cut_15to35px.h5"
        )["data"]

    def test_load_cube_testdataset1(self):
        # given
        self.test_gui.filename_entry.delete(0, "end")
        self.test_gui.filename_entry.insert(0, "diffpy/tests/testdata/sofq.h5")

        # when
        self.test_gui.load_cube()
        result = self.test_gui.cube

        # then
        self.assertTrue(np.allclose(result, self.test_sofq))

    def test_load_cube_testdataset2(self):
        # given
        self.test_gui.filename_entry.delete(0, "end")
        self.test_gui.filename_entry.insert(
            0, "diffpy/tests/testdata/sofq_cut_10to40px.h5"
        )

        # when
        self.test_gui.load_cube()
        result = self.test_gui.cube

        # then
        self.assertTrue(
            np.allclose(
                np.nan_to_num(result), np.nan_to_num(self.test_sofq_cut_10to40px)
            )
        )

    def test_load_cube_testdataset3(self):
        # given
        self.test_gui.filename_entry.delete(0, "end")
        self.test_gui.filename_entry.insert(
            0, "diffpy/tests/testdata/sofq_cut_15to35px.h5"
        )

        # when
        self.test_gui.load_cube()
        result = self.test_gui.cube

        # then
        self.assertTrue(
            np.allclose(
                np.nan_to_num(result), np.nan_to_num(self.test_sofq_cut_15to35px)
            )
        )

    def test_fft_testdataset1(self):
        # given
        self.test_gui.plot_plane = (
            lambda *a, **b: ()
        )  # overwrite plot_plane which requires not initialized attribute im
        self.test_gui.cube = self.test_sofq

        # when
        self.test_gui.fft()
        result = self.test_gui.cube

        # then
        self.assertTrue(np.allclose(result, self.test_gofr))

    def test_fft_testdataset2(self):
        # given
        self.test_gui.plot_plane = (
            lambda *a, **b: ()
        )  # overwrite plot_plane which requires not initialized attribute im
        self.test_gui.cube = self.test_sofq_cut_10to40px

        # when
        self.test_gui.fft()
        result = self.test_gui.cube

        # then
        self.assertTrue(np.allclose(result, self.test_gofr_cut_10to40px))

    def test_fft_testdataset3(self):
        # given
        self.test_gui.plot_plane = (
            lambda *a, **b: ()
        )  # overwrite plot_plane which requires not initialized attribute im
        self.test_gui.cube = self.test_sofq_cut_15to35px

        # when
        self.test_gui.fft()
        result = self.test_gui.cube

        # then
        self.assertTrue(np.allclose(result, self.test_gofr_cut_15to35px))

    def test_applycutoff_range1(self):
        # given
        self.test_gui.plot_plane = lambda *a, **b: ()
        self.test_gui.cube = self.test_sofq
        self.test_gui.qminentry.insert(0, "10")
        self.test_gui.qmaxentry.insert(0, "40")

        # when
        self.test_gui.applycutoff()
        result = self.test_gui.cube

        # then
        self.assertTrue(
            np.allclose(
                np.nan_to_num(result), np.nan_to_num(self.test_sofq_cut_10to40px)
            )
        )

    def test_applycutoff_range2(self):
        # given
        self.test_gui.plot_plane = lambda *a, **b: ()
        self.test_gui.cube = self.test_sofq
        self.test_gui.qminentry.insert(0, "15")
        self.test_gui.qmaxentry.insert(0, "35")

        # when
        self.test_gui.applycutoff()
        result = self.test_gui.cube

        # then
        self.assertTrue(
            np.allclose(
                np.nan_to_num(result), np.nan_to_num(self.test_sofq_cut_15to35px)
            )
        )


if __name__ == "__main__":
    unittest.main()
