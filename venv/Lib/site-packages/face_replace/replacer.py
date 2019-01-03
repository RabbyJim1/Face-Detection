from io import BytesIO
from PIL import Image
from face_replace import Finder

def replace_faces(img, replace_img_path):
    faces = Finder(img).get_faces()

    if not len(faces):
        return img

    target_img = Image.open(BytesIO(img))
    target_img = target_img.convert("RGBA")
    replace_img = Image.open(replace_img_path)

    for face in faces:
        scaled_img = replace_img.resize((face.width, face.height))
        alpha_layer = Image.new("RGBA", target_img.size)
        alpha_layer.paste(scaled_img, (face.coord_x1, face.coord_y1), scaled_img)
        target_img = Image.alpha_composite(target_img, alpha_layer)

    return target_img
