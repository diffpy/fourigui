import time
import tkinter as tk
from tkinter.ttk import Button

import h5py
import matplotlib
import numpy as np
from matplotlib import pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk

matplotlib.use("tk.TkAgg")

WIDTH = 920
HEIGHT = 630
XPOS = 300
YPOS = 100


class Gui(tk.Frame):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):

        self.loaded = False  # denotes whether a dataset is loaded
        self.transformed = False  # denotes whether dataset is Fourier transformed
        self.cutted = False  # denotes whether cutoff frequencies are applied to dataset
        self.transcutted = False  # denotes whether cutoff frequencies are applied and Fourier transformed

        self.master.title("FouriGUI")
        self.pack(fill=tk.BOTH, expand=True)

        print("\nNew Session started ...")
        print(
            "Enjoy exploring the beautiful reconstructions in real and in reciprocal space!"
        )

        # 4 frames:
        # frame 00: all buttons
        # frame 01: plot area
        # frame 10: exit button
        # frame 11: not used

        # 00 #
        # frame 00, upper left

        frame00 = tk.Frame(self)
        frame00.place(x=5, y=0)

        filelabel = tk.Label(frame00, text="filename: ")
        filelabel.grid(row=0, column=0)

        # row 0: load file area
        self.filename_entry = tk.Entry(frame00)
        self.filename_entry.grid(row=0, column=1, columnspan=3)
        self.filename_entry.insert(0, "/path/data.h5")

        loadbutton = Button(frame00, text="load", command=lambda: self.load_cube())
        loadbutton.grid(row=0, column=4)

        # row 1: change axis area
        axislabel = tk.Label(frame00, text="axis: ")
        axislabel.grid(row=1, column=0, pady=7, sticky=tk.W)

        self.axis = tk.IntVar()

        rb0 = tk.Radiobutton(
            frame00,
            text="0",
            variable=self.axis,
            value=0,
            command=lambda: self.plot_plane(),
        )
        rb0.grid(row=1, column=1)
        rb1 = tk.Radiobutton(
            frame00,
            text="1",
            variable=self.axis,
            value=1,
            command=lambda: self.plot_plane(),
        )
        rb1.grid(row=1, column=2)
        rb2 = tk.Radiobutton(
            frame00,
            text="2",
            variable=self.axis,
            value=2,
            command=lambda: self.plot_plane(),
        )
        rb2.grid(row=1, column=3)

        # row 2-4: intensity specs
        intlabel = tk.Label(frame00, text="intensity:")
        intlabel.grid(row=2, column=0, pady=1, sticky=tk.W)
        maxintlabel = tk.Label(frame00, text="max:")
        maxintlabel.grid(row=3, column=0, pady=1, sticky=tk.E)
        minintlabel = tk.Label(frame00, text="min:")
        minintlabel.grid(row=4, column=0, pady=1, sticky=tk.E)
        sumintlabel = tk.Label(frame00, text="sum:")
        sumintlabel.grid(row=5, column=0, pady=1, sticky=tk.E)
        nanratiolabel = tk.Label(frame00, text="nan ratio:")
        nanratiolabel.grid(row=6, column=0, pady=1, sticky=tk.E)
        globallabel = tk.Label(frame00, text="global", width=7)
        globallabel.grid(row=2, column=1)
        self.globalmax = tk.Label(frame00, text="")
        self.globalmax.grid(row=3, column=1)
        self.globalmin = tk.Label(frame00, text="")
        self.globalmin.grid(row=4, column=1)
        self.globalsum = tk.Label(frame00, text="")
        self.globalsum.grid(row=5, column=1)
        self.globalnanratio = tk.Label(frame00, text="")
        self.globalnanratio.grid(row=6, column=1)
        inplanelabel = tk.Label(frame00, text="in plane", width=7)
        inplanelabel.grid(row=2, column=2)
        self.localmax = tk.Label(frame00, text="")
        self.localmax.grid(row=3, column=2)
        self.localmin = tk.Label(frame00, text="")
        self.localmin.grid(row=4, column=2)
        self.localsum = tk.Label(frame00, text="")
        self.localsum.grid(row=5, column=2)
        self.localnanratio = tk.Label(frame00, text="")
        self.localnanratio.grid(row=6, column=2)
        colorbarlabel = tk.Label(frame00, text="colorbar")
        colorbarlabel.grid(row=2, column=3)
        self.colorbarmax = tk.Entry(frame00, width=7)
        self.colorbarmax.grid(row=3, column=3)
        self.colorbarmin = tk.Entry(frame00, width=7)
        self.colorbarmin.grid(row=4, column=3)
        set_range = Button(
            frame00, text="set range", command=lambda: self.colorrange_upd()
        )
        set_range.grid(row=2, column=4)
        toglobalmax = Button(
            frame00,
            text="global max",
            command=lambda: self.multiple_funcs(
                self.colorbarmax.delete(0, len(self.colorbarmax.get())),
                self.colorbarmax.insert(0, self.globalmax["text"]),
            ),
        )
        toglobalmax.grid(row=3, column=4)
        toglobalmin = Button(
            frame00,
            text="global min",
            command=lambda: self.multiple_funcs(
                self.colorbarmin.delete(0, len(self.colorbarmin.get())),
                self.colorbarmin.insert(0, self.globalmin["text"]),
            ),
        )
        toglobalmin.grid(row=4, column=4)

        # row 7-8: animation - automatic slicing through the planes
        anilabel = tk.Label(frame00, text="animation speed [ms]")
        anilabel.grid(row=7, column=3, columnspan=2, sticky=tk.W)
        self.anientry = tk.Entry(frame00, width=7)
        self.anientry.grid(row=8, column=3)
        anibutton = Button(frame00, text="animation", command=lambda: self.animation())
        anibutton.grid(row=8, column=4)

        # row 10-12 Fourier transformation
        seperator = tk.Label(
            frame00, text=" "
        )  # __________________________________________________________________")
        seperator.grid(row=9, column=0, columnspan=5)
        cutofflabel = tk.Label(frame00, text="cutoff frequency")
        cutofflabel.grid(row=10, column=2, columnspan=2)
        qminlabel = tk.Label(frame00, text="qmin [px]:")
        qminlabel.grid(row=11, column=2, sticky=tk.E)
        qmaxlabel = tk.Label(frame00, text="qmax [px]:")
        qmaxlabel.grid(row=12, column=2, sticky=tk.E)
        self.qminentry = tk.Entry(frame00, width=7)
        self.qminentry.grid(row=11, column=3)
        self.qmaxentry = tk.Entry(frame00, width=7)
        self.qmaxentry.grid(row=12, column=3)
        self.cutoff = tk.IntVar()
        newcutoffbutton = Button(
            frame00, text="new cutoff", command=lambda: self.newcutoff()
        )
        newcutoffbutton.grid(row=10, column=4)
        cutoffon = tk.Radiobutton(
            frame00,
            text="on",
            variable=self.cutoff,
            value=1,
            command=lambda: self.applycutoff(),
        )
        cutoffon.grid(row=11, column=4, sticky=tk.W)
        cutoffoff = tk.Radiobutton(
            frame00,
            text="off",
            variable=self.cutoff,
            value=0,
            command=lambda: self.redocutuff(),
        )
        cutoffoff.grid(row=12, column=4, sticky=tk.W)

        spacelabel = tk.Label(frame00, text="Space Selection")
        spacelabel.grid(row=10, column=0, columnspan=2, sticky=tk.W)
        self.space = tk.IntVar()
        reciprocal = tk.Radiobutton(
            frame00,
            text="reciprocal space",
            variable=self.space,
            value=0,
            command=lambda: self.ifft(),
            pady=5,
        )
        reciprocal.grid(row=11, column=0, columnspan=2, sticky=tk.W)
        fft = tk.Radiobutton(
            frame00,
            text="real space",
            variable=self.space,
            value=1,
            command=lambda: self.fft(),
        )
        fft.grid(row=12, column=0, columnspan=2, sticky=tk.W)

        # 01 #
        # frame 01, upper right
        self.frame01 = tk.Frame(self, bg="#cccccc")
        self.frame01.place(x=400, y=0)  # , height=HEIGHT//2, width=WIDTH//2)

        self.plane_num = tk.IntVar()

        self.slider = tk.Scale(
            self.frame01,
            variable=self.plane_num,
            from_=0,
            to=500,
            label="slider",
            orient=tk.HORIZONTAL,
            length=WIDTH // 2,  # resolution=-1,
            command=lambda x: self.multiple_funcs(
                self.plot_plane(), self.intensity_upd_local()
            ),
        )
        # command=lambda p: self.plot_plane())
        self.slider.grid(
            row=0, column=0, padx=10, pady=10, sticky=tk.N + tk.E + tk.S + tk.W
        )

        self.frame01_plotcell = tk.Frame(self.frame01)
        self.frame01_plotcell.grid(
            row=1, column=0, padx=10, pady=10, sticky=tk.N + tk.E + tk.S + tk.W
        )

        self.frame01_toolbar = tk.Frame(self.frame01)
        self.frame01_toolbar.grid(row=2, column=0)

        # 10 #
        # frame 10, lower left
        frame10 = tk.Frame(self)
        frame10.place(x=5, y=HEIGHT - 30)  # , height=HEIGHT//2, width=WIDTH//2)
        quit = Button(
            frame10,
            text="exit",
            command=lambda: self.multiple_funcs(
                print("Session ended...\n", self.quit())
            ),
        )
        quit.pack(side=tk.TOP)

        # 11 #
        # frame 00, lower right
        # no functionality
        frame11 = tk.Frame(self)
        frame11.place(
            x=WIDTH // 2, y=HEIGHT // 2
        )  # , height=HEIGHT//2, width=WIDTH//2)

    def load_cube(self):
        """
        loads 3D array in h5py file format from the filename input panel
        3D array is expected to be a reconstructed reciprocal scattering volume
        when executed, one slide perpendicular to the selected axis will be plotted in the plot panel
        """

        filename = self.filename_entry.get()
        f = h5py.File(filename, "r")
        try:
            if "data" in f.keys():
                self.cube = np.array(f["data"])
            elif "rebinned_data" in f.keys():
                self.cube = np.array(f["rebinned_data"])
        except Exception:
            raise KeyError(
                "- No data found in "
                + filename
                + " :( ..."
                + "\nchange to alternative keys: "
                + str(list(f.keys()))
            )
        print("- file loaded: {}".format(filename))

        self.slider.destroy()
        self.slider = tk.Scale(
            self.frame01,
            variable=self.plane_num,
            from_=0,
            to=len(self.cube) - 1,
            label="slider",
            orient=tk.HORIZONTAL,
            length=WIDTH // 2,  # resolution=-1,
            command=lambda x: self.multiple_funcs(
                self.plot_plane(), self.intensity_upd_local()
            ),
        )
        self.slider.grid(
            row=0, column=0, padx=10, pady=10, sticky=tk.N + tk.E + tk.S + tk.W
        )

        if not self.loaded:

            fig, ax = plt.subplots(figsize=(4.95, 4.95))
            fig = plt.gcf()
            DPI = fig.get_dpi()
            fig.set_size_inches(500 / float(DPI), 500 / float(DPI))

            self.plane_num.set(np.shape(self.cube)[0] // 2)

            if self.axis.get() == 0:
                self.im = plt.imshow(self.cube[self.plane_num.get(), :, :])
            elif self.axis.get() == 1:
                self.im = plt.imshow(self.cube[:, self.plane_num.get(), :])
            elif self.axis.get() == 2:
                self.im = plt.imshow(self.cube[:, :, self.plane_num.get()])
            else:
                raise ValueError("axis must be 0,1,2")
            plt.colorbar(shrink=0.81)
            ax.set_xlabel("pixel")
            ax.set_ylabel("pixel")
            self.canvas = FigureCanvasTkAgg(fig, master=self.frame01_plotcell)
            self.toolbar = NavigationToolbar2Tk(self.canvas, self.frame01_toolbar)
            self.toolbar.pack(side=tk.LEFT)
            # self.toolbar.children['!button6'].pack_forget()
            # self.toolbar.children['!button7'].pack_forget()
            self.toolbar.update()
            self.canvas.draw()
            self.canvas.get_tk_widget().pack(side=tk.LEFT, fill=tk.BOTH, expand=1)
            self.loaded = True

        else:
            self.plot_plane()
            self.transformed = False
            self.transcutted = False
            self.cutted = False
            self.cutoff.set(0)
            self.space.set(0)

        self.intensity_upd_global()

    def plot_plane(self):
        """update plotted plane perpendicular to the selected axis"""
        if self.axis.get() == 0:
            self.im.set_data(self.cube[self.plane_num.get(), :, :])
        elif self.axis.get() == 1:
            self.im.set_data(self.cube[:, self.plane_num.get(), :])
        elif self.axis.get() == 2:
            self.im.set_data(self.cube[:, :, self.plane_num.get()])
        else:
            raise ValueError("axis must be 0,1,2")
        self.canvas.draw()

    def colorrange_upd(self):
        """change color range in plot"""
        try:
            if self.colorbarmin.get() and self.colorbarmax.get():
                vmin = float(self.colorbarmin.get())
                vmax = float(self.colorbarmax.get())
            elif self.colorbarmin.get():
                vmin = float(self.colorbarmin.get())
                vmax = self.globalmax["text"]
            elif self.colorbarmax.get():
                vmin = self.globalmin["text"]
                vmax = float(self.colorbarmax.get())
            else:
                vmin = self.globalmin["text"]
                vmax = self.globalmax["text"]
        except ValueError:
            print("Oops... colorbar range must be a number or empty string.")
        self.im.set_clim(vmin, vmax)
        self.plot_plane()

    def intensity_upd_local(self):
        """show local intensity minimum, maximum and sum of current plotted plane"""
        if self.axis.get() == 0:
            plane = self.cube[self.plane_num.get(), :, :]
        elif self.axis.get() == 1:
            plane = self.cube[:, self.plane_num.get(), :]
        elif self.axis.get() == 2:
            plane = self.cube[:, :, self.plane_num.get()]
        nan_ratio = np.count_nonzero(np.isnan(plane)) / plane.size
        self.localmax["text"] = "{}".format(
            np.format_float_scientific(np.nanmax(plane), 1)
        )
        self.localmin["text"] = "{}".format(
            np.format_float_scientific(np.nanmin(plane), 1)
        )
        self.localsum["text"] = "{}".format(
            np.format_float_scientific(np.nansum(plane), 1)
        )
        self.localnanratio["text"] = "{}".format(round(nan_ratio, 2))

    def intensity_upd_global(self):
        """show global intensity minimum, maximum and sum of 3D array"""
        self.intensity_upd_local()
        nan_ratio = np.count_nonzero(np.isnan(self.cube)) / self.cube.size
        self.globalmax["text"] = "{}".format(
            np.format_float_scientific(np.nanmax(self.cube), 1)
        )
        self.globalmin["text"] = "{}".format(
            np.format_float_scientific(np.nanmin(self.cube), 1)
        )
        self.globalsum["text"] = "{}".format(
            np.format_float_scientific(np.nansum(self.cube), 1)
        )
        self.globalnanratio["text"] = "{}".format(round(nan_ratio, 2))

    def fft(self):
        """
        Fourier transform 3D array from reciprocal to real space
        the origin of reciprocal and real space is expected to be the central voxel
        """

        def perform_fft(fftholder):
            time0 = time.time()
            fftholder = np.nan_to_num(fftholder)
            size = list(fftholder.shape)
            fftholder = np.fft.ifftshift(fftholder)
            fftholder = np.fft.fftn(fftholder, s=size, norm="ortho")
            fftholder = np.fft.fftshift(fftholder)
            fftholder = fftholder.real
            fftdur = time.time() - time0
            print("- FFT performed in {} sec.".format(round(fftdur, 4)))
            return fftholder

        if not self.transformed and not self.transcutted:  # no fft at all yet
            if not self.cutoff.get():
                self.cube_reci = self.cube
                self.cube = perform_fft(self.cube)
                self.cube_real = self.cube
                self.transformed = True
            else:
                self.cube_recicut = self.cube
                self.cube = perform_fft(self.cube)
                self.cube_realcut = self.cube
                self.transcutted = True

        elif not self.transformed and self.transcutted:
            if not self.cutoff.get():
                self.cube = perform_fft(self.cube_reci)
                self.cube_real = self.cube
                self.transformed = True
            else:
                self.cube = self.cube_realcut

        elif self.transformed and not self.transcutted:
            if not self.cutoff.get():
                self.cube_reci = self.cube
                self.cube = self.cube_real
            else:
                self.cube = perform_fft(self.cube_recicut)
                # self.cube = self.cube_realcut
                self.transcutted = True

        else:
            if not self.cutoff.get():
                self.cube = self.cube_real
            else:
                self.cube = self.cube_realcut

        print("- Switching to real space")

        self.plot_plane()
        self.intensity_upd_global()

    def ifft(self):
        """
        Inverse Fourier transform 3D array from real to reciprocal space
        the origin of real and reciprocal space is expected to be the central voxel
        """
        if not self.cutoff.get():
            self.cube_real = self.cube
            self.cube = self.cube_reci
        else:
            self.cube_realcut = self.cube
            self.cube = self.cube_recicut

        print("- Switching to reciprocal space")

        self.plot_plane()
        self.intensity_upd_global()

    def applycutoff(self):
        """
        reassign all voxels with distance smaller than qmin and greater than qmax
        from the central voxel to 0.0
        qmin, qmax is loaded from the qmin, qmax input panel
        currently opperates in units of pixels
        """
        if not self.cutted:

            time0 = time.time()
            X, Y, Z = self.cube.shape
            sphere = np.ones((X, Y, Z))
            qmin = float(self.qminentry.get())
            qmax = float(self.qmaxentry.get())
            # convert qmin to pixels
            # convert qmax to pixels
            r2_inner = qmin**2
            r2_outer = qmax**2
            XS, YS, ZS = np.meshgrid(np.arange(X), np.arange(Y), np.arange(Z))
            R2 = (XS - X // 2) ** 2 + (YS - Y // 2) ** 2 + (ZS - Z // 2) ** 2
            mask = (R2 <= r2_inner) | (R2 >= r2_outer)
            sphere[mask] = np.nan
            cutdur = time.time() - time0

            if self.space.get():
                self.cube_real = self.cube
                self.cube = self.cube_reci * sphere
                self.cube_recicut = self.cube
                print(
                    "- Cutoff below {} and beyond {} in {} sec.".format(
                        qmin, qmax, round(cutdur, 4)
                    )
                )
                self.fft()
            else:
                self.cube_reci = self.cube
                self.cube = self.cube * sphere
                self.cube_recicut = self.cube
                self.plot_plane()
                self.intensity_upd_global()
                print(
                    "- Cutoff below {} and beyond {} in {} sec.".format(
                        qmin, qmax, round(cutdur, 4)
                    )
                )

            self.cutted = True

        else:
            if self.space.get():  # in real space
                self.cube = self.cube_realcut
            else:
                self.cube = self.cube_recicut
            self.plot_plane()
            self.intensity_upd_global()

    def redocutuff(self):
        if self.space.get():  # in real space
            self.cube_realcut = self.cube
            if not self.transformed:
                self.fft()
            self.cube = self.cube_real
        else:
            self.cube_recicut = self.cube
            self.cube = self.cube_reci
        self.plot_plane()
        self.intensity_upd_global()

    def newcutoff(self):
        if self.cutoff.get():
            if self.space.get() and self.transformed:
                self.cube = self.cube_real
            else:
                self.cube = self.cube_reci
        self.cutted = False
        self.transcutted = False
        self.applycutoff()

    def plot_next_plane(self):
        n = self.plane_num.get()
        if n == len(self.cube[self.axis.get()]) - 1:
            n = 0
        else:
            n += 1
        self.plane_num.set(n)
        self.plot_plane()

    def animation(self):
        """
        slices through the 3D array along the selcted axis
        """
        try:
            if not self.anientry.get():
                anispeed = 1
            else:
                anispeed = self.anientry.get()
        except ValueError:
            print("Oops... animation speed must be an integer > 0 or empty string.")
        n = self.plane_num.get() - 1
        while n is not self.plane_num.get():
            self.slider.after(anispeed, self.plot_next_plane())
        self.plot_next_plane()

    def multiple_funcs(*funcs):
        for func in funcs:
            func


def main():
    root = tk.Tk()
    root.geometry("{}x{}+{}+{}".format(WIDTH, HEIGHT, XPOS, YPOS))
    Gui()
    root.mainloop()


if __name__ == "__main__":
    main()
