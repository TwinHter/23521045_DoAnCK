import argparse
import itertools
from zipfile import ZipFile
import math

# Bộ password cho dictionary attack.
dictionary_file = 'dictionary.txt'
# Bộ dữ liệu thô cho hybrid attack .
hybrid_file = 'hybrid.txt' 
# File chứa các password đã thử nghiệm và kết quả đưa ra.
tested_file = open('tested_password.txt', 'w') 
class PasswordCracker:
    def __init__(self, zip_file):
        self.matched_password = None # Password chính xác
        self.zip_file = zip_file # File zip cần được xử lý
        self.total_passwords = 0 # Số password được thử nghiệm
        self.dict = {'a': '4', 'o': '0', 'e': '3', 'g': '9', 'z': '2', 'i': '1', 'A': '4', 'O': '0', 'E': '3', 'Z': '2', 'I': '1'} # Bộ ký tự thay thế dùng cho hybrid attack
        self.limit = 100000000 # Số lần thử password tối đa

    # Sinh password cho bruteforce attack.
    def generate_passwords(self, min_length, max_length, character_set): 
        # List để lưu những password khả thi
        passwords = [] 
        # Hàm để thực hiện sinh các tổ hợp thoả mãn min_length < password_length < max_length với bộ ký tự thuộc character_set
        for length in range(min_length, max_length + 1): 
            for combination in itertools.product(character_set, repeat=length):
                password = ''.join(combination)
                passwords.append(password)
        return passwords
    
    # Sinh password cho hybrid attack.
    def generate_hybrid_passwords(self, myList, cur = 0):  
        # List trả về
        res = []
        # Điều kiện dừng của đệ quy
        if cur == len(myList): 
            myPassword = ''.join(myList)
            # print(myList)
            res.append(myPassword)
            return res

        # Không thay đổi ký tự hiện tại
        res.extend(self.generate_hybrid_passwords(myList, cur+1)) 
        
        # Nếu ký tự hiện tại thuộc self.dict thì tiến hành thay đổi
        if myList[cur] in self.dict:
            tmp = myList[cur]
            myList[cur] = self.dict[tmp]
            res.extend(self.generate_hybrid_passwords(myList, cur+1)) 
            myList[cur] = tmp

            # Trường hợp đặc biệt với ký tự 'a'
            if myList[cur] == 'a':
                myList[cur] = '@'
                res.extend(self.generate_hybrid_passwords(myList, cur+1)) 
                myList[cur] = 'a'
        
        return res
    
    # Cracking với bộ password đã được sinh.
    def cracking(self, myPassword): 
        # Lấy từng xâu trong list để test 
        for password in myPassword: 
            self.total_passwords += 1
            tested_file.write(password + '\n')
            # Tiến hành test password
            try:
                with ZipFile(self.zip_file) as zipObj: 
                    zipObj.extractall(pwd=bytes(password, 'utf-8'))
                    self.matched_password = password
                    break
            except RuntimeError as e:
                continue

    # Thuật toán Bruteforce Attack.
    def crack_passwords_with_brute_force(self, min_length, max_length, character_set): 
        tested_file.write('Cracking with brute force attack \n')
        
        # Tính toán trước số lượng password sẽ phải sinh
        maximumGeneratePassword = 0
        for i in range(min_length, max_length+1):
            maximumGeneratePassword += int(math.pow(len(character_set), i))
        # Dừng thuật toán khi thấy số lượng tìm kiếm quá lớn
        if maximumGeneratePassword > self.limit and self.limit != -1:
            tested_file.write('Cannot crack because take too much time\n')
            tested_file.write(f'Expected password have to test: {maximumGeneratePassword}\n')
            exit()

        passwords = self.generate_passwords(min_length, max_length, character_set) # Sinh ra một list bao gôm các password thoả mãn yêu cầu được truyền vào
        self.cracking(passwords)     

    # Thuật toán cho dictionary attack.
    def crack_passwords_with_dictionary(self): 
        tested_file.write('Cracking with dictionary attack \n')
        # Mở file dictionary để làm việc
        with open(dictionary_file, 'r', encoding="latin-1") as dictionary: 
            # Đưa các password từ file dictionary.txt vào list passwords và xử lý
            passwords = dictionary.read().splitlines() 
            self.cracking(passwords)

    # Thuật toán cho hybrid attack.
    def crack_passwords_with_hybrid_attack(self): 
        tested_file.write('Cracking with hybrid attack \n')
        
        # List để chứa các tổ hợp của nums .
        nums = [] 
        for num_length in range(2):
            Lim = int(math.pow(10, num_length+1))
            for i in range(Lim):
                s = str(i).zfill(num_length)
                nums.append(s)
        
        nums3 = ['', '000', '123', '321', '111', '222', '333', '444', '555', '666', '777', '888', '999', '987', '789', '1234', '123456', 'abc', 'xyz']
        nums.extend(nums3)
        
        # List chứa các password khả thi.
        myValidPassword = [] 
        with open(hybrid_file, 'r', encoding="latin-1") as dictionary:
            passwords = dictionary.read().splitlines() 
            for password in passwords:
                myList = list(map(str, password))
                # List chứa các dạng lai của pass đang xét.
                extendPassword = self.generate_hybrid_passwords(myList)

                # Tiến hành tạo các password dạng num + pass hay pass + num.
                for newPass in extendPassword:
                    for num in nums:
                        myValidPassword.append(newPass + num)
                        myValidPassword.append(num + newPass)
            
        self.cracking(myValidPassword)
                        
    # Đưa ra kết luận cuối cùng.
    def print_statistics(self): 
        tested_file.write(f"Total Number of Passwords Tried: {self.total_passwords}\n")
        if self.matched_password:
            tested_file.write(f"Password Cracked! Password: {self.matched_password}\n")
        else:
            tested_file.write("Password Failed.\n")


def main():
    # Cài đặt môi trường và tiện ích cho tool.

    # Mô tả tool
    parser = argparse.ArgumentParser(description='Password cracking tool of Dang Nguyen - TWINHTER')
    # Chọn 1 trong 3 loại cracking gồm brute forces attack, dictionary attack và hybrid attack, default = dictionary attack.
    parser.add_argument('--algo',
                    default='da',
                    const='da',
                    nargs='?',
                    choices=['bfa', 'da', 'hb'],
                    help='brute force attack, dictionary attack or hybrid attack') 
    #minimum length of password
    parser.add_argument('-min', '--min-length', type=int, default=1, help='Minimum password length for brute force attack') 
    # maximum length of password
    parser.add_argument('-max', '--max-length', type=int, default=6, help='Maximum password length for brute force attack') 

    # Bộ ký tự cho bẻ khoá bruteforce - characterset
    parser.add_argument('-cset', '--character-set', default='abcdefghijklmnopqrstuvwxyz0123456789',
                        help='Character set for brute force attack') 
    parser.add_argument('--zipfile', type=str, help = 'Zip file to crack') # Đường dẫn của zip file cần được bẻ khoá

    args = parser.parse_args()

    cracker = PasswordCracker(args.zipfile)
    if args.algo == 'bfa':
        cracker.crack_passwords_with_brute_force(args.min_length, args.max_length, args.character_set) # Crack bằng brute force attack
    elif args.algo == 'da':
        cracker.crack_passwords_with_dictionary() # Crack bằng dictionary attack
    else:
        cracker.crack_passwords_with_hybrid_attack() # Crack bằng hybrid attack

    cracker.print_statistics() # in ra kết luận
    tested_file.close() # Đóng file kết quả

if __name__ == '__main__':
    main()