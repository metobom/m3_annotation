import os
import matplotlib.pyplot as plt
import cv2
from matplotlib.widgets import PolygonSelector, TextBox
import numpy as np
import shutil
import sys

from create_json import to_json


class metos_annotation_tool():
    def __init__(self):
        # PROGRAMI ISTEDIGINIZ GIBI AYARLAMAK ICIN BURADAKI DEGERLERLE OYNAYIN.
        self.dataset_image_size = (512, 256)
        self.guide_line_freq = 22 # Çizilecek yardımcı çizgi sayısı. 
        self.window_start_loc = '+200+300' # Açılacak pencerenin konumu.
        self.window_size = (12, 6) # Açılacak pencerenin boyutu.
        self.required_point_number = 12 # Eğer belirli bir sayıda nokta işaretlemeniz gerekiyorsa ayarlayın.
        self.log_check0 = False # Işaretlediğiniz nokta sayısını yazdırmak için ayarlayın.
        self.log_check1 = True # Q ile bir sonraki resme geçtiğizde kaç nokta işaretlediğinizi, noktaların u, v kordinatlarını, ve lines listinin uzunluğunu yazdırmak için ayarlayın.
        self.shut_down_key = 'x' # Programı kapatmak için istediğiniz tuşu ayarlayın.
        self.next_image_key = 'q' # Bir sonraki resme geçmek için istediğiniz tuşu ayarlayın.
        self.line_color = 'y' # {'b', 'g', 'r', 'c', 'm', 'y', 'k', 'w'}
        self.line_alpha = 0.6 # noktalari secerken olusan dogrularin seffafligi
        self.guideline_alpha = 0.7
        self.guidline_thickness = 2 # yardimci dogrularin kalinligi

        self.image_path = 'Images/' # Veri setinizde bulunan resimlerin bulunacağı yol.
        self.annotated_image_path = 'Images/annotated_images/' # Işaretlediğniz resimlerin taşınacağı yol.
        self.image_path_for_json = ' '
        #######################################################################

        self.count = 0
        self.image = None
        self.lines = []

    def shut_down(self, shut_down_event):
        if shut_down_event.key == self.shut_down_key or shut_down_event.key == self.shut_down_key.upper():
            print('Kapatiliyor...')
            sys.exit()

    def point_callback(self, click):
        u, v = click.xdata, click.ydata
        self.lines.append(int(u))
        self.lines.append(int(v))
        self.count += 1
        if self.log_check0:
            print('Nokta sayisi: ', self.count)
            if self.count == self.required_point_number:
                count = 0
                print('!!!!! SONRAKI RESME GEC !!!!!')

    def toggle_selector(self, selector_event):
        toggle_selector.RS.set_active(True)

    def onpress(self, onpress_event):
        if onpress_event.key == self.next_image_key or onpress_event.key == self.next_image_key.upper():
            # console logs
            if self.log_check1:
                print('Dogru kordinatlari: ', self.lines)
                print('lines degiskeni uzunlugu: ', len(self.lines))
                print('Toplam isaretlenen nokta sayisi: ', len(self.lines) // 2)
            # for safety
            if len(self.lines) != 0:
                to_json(self.lines, self.image_path_for_json)
                shutil.move(self.image_path_for_json, self.annotated_image_path)
            self.image = None
            self.lines = []
            plt.close()

    def main(self):
        for filename in os.listdir(self.image_path):
            if filename.endswith('.jpg') or filename.endswith('.png'):
                print('Resim adi: ', filename)
                image = cv2.imread(self.image_path + filename)
                self.image_path_for_json = self.image_path + filename
        
                # give your dataset image size to resize function
                image = cv2.resize(image, self.dataset_image_size)
                image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
                # for guide lines
                black_image = np.zeros_like(image)
                for i in range(image.shape[0]):
                    if i % 22 == 0:
                        black_image = cv2.line(black_image, (0, i), (image.shape[1], i), (255, 0, 0), 2)
                image = cv2.addWeighted(image, 1, black_image, self.guideline_alpha, self.guidline_thickness)
                # plot
                fig, ax = plt.subplots(1, figsize = self.window_size)
                ax = plt.axes([0.0, 0.0, 1.0, 1.0])
                ax.imshow(image)
                fig.canvas
                plt.xlabel(filename)
                mngr = plt.get_current_fig_manager()
                mngr.window.wm_geometry(self.window_start_loc)

                # for visualizing linestrips
                self.toggle_selector = PolygonSelector(ax, True, True, lineprops = dict(color = self.line_color, linestyle = '-', linewidth = 2, alpha = self.line_alpha)) # (c m w k y)
                # events
                line_strips = plt.connect('button_press_event', self.point_callback)
                key = plt.connect('key_press_event', self.onpress)
                shutit = plt.connect('key_press_event', self.shut_down)

                plt.show()

if __name__ == "__main__":
    app = metos_annotation_tool()
    app.main()
