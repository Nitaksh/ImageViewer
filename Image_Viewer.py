import sys
import random
import pickle
import requests
from PyQt6.QtWidgets import *
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QImage, QPixmap, QPen,QPainter,QColor
#Code by R-Nithish (R.No 21PD23) PSG College Of Technology, Coimbatore
#
# Class to download given image
#
# Member Functions:
# 1) download()
#    This function uses the requests API to download the 
#    image from the given URL.
#

class DownloadableImage:
    def __init__(self, url):
        self.url = url

    def download(self):
        try:
            response = requests.get(self.url)
            img = QImage()
            img.loadFromData(response.content)
            return QPixmap.fromImage(img)
        except Exception as e:
            QMessageBox.critical(None, "Error downloading image", 
                                 f"Unable to download an image: {e}")
            return None

#
# Class to initiate the GUI
#

class ImageGraphicsScene(QGraphicsScene):
    def __init__(self):
        super().__init__()
        self.center_line = None

    def clear_center_line(self):
        if self.center_line:
            self.removeItem(self.center_line)
            self.center_line = None

    def draw_center_line(self, start, end):
        pen = QPen()
        pen.setWidth(2)
        pen.setStyle(Qt.PenStyle.DotLine)

        self.center_line = \
            self.addLine(start.x(), start.y(), end.x(), end.y(), pen)

#
# Class to initiate the main window
#
# Member Functions:
# 1) init_gui()
#    Adding buttons and defining layout.
#     
# 2) add_image()
#    Adding functionality to the add image button.
#
# 3) group_images()
#    Adding functionality to group image button.
#
# 4) get_random_image_url()
#    Use random function to choose a random URL from 
#    the given set of image URL.
#
# 5) connnect_central_points()
#    Adding functionality to the connect central points 
#    button.
#

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        self.init_gui()

    def init_gui(self):
        self.scene = ImageGraphicsScene()
        self.view = QGraphicsView(self.scene)

        self.button_add = QPushButton("Add Image")
        self.button_add.clicked.connect(self.add_image)

        self.button_group = QPushButton("Group Images")
        self.button_group.clicked.connect(self.group_images)

        self.button_connect_center = \
                    QPushButton("Connect Image Centers")
        self.button_connect_center.setCheckable(True)
        self.button_connect_center.clicked.connect\
                        (self.connect_central_points)

        layout = QVBoxLayout()
        layout.addWidget(self.view)
        layout.addWidget(self.button_add)
        layout.addWidget(self.button_group)
        layout.addWidget(self.button_connect_center)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        self.setGeometry(100, 100, 1280, 720)
        self.setWindowTitle("Image viewer")

    def add_image(self):
        random_image_url = self.get_random_image_url()
        downloadable_image = DownloadableImage(random_image_url)
        image = downloadable_image.download() 

        if image:
            x, y = random.randint(0, 600), random.randint(0, 400)
            item = self.scene.addPixmap(image)
            item.setPos(x, y)
            item.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsMovable)
            item.setFlag \
                (QGraphicsItem.GraphicsItemFlag.ItemIsSelectable)

            width, height = image.width(), image.height()
            image_color = None
            for i in range(width):
                for j in range(height):
                    color = image.toImage().pixelColor(i, j)
                    if color.alpha() > 0:
                        image_color = color
                        break

            if image_color:
                QMessageBox.information(self, "Image Information",
                f"Image size: {width} x {height}")

    def group_images(self):
        group = QGraphicsItemGroup()
        for item in self.view.scene().selectedItems():
            group.addToGroup(item)

        self.view.scene().addItem(group)
        group.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsMovable)
        group.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsSelectable)

    def get_random_image_url(self):
        with open("Images.dat",'rb') as file :
            url = random.choice(pickle.load(file))
        return "https://raw.githubusercontent.com/hfg-gmuend/"+\
            "openmoji/44c02495e040c52fbea0bfb1cba89aa24754f9a8/"+\
            "src/symbols/geometric/"+url

    def connect_central_points(self, checked):
        if checked:
            self.view.setRenderHint(QPainter.RenderHint.Antialiasing)
            
            self.view.setRenderHint\
            (QPainter.RenderHint.SmoothPixmapTransform)
            
            selected_items = self.view.scene().selectedItems()

            if len(selected_items) < 2:
                QMessageBox.warning
                (self, "Cannot Connect Centers", 
                "Select at least two items to connect centers.")
                
                self.button_connect_center.setChecked(False)
            else:
                self.scene.clear_center_line()
                p1 = selected_items[0].sceneBoundingRect().center()
                p2 = selected_items[1].sceneBoundingRect().center()
                self.scene.draw_center_line(p1, p2)
        else:
            self.view.setRenderHint 
            (QPainter.RenderHint.Antialiasing, False)
            
            self.view.setRenderHint
            (QPainter.RenderHint.SmoothPixmapTransform, False)
            
            self.scene.clear_center_line()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())