# PASSWORD CRACKING PROJECT FOR IT003 - 23521045
- git clone my repo
- If **git** not avaiable, you can download the source code as zip file form.
- Unzip the zip file and open the project using VSCode
- In the VSCode terminal, type the command.
```
python3 password_cracking_tool.py <content>
```
```
--algo ‘bfa’, ‘hb’, ‘da’
Brute force attack, hybrid attack, dicitonary attack (default)
--zipfile Text
--min-length, Int
-min force attack)
Đường dẫn đến file zip cần crack
Default = 1, độ dài tối thiểu của mật khẩu (dùng cho brute
--max- Int length, -max --character- Text set, -cset
Default = 6, độ dài tối đa của mật khẩu (dùng cho brute force attack)
Default = ‘abcdefghijklmnopqrstuvwxyz0123456789’, chứa bộ ký tự của mật khẩu
```
- After that, you can see the result in file tested_password.txt.
- It may take 3 minutes for cracking.
- You can use the files example.zip for cracking.
