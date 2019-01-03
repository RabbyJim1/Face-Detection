class Face:
    def __init__(self, face_type, face_coordinates):
        self.face_type = face_type
        self.coord_x1 = face_coordinates[0]
        self.coord_y1 = face_coordinates[1]
        self.width = face_coordinates[2]
        self.height = face_coordinates[3]
        self.coord_x2 = self.coord_x1 + self.width
        self.coord_y2 = self.coord_y1 + self.height
