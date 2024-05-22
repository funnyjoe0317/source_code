import argparse
import os
import cv2
import shutil

def data_parsing(origin_data,out_train_data,out_val_data):
    print('start')
    file_list = sorted(os.listdir(origin_data))

    if not os.path.exists(out_train_data):
        os.makedirs(out_train_data)

    if not os.path.exists(out_val_data):
        os.makedirs(out_val_data)


    star_sequence_num = '001'
    #star_sequence_num = '510'
    sequence_list = []

    for index in range(len(file_list)):
        if star_sequence_num == file_list[index].split('-')[1]:

            sequence_list.append(file_list[index])

            if index == len(file_list) - 1:
                # 마지막 train/ val 처리
                val_num = int(len(sequence_list) / 10)
                train_num = len(sequence_list) - val_num

                for t in range(0, train_num):
                    train_img_path = os.path.join(origin_data, sequence_list[t])
                    train_img_copy = os.path.join(out_train_data, sequence_list[t])

                    shutil.copy(train_img_path, train_img_copy)

                for v in range(train_num, len(sequence_list)):
                    val_img_path = os.path.join(origin_data, sequence_list[v])
                    val_img_copy = os.path.join(out_val_data, sequence_list[v])

                    shutil.copy(val_img_path, val_img_copy)

        elif star_sequence_num != file_list[index].split('-')[1]:
            # train/ val 처리
            val_num = int(len(sequence_list)/10)
            train_num = len(sequence_list) - val_num

            for t in range(0, train_num):
                train_img_path = os.path.join(origin_data, sequence_list[t])
                train_img_copy = os.path.join(out_train_data, sequence_list[t])

                shutil.copy(train_img_path, train_img_copy)

            for v in range(train_num, len(sequence_list)):
                val_img_path = os.path.join(origin_data, sequence_list[v])
                val_img_copy = os.path.join(out_val_data, sequence_list[v])

                shutil.copy(val_img_path, val_img_copy)

            print('copy class: {}'.format(star_sequence_num))

            #list 초기화
            star_sequence_num = file_list[index].split('-')[1]
            sequence_list = []

            #list 새 시작점 저장
            sequence_list.append(file_list[index])

def label_copy(origin_img_path, origin_label_path, label_copy_path):
    file_list = sorted(os.listdir(origin_img_path))

    for i in range(len(file_list)):
        file_name = file_list[i][:-4]

        origin_label_file = os.path.join(origin_label_path, file_name + '.txt')
        copy_label_file = os.path.join(label_copy_path, file_name + '.txt')

        shutil.copy(origin_label_file, copy_label_file)

        print('copy txt: {}'.format(file_name))

def pair_check(img_path, label_path):
    file_list = sorted(os.listdir(img_path))
    label_list = sorted(os.listdir(label_path))

    txt_file = open('F:/Underwater/object_detection/empty_label_file.txt', 'a+')

    for i in range(len(file_list)):

        file_check = os.path.isfile(os.path.join(label_path, file_list[i][:-4] + '.jpg'))

        if file_check == False:
            txt_file.write('{}\n'.format(file_list[i]))

    txt_file.close()

def extract_data(extract_img_path, extract_label_path, copy_img_path, copy_label_path):
    img_file_list = sorted(os.listdir(extract_img_path))

    file_count = 0

    for i in range(len(img_file_list)):
        ex_label_data = os.path.join(extract_label_path, img_file_list[i][:-4] + '.txt')

        txt_file_check = os.path.isfile(ex_label_data)


        if txt_file_check == True:
            shutil.copy(os.path.join(extract_img_path, img_file_list[i][:-4] + '.jpg'), os.path.join(copy_img_path, img_file_list[i][:-4] + '.jpg'))   # img copy
            shutil.copy(os.path.join(extract_label_path, img_file_list[i][:-4] + '.txt'), os.path.join(copy_label_path, img_file_list[i][:-4] + '.txt'))   # label copy

            file_count += 1

            print('copy file: {}'.format(img_file_list[i][:-4]))

    print('\ncopy file num: {}'.format(file_count))

def label_delete(txt_file_path, del_txt_file_path):

    txt_file_list = sorted(os.listdir(txt_file_path))

    for i in range(len(txt_file_list)):

        input_txt_file_path = os.path.join(txt_file_path, txt_file_list[i])

        f = open(input_txt_file_path)

        txt_line = f.readlines()

        write_txt_path = os.path.join(del_txt_file_path, txt_file_list[i])
        write_txt_file = open(write_txt_path,'a+')

        for j in range(len(txt_line)):

            txt_line_split = txt_line[j].split(' ')
            joined_txt_line = " ".join(txt_line_split[:5])

            write_txt_file.write('{}\n'.format(joined_txt_line))

        write_txt_file.close()




if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    parser.add_argument('--origin_data',default='J:/Underwater/underwater_images/work_yolo/4_original_dataset_corrected_images_from_uncorrected/labels',help='input data root')
    parser.add_argument('--out_train_data', default='J:/Underwater/underwater_images/work_yolo/4_original_dataset_corrected_images_from_uncorrected/yolo/labels/train', help='data root')
    parser.add_argument('--out_val_data', default='J:/Underwater/underwater_images/work_yolo/4_original_dataset_corrected_images_from_uncorrected/yolo/labels/val', help='data root')

    parser.add_argument('--origin_img_path',default='F:/Underwater/object_detection/underwater_images_yolo/images/train',help='input data root')
    parser.add_argument('--origin_label_path', default='F:/Underwater/object_detection/annotations/221122_annotations_yolo/labels', help='input data root')
    parser.add_argument('--label_copy_path', default='F:/Underwater/object_detection/underwater_images_yolo/labels/train', help='input data root')

    parser.add_argument('--img_path', default='F:/Underwater/object_detection/underwater_images', help='input data root')
    parser.add_argument('--label_path', default='F:/Underwater/object_detection/annotations/221122_annotations_yolo/labels', help='input data root')

    parser.add_argument('--extract_img_path', default='F:/Underwater/object_detection/underwater_images/', help='input data root')
    parser.add_argument('--extract_label_path', default='F:/Underwater/object_detection/annotations/221122_annotations_yolo/labels', help='input data root')
    parser.add_argument('--copy_img_path', default='F:/Underwater/object_detection/underwater_images_yolo_base/image', help='input data root')
    parser.add_argument('--copy_label_path', default='F:/Underwater/object_detection/underwater_images_yolo_base/label', help='input data root')

    parser.add_argument('--txt_file_path', default='F:/Underwater/annotation_yolo/221228_annotations_yolo/labels', help='input data root')
    parser.add_argument('--del_txt_file_path', default='F:/Underwater/annotation_yolo/221228_annotations_yolo/edit_labels', help='input data root')

    args = parser.parse_args()

    data_parsing(args.origin_data, args.out_train_data, args.out_val_data)

    #label_copy(args.origin_img_path, args.origin_label_path, args.label_copy_path)

    #pair_check(args.img_path, args.label_path)
    #pair_check(args.label_path, args.img_path)

    #extract_data(args.extract_img_path, args.extract_label_path, args.copy_img_path, args.copy_label_path)

    #label_delete(args.txt_file_path, args.del_txt_file_path)

    print("Finish")