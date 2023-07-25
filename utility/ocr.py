import os
import datetime
from time import time
import pandas as pd
from paddleocr import PaddleOCR
import re
import copy


class Ocr:
    path = '/home/sunprizrak/Изображения/vladimir'

    def __init__(self):
        self.data = []

    @staticmethod
    def reform(data: list):
        res = list(map(str.strip, [el[1][0] for el in data[0]]))

        # remove (Profile, X)
        for el in copy.copy(res):
            count = 0
            if el.lower() == 'profile' or el.lower() == 'x':
                res.remove(el)
                count += 1
            if count == 2:
                break

        # remove CT
        for el in res:
            if re.fullmatch('ct\d\d[:;]\d\d', el.lower()):
                res.remove(el)
                break

        # remove LVL
        for el in res:
            if re.fullmatch('l\D*[.]\d*', el.lower()):
                res.remove(el)
                break
            elif re.fullmatch('l\D*\d', el.lower()):
                res.remove(el)
                break
        for i, el in enumerate(res):
            if re.fullmatch('id[:;]\d*', el.lower()):
                res[i] = el[3:]
                break
            elif re.fullmatch('id\d*]', el.lower()):
                res[i] = el[2:]
                break
            elif re.fullmatch('id[:;]\d*\D*[.]\d', el.lower()):
                el_id = list(el[3:-1])
                for x in list(el[3:-1]):
                    if not x.isdigit():
                        el_id.remove(x)
                res[i] = ''.join(el_id)
                break
            elif re.fullmatch('id\d*\D*[.]\d', el.lower()):
                el_id = list(el[2:-1])
                for x in list(el[2:-1]):
                    if not x.isdigit():
                        el_id.remove(x)
                res[i] = ''.join(el_id)
                break
            elif re.fullmatch('\d*\D*[.]\d', el.lower()):
                el_id = list(el[:-1])
                for x in list(el[:-1]):
                    if not x.isdigit():
                        el_id.remove(x)
                res[i] = ''.join(el_id)
                break

        # Club, % to number
        for i, el in enumerate(res):
            if re.fullmatch('\w{4}[:;].*', el.lower()):
                res[i] = el[5:]
            elif re.fullmatch('\d*%', el):
                res[i] = el[:-1]

        # remove words
        for i, el in enumerate(res[3:]):
            if not el.isdigit() and not re.fullmatch('\d*[,.]\d*', el):
                res.remove(el)

        if len(res) < 15:
            res = res[:8]
        else:
            lines = [res[3:7], res[7:11], res[11:]]
            res = res[:3] + lines[0][:2] + [lines[1][0], lines[1][2]] + [lines[2][0]]

        now = datetime.datetime.now()
        date = now.strftime("%d/%m/%Y")
        res.append(date)
        return res

    def main(self):
        os.chdir(path=self.path)
        dir_list = os.listdir(path=self.path)
        setattr(self, 'ocr', PaddleOCR(use_angle_cls=True, show_log=False))

        for el in dir_list:
            image_data = getattr(self, 'ocr').ocr(el)
            reform_data = self.reform(image_data)

            if self.data:

                for i, elem in enumerate(self.data):
                    if elem[1] == reform_data[1]:
                        self.data.remove(self.data[i])
                        break

            self.data.append(reform_data)
            print(reform_data)

    def __call__(self, *args, **kwargs):
        self.main()
        return self.data


if __name__ == '__main__':
    start = time()
    ocr = Ocr()
    ocr()
    print(f"Время затраченное на работу: {time() - start}")
    # columns = ['Username', 'ID', 'Club', 'VPIP', 'PFR', '3-Bet', 'C-Bet', 'Total_Hands', 'Date']

    # df = pd.DataFrame(self.data, index=range(1, len(self.data)+1), columns=columns)
    # #pd.set_option('display.max_rows', None)
    # pd.set_option('display.max_columns', None)
    # print(df)