------------
file_handler
------------

Code to copy files via ftp or sftp.

file_handler.py contains an interface where you can select your protocol and provide relevant details about the file to be copied. All files will be copied to current directory.

The details are provided via commandline as follows :

python file_handler.py "ftp://username:password@localhost/Downloads/test.txt"
OR
python file_handler.py "sftp://username:password@localhost/Downloads/test.txt"



