import glob
import os
import argparse
from PIL import Image, ImageDraw, ImageFont


def mark_img(src_file, marks, dst_file):
    image = Image.open(src_file)
    # width, height = image.size
    draw = ImageDraw.Draw(image)

    font = ImageFont.truetype('Arial.ttf', 15)
    # text_width, text_height = draw.textsize(marks, font)

    # calculate the x,y coordinates of the text
    margin = 5
    x = margin
    y = margin

    # draw watermark in the bottom right corner
    draw.text((x, y), marks, fill=(255, 0, 0, 255), font=font)

    image.save(dst_file)

    print "{} Marked.".format(src_file)


def read_marks_from_file(marks_file, line_num):
    mark = ''
    fp = open(marks_file)
    for i, line in enumerate(fp):
        if i == line_num - 1:
            mark = line
            break
    fp.close()
    return mark


def batch_mark(src_dir, dst_dir, marks_file, file_prefix="demo_", dynamic_filename_len=8, file_type='jpg'):
    files_len = len(glob.glob1(src_dir, "*.{}".format(file_type)))

    for i in range(0, files_len):
        formatter = '{{0:0{}}}'.format(dynamic_filename_len)
        dynamic_filename = formatter.format(i)
        src_file = os.path.join(src_dir, '{}{}.{}'.format(file_prefix, dynamic_filename, file_type))
        dst_file = os.path.join(dst_dir, '{}{}.{}'.format(file_prefix, dynamic_filename, file_type))
        if src_file == dst_file:
            raise ValueError("Source directory should not be Destination directory.")
        mark = read_marks_from_file(marks_file, i)
        mark_img(src_file, mark, dst_file)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-s', help='Source directory')
    parser.add_argument('-d', help='Destination directory')
    parser.add_argument('-m', help='Marks file, one mark one line')
    parser.add_argument('-p', help='Filename prefix')
    parser.add_argument('-l', help='Fixed length of filename dynamic part, for example,' \
                                   ' demo_00012.jpg -l is 5, -p is demo_')
    parser.add_argument('-t', help='File type, such as jpg, png etc.')
    args = parser.parse_args()

    batch_mark(args.s, args.d, args.m, args.p, args.l, args.t)
