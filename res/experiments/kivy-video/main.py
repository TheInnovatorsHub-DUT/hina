# coding:utf-8
from kivy.app import App
from kivy.uix.image import Image
from kivy.clock import Clock
from kivy.graphics.texture import Texture
import cv2


class KivyCamera(Image):

    def __init__(self, capture, fps, **kwargs):
        super(KivyCamera, self).__init__(**kwargs)
        self.capture = capture
        Clock.schedule_interval(self.update, 1.0 / fps)

    def update(self, dt):
        faceCascade = cv2.CascadeClassifier(cv2.data.haarcascades +
                                            'haarcascade_frontalface_default.xml')

        ret, frame = self.capture.read()
        if ret:

            frameGray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)  # added
            faces = faceCascade.detectMultiScale(frameGray, 1.1, 4)  # added

            for (x, y, w, h) in faces:  # added
                cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0),
                              2)  # added

            # convert it to texture
            buf1 = cv2.flip(frame, 0)
            buf = buf1.tostring()
            image_texture = Texture.create(size=(frame.shape[1],
                                                 frame.shape[0]),
                                           colorfmt='bgr')
            image_texture.blit_buffer(buf, colorfmt='bgr', bufferfmt='ubyte')
            # display image from the texture
            self.texture = image_texture


class CamApp(App):

    def build(self):
        self.capture = cv2.VideoCapture(0)
        self.my_camera = KivyCamera(capture=self.capture, fps=30)
        return self.my_camera

    def on_stop(self):
        #without this, app will not exit even if the window is closed
        self.capture.release()


if __name__ == '__main__':
    CamApp().run()
