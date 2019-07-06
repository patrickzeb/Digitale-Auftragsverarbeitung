from os import listdir
from random import randint

import cv2
from natsort import natsorted
from numpy import around
from pandas import DataFrame


def _detect_edges(image) -> ((int, int), (int, int)):
    h_begin = h_end = -1
    w_begin = w_end = h_begin

    height, width = image.shape

    for i in range(height):
        if sum(image[i]) < 255 * width:
            h_begin = i
            break

    for i in range(height - 1, 0, -1):
        if sum(image[i]) < 255 * width:
            h_end = i
            break

    for i in range(width):
        if sum(image[:, i]) < 255 * height:
            w_begin = i
            break

    for i in range(width - 1, 0, -1):
        if sum(image[:, i]) < 255 * height:
            w_end = i
            break

    x = (h_begin, w_begin)
    y = (h_end, w_end)

    return x, y


def resize(image_a, image_b):
    x, y = _detect_edges(image_a)
    edges_a = image_a[x[0]: y[0], x[1]:y[1]]

    x, y = _detect_edges(image_b)
    edges_b = image_b[x[0]: y[0], x[1]:y[1]]

    if edges_a.sum() < edges_b.sum():
        resized_a = edges_a
        resized_b = cv2.resize(edges_b, edges_a.shape[::-1], interpolation=cv2.INTER_CUBIC)
    else:
        resized_a = cv2.resize(edges_a, edges_b.shape[::-1], interpolation=cv2.INTER_CUBIC)
        resized_b = edges_b

    return resized_a, resized_b


def add_noise(image, ignore=False):
    if ignore:
        return image

    height, width = image.shape

    for h in range(height):
        for w in range(width):
            if image[h, w] > 250:
                image[h, w] = randint(100, 150)

    return image


def sift_sim(image_a, image_b):
    orb = cv2.ORB_create()

    kp_a, desc_a = orb.detectAndCompute(image_a, None)
    kp_b, desc_b = orb.detectAndCompute(image_b, None)

    bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)

    matches = bf.match(desc_a, desc_b)
    similar_regions = [i for i in matches if i.distance < 70]

    if len(similar_regions) == 0:
        return 0

    return len(similar_regions) / len(matches)


signatures = [file for file in listdir('./upload/') if file.startswith('Unterschrift')]
signatures = natsorted(signatures)




def show_reference(application) -> None:
    from IPython.display import Image

    if application == "Dinglich":
        reference = './upload/signatures/Referenz_Dinglich.jpg'
    elif application == "Blanko":
        reference = './upload/signatures/Referenz_Blanko.jpg'

    print (application)
    print('Als Referenz wurde die folgende Unterschrift aus dem Antrag ausgelesen:')
    display(Image(filename=reference, width=400))


def compare_signatures(application, compared_signature) -> None:
    if application == "Dinglich":
        original = 'Referenz_Dinglich.jpg'
    elif application == "Blanko":
        original = 'Referenz_Blanko.jpg'

    # original = 'Unterschrift_01_richtig.png'
	
    compared_signature = str(compared_signature)
    original = str(original)
    sims = []
    image_a = cv2.imread('./upload/signatures/' + original)
    image_b = cv2.imread('./upload/' + compared_signature)

    image_a = cv2.cvtColor(image_a, cv2.COLOR_BGR2GRAY)
    image_b = cv2.cvtColor(image_b, cv2.COLOR_BGR2GRAY)

    resized_a, resized_b = resize(image_a, image_b)
    
    noised_a = add_noise(resized_a, ignore=True)
    noised_b = add_noise(resized_b, ignore=True)

    sim = sift_sim(noised_a, noised_b)

    sims.append(around(sim, 3))
    
    df = DataFrame([sims], index=[original], columns=signatures)
    df.plot()
    # df.to_csv('./signatures.csv')

