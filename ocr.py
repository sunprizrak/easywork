import datetime
import os
from paddleocr import PaddleOCR
import re


class Ocr:
    model_path = os.sep.join(['ch_PP-OCRv4_rec_infer'])

    def reform(self, data: list):
        res = list(map(str.strip, [el[1][0] for el in data[0]]))
        print(f'res: {res}')

        # remove CT
        for el in res:
            if re.fullmatch('ct\d\d[:;]\d\d', el.lower().replace(' ', '')):
                res.remove(el)
                break

        # remove LVL
        for el in res:
            if re.fullmatch('l\D*[.]\d*', el.lower().replace(' ', '')):
                res.remove(el)
                break
            elif re.fullmatch('l\D*\d', el.lower().replace(' ', '')):
                res.remove(el)
                break

        # id and cut profile with x
        for i, el in enumerate(res):
            if re.fullmatch('.{,2}[:;：]\s{0,}\d*', el.lower().replace(' ', '')):
                for symbl in [':', ';', '：']:
                    if symbl in el:
                        res[i] = el.split(symbl)[-1].strip()
                        res = res[i-1:]  # cut profile and x if there
                        break
            elif re.fullmatch('.{,2}[:;]\s{0,}\d*[a-z]{,3}[.,]\d*', el.lower().replace(' ', '')):
                for symbl in [':', ';']:
                    if symbl in el:
                        res[i] = ''.join([ex for ex in el.split(symbl)[-1].split('.')[0] if ex.isdigit()]).strip()
                        res = res[i-1:]  # cut profile and x if there
                        break

        # % to number
        for i, el in enumerate(res):
            if re.fullmatch('%?\d*%?', el.replace(' ', '')):
                res[i] = el.replace('%', '').strip()

        # remove words
        for i, el in enumerate(res[2:]):
            if not el.replace(',', '').isdigit() and not any([let for let in el if let in [';', ':']]):
                res.remove(el)

        # Club
        for i, el in enumerate(res):
            if re.fullmatch('\w{3,}[:;].*', el.lower().replace(' ', '')):
                for symbl in [':', ';']:
                    if symbl in el:
                        res[i] = el.split(symbl)[-1].strip()

        print(len(res))
        print(f'<>: {res}')

        if len(res) < 14:
            res = res[:8]
        else:
            lines = [res[3:7], res[7:11], res[11:]]
            res = res[:3] + lines[0][:2] + [lines[1][0], lines[1][2]] + [lines[2][0]]

        res[-1] = res[-1].replace(',', '')

        res.insert(0, getattr(self, 'path'))

        now = datetime.datetime.now()
        date = now.strftime("%d/%m")
        res.append(date)
        return res

    def main(self, file_path: str):
        setattr(self, 'path', file_path)
        paddle_ocr = PaddleOCR(use_angle_cls=True, show_log=False, Rec_model_dir=self.model_path, use_gpu=False)
        image_data = paddle_ocr.ocr(file_path)
        reform_data = self.reform(image_data)
        print(f'reform_data: {reform_data}')
        print('-------------------------------------------------------------------------------')
        return reform_data

    def __call__(self, path: str):
        return self.main(file_path=path)