import argparse
import itertools
from multiprocessing import Pool
from zipfile import ZipFile
import math

tested_file = open('tested_password.txt', 'w') # File chứa các password đã thử nghiệm và kết quả đưa ra
hybrid_file = 'hybrid.txt' # Bộ dữ liệu cho hybrid attack
dict = {'a': '4', 'o': '0', 'e': '3', 'g': '9', 'z': '2', 'i': '1', 'A': '4', 'O': '0', 'E': '3', 'Z': '2', 'I': '1'}
def generate_hybrid_passwords(myList, cur = 0):
        res = []
        if cur == len(myList):
            myPassword = ''.join(myList)
            # print(myList)
            res.append(myPassword)
            return res

        res.extend(generate_hybrid_passwords(myList, cur+1))
        if myList[cur] in dict:
            tmp = myList[cur]
            myList[cur] = dict[tmp]
            res.extend(generate_hybrid_passwords(myList, cur+1))
            myList[cur] = tmp

            if myList[cur] == 'a':
                myList[cur] = '@'
                res.extend(generate_hybrid_passwords(myList, cur+1))
                myList[cur] = 'a'

        return res
def crack_passwords_with_hybrid_attack():
        # a, 4, @ / o, 0 / e, 3/ g, 9/ z 2/ i 1/ Một vài cặp ký tự có thể thay đổi cho nhau
        # pass-num, num-pass Một vài dạng password có thể được cải tiến (num có length 0->3) 
        nums = [] # List để chứa các tổ hợp của num
        for num_length in range(2):
            Lim = int(math.pow(10, num_length+1))
            for i in range(Lim):
                s = str(i).zfill(num_length)
                nums.append(s)
        
        nums3 = ['000', '123', '321', '111', '222', '333', '444', '555', '666', '777', '888', '999', '987', '789', '1234', '123456', 'abc', 'xyz']
        nums.extend(nums3)
        
        myValidPassword = []
        with open(hybrid_file, 'r', encoding="latin-1") as dictionary:
            passwords = dictionary.read().splitlines() # List để chứa các tổ hợp của pass
            for password in passwords:
                myList = list(map(str, password))
                extendPassword = generate_hybrid_passwords(myList)
                for newPass in extendPassword:
                    for num in nums:
                        myValidPassword.append(newPass + num)
                        myValidPassword.append(num + newPass)
            
        for password in myValidPassword:
            tested_file.write(password + '\n')

crack_passwords_with_hybrid_attack()
tested_file.close()