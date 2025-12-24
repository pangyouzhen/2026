#!/usr/bin/python3

import re
import sys

# 以4开头的不支持, 例如430300
# 以8开头的也不支持, 例如832225
if __name__ == '__main__':

    num_in = sys.argv[1]
    num_out = sys.argv[2]

    market = {
        "6": b"\x21",
        "9": b"\x21",
        "5": b"\x21",
        "0": b"\x11",
        "2": b"\x11",
        "3": b"\x11",
        "1": b"\x11",
    }

    with open(num_in, 'r') as f_in:
        nums_text = f_in.read()
        num_re = re.compile(r"\d{6}")
        file_num = num_re.findall(nums_text)

    count = len(file_num)

    with open(num_out, 'wb') as f_out:
        # 写入自选股数量 (8 字节，小端序，假设)
        f_out.write(count.to_bytes(8, byteorder='little'))
        # 写入 NULL 分隔符 (8 字节)
        f_out.write(b'\x00' * 8)
        # 写入 \x07 分隔符 (8 字节)
        f_out.write(b'\x07' * 8)

        for num in file_num:
            try:
                f_out.write(b'\x07' + market[num[0]] + num.encode('ascii'))
            except KeyError as e:
                print("不支持code: %s"%num)

        # 最后一个 \n (根据您提供的十六进制数据，最后有一个 0a)
        if file_num:
            f_out.write(b'\x0a')