# PASSWORD CRACKING PROJECT FOR IT003 - 23521045
- git clone my repo
- If **git** not avaiable, you can download the source code as zip file form.
- Unzip the zip file and open the project using VSCode
- In the VSCode terminal, type the command.
```
python3 password_cracking_tool.py <content>
```
```
<content> : 
--algo ‘bfa’, ‘hb’, ‘da’              <Brute force attack, hybrid attack, dicitonary attack (default)>
--zipfile Text -> text                <Path to zip file to crack>
--min-length, min -> int              <Default = 1, minumum length of password for brute force attack>
--max-lenth, -max -> int              <Default = 6, maximin length of password for brute force attack>
--character-set, -cset -> text        <Default = 'abcdefghijklmnopqrstuvwxyz0123456789, Character set for bruteforce attack>
```
- After that, you can see the result in file tested_password.txt.
- It may take 3 minutes for cracking.
- You can use the files example.zip for cracking.
