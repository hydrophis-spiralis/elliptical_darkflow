import numpy as np
import cv2
import os

min_disks = 1
max_disks = 10
max_disk_a = 100
max_disk_b = 100
thickness = 10
color = (0, 255, 0)


def generate_circles(circles_num,w,h):
    circles = []
    for i in range(np.random.randint(min_disks, circles_num)):
        x = np.random.randint(low = max_disk_a, high=w - max_disk_a)
        y = np.random.randint(low=max_disk_b, high=h - max_disk_b)
        a = np.random.randint(max_disk_a / 2, max_disk_a)
        b = np.random.randint(max_disk_b / 2, max_disk_b)
        angle = np.random.randint(-90, 90)
        color = (np.random.randint(127,255),np.random.randint(127,255),np.random.randint(127,255))
        circles.append([int(x),int(y),int(a),int(b),int(angle), color])
    return circles

def paint_circles(background, circles):
    for circle in circles:
        x, y, a,b, angle, color = circle
        cv2.ellipse(background,(x, y), (a, b), angle, 0, 360, color, -1)
    return background

def generate_img(background_file, circles, filename):
    img = cv2.imread(background_file)
    paint_circles(img, circles)
    cv2.imwrite(filename=filename, img=img)

def write_label(circles, img_filename, filename):
    strings = []

    for circle in circles:
        print(circle)
        strings.append("{}\t{}\t{}\t{}\t{}\t{}\n".format(img_filename, circle[0], circle[1],circle[2],circle[3],circle[4]))

    with open(filename, 'a') as f:
        for string in strings:
            f.write(string)

def main(folder, count, background_file = 'back.jpg'):
    background = cv2.imread(background_file)
    h, w, num_channel = background.shape
    del background

    label_filename = os.path.join(folder, "dataset.txt")

    for i in range(count):
        circles = generate_circles(4, w,h)
        filename  = os.path.join(folder, "f_{}.png".format(i))
        generate_img(background_file, circles, filename)
        write_label(circles,filename, label_filename)

if  __name__=='__main__':
    main('/home/spiralis/datasets/elipse_regions/train', 20000)