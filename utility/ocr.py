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
            if re.fullmatch('.{,2}[:;：]\s{0,}\d*', el.lower()):
                for symbl in [':', ';', '：']:
                    if symbl in el:
                        res[i] = el.split(symbl)[-1].strip()
                        res = res[i-1:]  # cut profile and x if there
                        break
            elif re.fullmatch('.{,2}[:;]\s{0,}\d*[a-z]{,3}[.]\d', el.lower()):
                for symbl in [':', ';']:
                    if symbl in el:
                        res[i] = ''.join([ex for ex in el.split(symbl)[-1].split('.')[0] if ex.isdigit()]).strip()
                        res = res[i-1:]  # cut profile and x if there
                        break

        # % to number
        for i, el in enumerate(res):
            if re.fullmatch('%?\d*%?', el):
                res[i] = el.replace('%', '').strip()

        # remove words
        for i, el in enumerate(res[2:]):
            if not el.replace(',', '').isdigit() and not any([let for let in el if let in [';', ':']]):
                res.remove(el)

        # Club
        for i, el in enumerate(res):
            if re.fullmatch('\w{3,}[:;].*', el.lower()):
                for symbl in [':', ';']:
                    if symbl in el:
                        res[i] = el.split(symbl)[-1].strip()

        if len(res) < 15:
            res = res[:8]
        else:
            lines = [res[3:7], res[7:11], res[11:]]
            res = res[:3] + lines[0][:2] + [lines[1][0], lines[1][2]] + [lines[2][0]]

        res[-1] = res[-1].replace(',', '')

        res.insert(0, path)

        now = datetime.datetime.now()
        date = now.strftime("%d/%m")
        res.append(date)
        return res

    def add_data(self, name, folder=False):
        image_data = getattr(self, 'ocr').ocr(name)

        if folder:
            path = os.path.join(self.path, name)
            reform_data = self.reform(image_data, path)
        else:
            reform_data = self.reform(image_data, self.path)

        print(reform_data)

        if self.data.get(reform_data[2]):
            if int(self.data[reform_data[2]][-2].replace(',', '.')) <= int(reform_data[-2].replace(',', '.')):
                self.data[reform_data[2]] = reform_data
        else:
            self.data[reform_data[2]] = reform_data

    def main(self, path: str):
        setattr(self, 'path', path)
        setattr(self, 'ocr', PaddleOCR(use_angle_cls=True, show_log=False))

        if os.path.isfile(self.path):
            dir_name = os.path.dirname(path)
            file_name = os.path.basename(path)
            os.chdir(path=dir_name)
            self.add_data(name=file_name)
        elif os.path.isdir(self.path):
            os.chdir(path=self.path)
            dir_list = os.listdir(path=self.path)

            for el in dir_list:
                if os.path.isfile(os.path.join(self.path, el)):
                    self.add_data(name=el, folder=True)

    def __call__(self, path: str):
        self.main(path=path)
        return self.data


if __name__ == '__main__':
    test_path = '/home/sunprizrak/Изображения/vladimir'
    start = time()
    ocr = Ocr()
    ocr(path=test_path)
    print(f"Время затраченное на работу: {time() - start}")

