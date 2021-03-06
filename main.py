import argparse
import cv2
from skimage import img_as_ubyte
import numpy as np

from gabor import gabor
from threshold import binarise
from skeletonization import skeletonize
from minutae import calculate_minutiaes

from matplotlib import pyplot as plt

def prepare_image(img):
    gabor_img = gabor(img)
    binarised_img = binarise(gabor_img)
    return skeletonize(binarised_img)

def compare_images(img1, img2):
    # Initiate SIFT detector
    orb = cv2.ORB_create()

    # find the keypoints and descriptors with SIFT
    kp1, des1 = orb.detectAndCompute(img1, None)
    kp2, des2 = orb.detectAndCompute(img2, None)

    # create BFMatcher object
    bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)

    # Match descriptors.
    matches = bf.match(des1, des2)

    # Sort them in the order of their distance.
    matches = sorted(matches, key = lambda x : x.distance)
    filtered_matches = [ item for item in matches[:10] if item.distance < 25 ]
    print(len(filtered_matches) / 10)

    # Draw first 10 matches.
    return cv2.drawMatches(img1, kp1, img2, kp2, filtered_matches, flags=2, outImg=None)

def compare(img_file1, img_file2):
    img1 = prepare_image(img_file1)
    img2 = prepare_image(img_file2)

    return compare_images(img1, img2)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("file_path1", type=str)
    parser.add_argument("file_path2", type=str)
    args = parser.parse_args()

    img1 = cv2.imread(args.file_path1, 0)
    img2 = cv2.imread(args.file_path2, 0)

    comp = compare(img1, img2)
    cv2.imshow("comp", comp)

    # gabor_img = gabor(img1)
    # binarised_img = binarise(gabor_img)
    # skeletonized = skeletonize(binarised_img)
    #minutiaes = calculate_minutiaes(skeletonized)

    # cv2.imshow("image", img1)
    # cv2.imshow("gabor", gabor_img)
    # cv2.imshow("binarised", img_as_ubyte(binarised_img))
    # cv2.imshow("skeletonize", skeletonized)
    #cv2.imshow("minutiaes", minutiaes)

    cv2.waitKey(0)
    cv2.destroyAllWindows()
