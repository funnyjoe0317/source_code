import argparse
import os
import pickle

def data_parsing(uwi_label_path, out_lable_count_txt):
    label = [0 for i in range(42)]

    annot_txt_list = sorted(os.listdir(uwi_label_path))

    for i in range(len(annot_txt_list)):
        f = open(os.path.join(uwi_label_path, annot_txt_list[i]))
        f_line = f.readlines()

        print("File Count: {}".format(i + 1))

        for j in range(len(f_line)):
            splited_f_line = f_line[j].split()

            if splited_f_line[0] == str(0):
                label[0] += 1
            elif splited_f_line[0] == str(1):
                label[1] += 1
            elif splited_f_line[0] == str(2):
                label[2] += 1
            elif splited_f_line[0] == str(3):
                label[3] += 1
            elif splited_f_line[0] == str(4):
                label[4] += 1
            elif splited_f_line[0] == str(5):
                label[5] += 1
            elif splited_f_line[0] == str(6):
                label[6] += 1
            elif splited_f_line[0] == str(7):
                label[7] += 1
            elif splited_f_line[0] == str(8):
                label[8] += 1
            elif splited_f_line[0] == str(9):
                label[9] += 1
            elif splited_f_line[0] == str(10):
                label[10] += 1
            elif splited_f_line[0] == str(11):
                label[11] += 1
            elif splited_f_line[0] == str(12):
                label[12] += 1
            elif splited_f_line[0] == str(13):
                label[13] += 1
            elif splited_f_line[0] == str(14):
                label[14] += 1
            elif splited_f_line[0] == str(15):
                label[15] += 1
            elif splited_f_line[0] == str(16):
                label[16] += 1
            elif splited_f_line[0] == str(17):
                label[17] += 1
            elif splited_f_line[0] == str(18):
                label[18] += 1
            elif splited_f_line[0] == str(19):
                label[19] += 1
            elif splited_f_line[0] == str(20):
                label[20] += 1
            elif splited_f_line[0] == str(21):
                label[21] += 1
            elif splited_f_line[0] == str(22):
                label[22] += 1
            elif splited_f_line[0] == str(23):
                label[23] += 1
            elif splited_f_line[0] == str(24):
                label[24] += 1
            elif splited_f_line[0] == str(25):
                label[25] += 1
            elif splited_f_line[0] == str(26):
                label[26] += 1
            elif splited_f_line[0] == str(27):
                label[27] += 1
            elif splited_f_line[0] == str(28):
                label[28] += 1
            elif splited_f_line[0] == str(29):
                label[29] += 1
            elif splited_f_line[0] == str(30):
                label[30] += 1
            elif splited_f_line[0] == str(31):
                label[31] += 1
            elif splited_f_line[0] == str(32):
                label[32] += 1
            elif splited_f_line[0] == str(33):
                label[33] += 1
            elif splited_f_line[0] == str(34):
                label[34] += 1
            elif splited_f_line[0] == str(35):
                label[35] += 1
            elif splited_f_line[0] == str(36):
                label[36] += 1
            elif splited_f_line[0] == str(37):
                label[37] += 1
            elif splited_f_line[0] == str(38):
                label[38] += 1
            elif splited_f_line[0] == str(39):
                label[39] += 1
            elif splited_f_line[0] == str(40):
                label[40] += 1
            elif splited_f_line[0] == str(41):
                label[41] += 1
            elif splited_f_line[0] == str(42):
                label[42] += 1

    str_label = list(map(str,label))
    txt_file_path = os.path.join(out_lable_count_txt, 'valid.txt')

#    with open(txt_file_path, 'wb') as lf:
#        pickle.dump(label, lf)
#    with open(txt_file_path, 'w') as file:
#        file.writelines(str_label)
    print()

    for m in str_label:
        print(m)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    parser.add_argument('--uwi_label_path',default='F:/221228_underwater_images_yolo/labels/train',help='input data root')
    #parser.add_argument('--uwi_label_path', default='F:/221228_underwater_images_yolo/labels/valid', help='input data root')
    parser.add_argument('--out_lable_count_txt', default='F:/221228_underwater_images_yolo/labels', help='')

    args = parser.parse_args()

    data_parsing(args.uwi_label_path, args.out_lable_count_txt)

    print("Finish")