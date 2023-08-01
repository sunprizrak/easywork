import os
import datetime
from time import time
from paddleocr import PaddleOCR
import re


class Ocr:
    def __init__(self):
        self.data = {}

    @staticmethod
    def reform(data: list, path: str):
        res = list(map(str.strip, [el[1][0] for el in data[0]]))

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

        # id and cut profile with x
        for i, el in enumerate(res):
            if re.fullmatch('[a-z]{,2}[:;]\d*', el.lower()):
                for symbl in [':', ';']:
                    if symbl in el:
                        res[i] = el.split(symbl)[1]
                        res = res[i-1:]  # cut profile and x if there
                        break
            elif re.fullmatch('[a-z]{,2}[:;]\d*[a-z]{,3}[.]\d', el.lower()):
                for symbl in [':', ';']:
                    if symbl in el:
                        res[i] = ''.join([ex for ex in el.split(symbl)[1].split('.')[0] if ex.isdigit()])
                        res = res[i-1:]  # cut profile and x if there
                        break

        # Club and % to number
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

        res.insert(0, path)

        now = datetime.datetime.now()
        date = now.strftime("%d/%m/%Y")
        res.append(date)
        return res

    def main(self, path: str):
        setattr(self, 'path', path)
        setattr(self, 'ocr', PaddleOCR(use_angle_cls=True, show_log=False))

        if os.path.isfile(self.path):
            dir_name = os.path.dirname(path)
            file_name = os.path.basename(path)
            os.chdir(path=dir_name)
            image_data = getattr(self, 'ocr').ocr(file_name)
            reform_data = self.reform(image_data, self.path)
            self.data[reform_data[2]] = reform_data
        elif os.path.isdir(self.path):
            os.chdir(path=self.path)
            dir_list = os.listdir(path=self.path)

            for el in dir_list:
                if os.path.isfile(os.path.join(self.path, el)):
                    image_data = getattr(self, 'ocr').ocr(el)
                    path = os.path.join(self.path, el)
                    reform_data = self.reform(image_data, path)
                    print(reform_data)

                    if self.data.get(reform_data[2]):
                        if float(self.data[reform_data[2]][-2].replace(',', '.')) <= float(reform_data[-2].replace(',', '.')):
                            self.data[reform_data[2]] = reform_data
                    else:
                        self.data[reform_data[2]] = reform_data

    def __call__(self, path: str):
        self.main(path=path)
        return self.data


if __name__ == '__main__':
    test_path = '/home/sunprizrak/Изображения/vladimir'
    start = time()
    ocr = Ocr()
    ocr(path=test_path)
    print(f"Время затраченное на работу: {time() - start}")

