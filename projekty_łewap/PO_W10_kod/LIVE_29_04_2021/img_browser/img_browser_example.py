import sys
from os import walk, path

import numpy as np
from PIL import Image, ImageOps
from PIL.ImageQt import ImageQt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QFileDialog, QHBoxLayout, QGroupBox, QVBoxLayout, \
    QGridLayout, QLabel
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure


class MplHistCanvas(FigureCanvasQTAgg):
    def __init__(self, width=4, height=4, dpi=100):
        self.__fig = Figure(figsize=(width, height), dpi=dpi)
        super().__init__(self.__fig)

        self.__axes = None

    def plot_img_hist(self, gray_img, title, bins=256):
        if self.__axes is None:
            self.__axes = self.__fig.add_subplot(111)

        img_hist = np.asarray(gray_img).ravel()
        self.__axes.clear()
        self.__axes.hist(img_hist, bins=bins)
        self.__axes.set_title(title)
        self.draw()


class ImagesDirBrowser:

    def __init__(self, path_to_dir, accepted_formats):
        self.__path_to_dir = path_to_dir
        self.__accepted_formats = accepted_formats
        self.__img_files = self.__get_list_of_images()
        self.__current_id = self.__init_current_id()

    def __get_list_of_images(self):
        images = []
        _, _, filenames = next(walk(self.__path_to_dir), (None, None, []))
        for filename in filenames:
            file_extension = path.splitext(filename)[1].lower()

            if file_extension in self.__accepted_formats:
                full_path = path.join(self.__path_to_dir, filename)
                images.append(full_path)

        return images

    def __init_current_id(self):
        n = len(self.__img_files)
        return 0 if n > 0 else None

    def get_current(self):
        if self.__current_id is not None:
            return self.__img_files[self.__current_id]
        else:
            raise IndexError("The image list has no  images!")

    def get_next(self):
        if self.has_next():
            self.__current_id += 1
            return self.__img_files[self.__current_id]
        else:
            raise IndexError("The image list has no more (NEXT) images!")

    def has_next(self):
        n = len(self.__img_files)
        return self.__current_id is not None and self.__current_id < n - 1

    def get_prev(self):
        if self.has_prev():
            self.__current_id -= 1
            return self.__img_files[self.__current_id]
        else:
            raise IndexError("The image list has no more (PREVIOUS) images!")

    def has_prev(self):
        return self.__current_id is not None and self.__current_id > 0


class ImgBrowser(QWidget):

    def __init__(self, accepted_format):
        super().__init__()
        self.__accepted_format = accepted_format

        self.__init_window()
        self.__prepare_buttons()
        self.__prepare_images()
        self.__set_main_layout()
        self.__img_dir_browser: ImagesDirBrowser = None
        self.__img_max_height = 250  # fixme

    def __init_window(self):
        width, height = 800, 600
        self.setWindowTitle("Image browser")
        self.setFixedSize(width, height)
        self.show()

    def __prepare_buttons(self):
        self.__btn_prev = self.__create_prev_button()
        self.__btn_next = self.__create_next_button()
        self.__btn_dir_select = self.__create_dir_select_button()

    def __create_prev_button(self):
        btn_prev = QPushButton("Prev")
        btn_prev.setEnabled(False)
        btn_prev.clicked.connect(self.__handle_prev)
        return btn_prev

    def __handle_prev(self):
        if self.__img_dir_browser.has_prev():
            path_to_img = self.__img_dir_browser.get_prev()
            self.__update_window(path_to_img)
            self.__update_prev_and_next()

    def __create_next_button(self):
        btn_next = QPushButton("Next")
        btn_next.setEnabled(False)
        btn_next.clicked.connect(self.__handle_next)
        return btn_next

    def __handle_next(self):
        if self.__img_dir_browser.has_next():
            path_to_img = self.__img_dir_browser.get_next()
            self.__update_window(path_to_img)
            self.__update_prev_and_next()

    def __create_dir_select_button(self):
        btn_dir_select = QPushButton("Select")
        btn_dir_select.clicked.connect(self.__handle_select_dir)
        return btn_dir_select

    def __handle_select_dir(self):
        dir_path = QFileDialog.getExistingDirectory(self, "Select imgs dir")

        if dir_path:
            self.__img_dir_browser = ImagesDirBrowser(dir_path, self.__accepted_format)
            self.__update_prev_and_next()
            if self.__img_dir_browser.has_next():
                path_to_img = self.__img_dir_browser.get_current()
                self.__update_window(path_to_img)

    def __update_prev_and_next(self):
        if self.__img_dir_browser.has_prev():
            self.__btn_prev.setEnabled(True)
        else:
            self.__btn_prev.setEnabled(False)

        if self.__img_dir_browser.has_next():
            self.__btn_next.setEnabled(True)
        else:
            self.__btn_next.setEnabled(False)

    def __set_main_layout(self):
        main_layout = QVBoxLayout()
        self.setLayout(main_layout)

        images_group = self.__create_images_group()
        buttons_group = self.__create_buttons_group()

        main_layout.addWidget(images_group)
        main_layout.addWidget(buttons_group)

    def __prepare_images(self):
        self.__img_bw_org = QLabel()
        self.__img_bw_org_hist = MplHistCanvas()
        self.__img_bw_eq = QLabel()
        self.__img_bw_eq_hist = MplHistCanvas()

    def __create_images_group(self):
        images_group = QGroupBox()
        images_layout = QGridLayout()

        images_layout.addWidget(self.__img_bw_org, 0, 0)
        images_layout.addWidget(self.__img_bw_org_hist, 0, 1)
        images_layout.addWidget(self.__img_bw_eq, 1, 0)
        images_layout.addWidget(self.__img_bw_eq_hist, 1, 1)

        images_group.setLayout(images_layout)

        return images_group

    def __create_buttons_group(self):
        buttons_layout = QHBoxLayout()
        buttons_layout.addWidget(self.__btn_prev)
        buttons_layout.addWidget(self.__btn_next)
        buttons_layout.addWidget(self.__btn_dir_select)

        buttons_group = QGroupBox()
        buttons_group.setMaximumHeight(50)
        buttons_group.setLayout(buttons_layout)

        return buttons_group

    def __update_window(self, path_to_img):
        org_img = Image.open(path_to_img)
        scale_factor = self.__img_max_height / org_img.size[1]
        org_img = ImageOps.scale(org_img, scale_factor)

        bw_img = ImageOps.grayscale(org_img)
        bw_img_qt = QPixmap.fromImage(ImageQt(bw_img))
        bw_img_eq = ImageOps.equalize(bw_img)
        bw_img_eq_qt = QPixmap.fromImage(ImageQt(bw_img_eq))

        self.__img_bw_org.setPixmap(bw_img_qt)
        self.__img_bw_org_hist.plot_img_hist(bw_img, "Original histogram")
        self.__img_bw_eq.setPixmap(bw_img_eq_qt)
        self.__img_bw_eq_hist.plot_img_hist(bw_img_eq, "Equalized histogram")


if __name__ == "__main__":
    app = QApplication([])

    accepted_formats = (".jpg", ".png")
    img_browser = ImgBrowser(accepted_formats)

    sys.exit(app.exec_())
