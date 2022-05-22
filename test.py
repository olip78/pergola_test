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
url = 'https://petimagesandrei.s3.us-east-1.amazonaws.com/data_deepspect/tensorflow-training-2022-05-17-09-34-33-135/output/model.tar.gz?response-content-disposition=inline&X-Amz-Security-Token=IQoJb3JpZ2luX2VjECgaDGV1LWNlbnRyYWwtMSJGMEQCIHAPCR%2B69pD9KhU5SoL25RTcZed5exPIs3N%2ByKfo4fNFAiBsOFlcXBxc%2FZEiyadqx2mQy04CaRW%2FCaLfyRao5L0h8SrkAggSEAAaDDU4NjE2NzQzOTM1NCIMU3qR4CTrVmNMS9NqKsECTPhRT3HyAvNPAue9eoTePZZhptdC53tRfqDBTQ6%2BmQtgOp5t%2B9jYmPRvmRsKDIrBWjgipAH9T8aHyYc5wqw5tszJyu2q7TzDXbpPTX4DGXlei58gP00UMYQNCPDA2cBWL7yCVw%2BqTmnFulgOgsOd%2FwSR6TjSzzq38wsq%2Fr7HDv2195DkSwT2Hz8rMjZSNu4CMtrH5q9pwGz9kF8jzzRPa1gs39NlBbULsouUrHJTFAHofWp4A4FiShtBb3rEIBb0HiRurUUW%2F9avaB9FxagOlCDUsmGogrsTHzB2T7xYt5nuFeed%2B%2F%2Ffl5khc7DJNAUI9eGQGAnRvZE3emETlwHxQ1c2BLZ2da7%2FpVDU4nCzRvHHT2CJQjW5sKxPMIo%2FbamzADA56vd3ZYhR2tRvtia2hFQa0isK0bRzcW%2BQ9BmUqMbdMMmgnZQGOrQCp93Gg8jE63WqElFm%2F50orpWhNNNMY%2FRuFf3vmwFVimwrz219kR9mV5FoN%2B5lr8KcbK%2BpmEdG23LEyPe0SUYPl5NU%2Fn07UhYfSIBaqh0a4sKffB0GkPRxEDSpRyhNVBNu1RNCAESBrDvjpDxPJw3aCJsHnEAhh4Iwy%2BTMRWiZ5ysTKufhaosDxQpqaW5H1UfNDj%2Bdo8WFAj8ICz%2BqhVg7HC0GXYfjCYNBVpCfkofNmjlvusn9UBCUBxQc%2BiYxVOBiRVjTapi1pFzPll%2F4OhKUoDGnu%2BrhwvzgYCMxKsbTtfElxpexIOeKO%2B31ChoUCrfqF%2BD6wjvinWKepl9htOwpT9f4sAwYD298y9tH%2BBmRNsDBzXFKi7%2BMoY5I8oDhLtTraO9fP9DeqnBF0%2BwV8DTIbEmpGZA%3D&X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Date=20220520T093813Z&X-Amz-SignedHeaders=host&X-Amz-Expires=43200&X-Amz-Credential=ASIAYQ6SNJ75MVC73UUR%2F20220520%2Fus-east-1%2Fs3%2Faws4_request&X-Amz-Signature=6235d526e26ee1a8ec88c961e29f14357119d52481941e932ce18fbfc68d836b'
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
