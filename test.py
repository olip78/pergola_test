import urllib.request
import tarfile
import os
import tensorflow as tf
import numpy as np
import tempfile
import PIL.Image, PIL.ImageOps
from matplotlib import pyplot as plt

def img_preprocessong(img_path, dim=(224, 224)):
    pil_image = PIL.Image.open(img_path)
    pil_image = PIL.ImageOps.pad(pil_image, (dim[0], dim[1]))
    pil_image = pil_image.convert('RGB')
    return np.asarray(pil_image)

def draw_img(img_path, text=''):
    fig, ax = plt.subplots(1, 1, figsize=(6, 6))
    with PIL.Image.open(img_path) as img:
        rgbimg = PIL.Image.new("RGBA", img.size)
        rgbimg.paste(img)
        ax.grid(False)
        ax.imshow(rgbimg)
        ax.set_title(text)
        plt.show()

# shared link onla for 12 hours:
url = 'https://petimagesandrei.s3.us-east-1.amazonaws.com/data_deepspect/tensorflow-training-2022-05-16-17-19-20-561/output/model.tar.gz?response-content-disposition=inline&X-Amz-Security-Token=IQoJb3JpZ2luX2VjEHAaCWV1LXdlc3QtMiJHMEUCIQDOm%2Bg7s6BCNvNCTdJCAr63DbgvQ4HpGd2uaXYsH5cGAgIgflzM715wlLQUWZNtqLXpT6OvRQcjgphzfVpsKxMcdKsq5AIIWRAAGgw1ODYxNjc0MzkzNTQiDGrQp848FfnvpUkksSrBAjwsOLfKnlCaDl%2BH%2BYFJDM3NQkV%2FJLRmXcyHigwSaoMhHf09vGdcHmJYxeA%2FXFnUqml2xQuhO9YC8silhRYErgHcElXC93LyoHFvR518Ma%2BbU6Hx%2Flt2GBYKnE1y%2F%2FbgWhCq5aT9N6AMjmCoe65TomBKfMrdkV0jdPaK0RMbHztVqkgbIH51vHn6f%2F%2BiS61fX%2B%2B8j8gH5O62LcAd4D9rcC2Z9DMg3a8YL9h4TkCnk4r%2Fb2LnchBdkECv5WmYiPGcS21pDL%2BbBQhGosXZx0TBMItrxQLG8ttivcERnGjHp%2FoB0aM%2Bvo34Uz1FVdvJm2dT9V1wwrWuTZGXRvGra63UiDlbWRlzGZ59cRX0clxsj6yAMnFene9B%2FTPIKC%2Fe3xzw005xGcR6HT%2Fq8NI7yzfr1rUkYPYPUWXv%2BdvFF%2FdufNiVvjCR86yUBjqzAnNIcw9mdDsBdzsfZSETrg%2BdZ2tLIRWC2V0Nn7WaroiBu9G80LwuoSuhJDUesUW0vhlp%2FARJcEc0U3ue6eZjowpPnriVpaRXhqZvfhhd6pke8DXNH4ebLOIuLD254r6%2BTYveJkZzu7dWCuBD8GH8J0PzpMaUGnmIhOWh2ZD4tLF7RYklhsJgvOhoDTCXaL0Ucbf0B0rth0nyYTYAnT8e5FfkGqxc5tjvxfou%2F1%2FHtLS8WHK33P42jrIaJoQsYtgtcOKrWc8FwxGflMErxBfTn%2BAo80Qeq8cRXjlGJaJQ0M77V50qKzdXdIuBlcmMGpC5NEPzHvM%2Fi%2BtvYWdsuJW01cQBt%2F4JS8QVOH5qrR%2BfVeuF%2FXqf2ZnuX%2FGwaoBZjGP5UH9NnWU%2Fy9eOI8b3Kc2w1VVsmn0%3D&X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Date=20220523T073715Z&X-Amz-SignedHeaders=host&X-Amz-Expires=43200&X-Amz-Credential=ASIAYQ6SNJ75J474I5JP%2F20220523%2Fus-east-1%2Fs3%2Faws4_request&X-Amz-Signature=9c49ae547f322ca23ed3346f618a9e61297f877b6c63ebbe90e55e054c9a645f'
ftpstream = urllib.request.urlopen(url)
tar = tarfile.open(fileobj=ftpstream, mode="r|gz")

with tempfile.TemporaryDirectory() as tmpdirname:
    tar.extractall(path=tmpdirname)
    model = tf.keras.models.load_model(os.path.join(tmpdirname, 'model'))
    

#img_path = '/Users/andreichekunov/brandcompete/deepspect/Original/VIM2_CV1_C1_181-2 pseudo reject/VIM2_CV1_C1_181-2_(623)_NG_OK.png'

img_path = ''
print('for stopping enter "q"')
while img_path != 'q':
    print('input an img path: ')
    img_path = input()
    ext = img_path.split('.')[-1]
    if ext in ['png', 'jpg']:
        v = model.predict(np.expand_dims(img_preprocessong(img_path), axis=0))[0][0]
        if v >0.5:
            text = 'img is ok, p = {}'.format(v)
        else:
            text = 'img contains a deffect, p = {}'.format(v)
        draw_img(img_path, text=text)
