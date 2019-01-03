"""
All face finding stuff goes here.
Would be pretty great to expand the config part a bit more
"""
import numpy
import cv2
from cv2.cv2 import CASCADE_SCALE_IMAGE
from face_replace import FACE_TYPES, Face
import os

DIR = os.path.dirname(__file__)
FRONT_PATH = DIR + '/paths/haarcascade_frontalface_alt.xml'
PROFILE_PATH = DIR + '/paths/haarcascade_profileface.xml'

class Finder:
    """Uses haar cascade classifier to find all faces and their general orientation"""
    def __init__(self, img):
        self.__gray_img = cv2.imdecode(numpy.fromstring(img, numpy.uint8), cv2.IMREAD_GRAYSCALE)
        rows, cols = numpy.shape(self.__gray_img)

        # Size and Coord properties(x, y)
        self.__img_size = (rows, cols)
        self.__min_face_size = (30, 30)
        self.__img_mid_coord = (rows / 2, cols / 2)

        # Load trained models
        self.__frontal_cascade = cv2.CascadeClassifier(FRONT_PATH)
        self.__profile_cascade = cv2.CascadeClassifier(PROFILE_PATH)

        # Config options
        self.__scale = 1.1
        self.__rot_angle_cw = -30
        self.__rot_angle_ccw = 30
        self.__min_neighbors = 4

    def get_faces(self):
        return self.get_front_faces() + self.get_front_l_faces() + self.get_front_r_faces() + self.get_profile_r_faces() + self.get_profile_l_faces()

    def get_front_faces(self):
        f_type = FACE_TYPES['FRONT']
        return fmt_faces(f_type, self.__get_frontal_faces(self.__gray_img))

    def get_front_l_faces(self):
        f_type = FACE_TYPES['FRONT_LEFT']
        faces = self.__get_rot_frontal_faces(self.__gray_img, self.__rot_angle_ccw)
        return fmt_faces(f_type, faces)

    def get_front_r_faces(self):
        f_type = FACE_TYPES['FRONT_RIGHT']
        faces = self.__get_rot_frontal_faces(self.__gray_img, self.__rot_angle_ccw)
        return fmt_faces(f_type, faces)

    def get_profile_l_faces(self):
        f_type = FACE_TYPES['LEFT']
        faces = self.__get_profile_faces(self.__gray_img)
        return fmt_faces(f_type, faces)

    def get_profile_r_faces(self):
        f_type = FACE_TYPES['RIGHT']
        flip_img = cv2.flip(self.__gray_img, 1)

        # x coordinate has to flip back to mirror img
        width, _ = flip_img.shape[::-1]
        faces = [(x - width, y, w, h) for x, y, w, h in self.__get_profile_faces(flip_img)]

        return fmt_faces(f_type, faces)


    def __get_rot_frontal_faces(self, img, rot_angle):
        M = cv2.getRotationMatrix2D(self.__img_mid_coord, rot_angle, 1)
        rot_img = cv2.warpAffine(img, M, self.__img_size)

        return self.__get_frontal_faces(rot_img)

    def __get_frontal_faces(self, img):
        return self.__frontal_cascade.detectMultiScale(
            img,
            scaleFactor=self.__scale,
            minNeighbors=self.__min_neighbors,
            minSize=self.__min_face_size,
            flags=CASCADE_SCALE_IMAGE)

    def __get_profile_faces(self, img):
        return self.__profile_cascade.detectMultiScale(
            img,
            scaleFactor=self.__scale,
            minNeighbors=self.__min_neighbors,
            minSize=self.__min_face_size,
            flags=CASCADE_SCALE_IMAGE)

def fmt_faces(face_type, faces):
    return [Face(face_type, face) for face in faces]
