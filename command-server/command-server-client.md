# commands server
On this example i have created a server-client script that allow a client to execute commands on on the server and get the command result.<br>

https://github.com/ip-repo/python/assets/123945379/6cdf773e-3c4e-47b4-a8c6-629cb84bbcd2


How to use:
```
git https://github.com/ip-repo/python.git
python -m venv command-venv
command-venv\scripts\activate
pip install pyautogui
pip install pillow
pip install colorama
cd command-server
python cs-server.py #terminal 1
python cs-client.py #terminal 2
```

The commands that the server-side allow are:
1. DIR : list the content of a directory on the server.
2. DELETE : delete a file on server.
3. COPY : copy file to a specific directory on server.
4. EXECUTE : execute a exe program on server.
5. SCREENSHOT : take a screenshot and send it to client.
6. EXIT

And this is how to use them.
```
DIR C:\Users\user\Desktop\images_directory
COPY C:\Users\user\Desktop\images_directory\img06.jpg C:\Users\user\Desktop\images_directory\img078.jpg
DELETE C:\Users\user\Desktop\images_directory\img078.jpg
EXECUTE C:\Windows\notepad.exe
SCREENSHOT
EXIT
```
**note:** The command can be lower or upper case but the space between command and path(if needed) need to exactly 1 and also that path need to be full.

This program use a general **length protocl of 4 bits** and a response string to handle response on the client side for example:
```
client command:EXECUTE C:\Windows\System32\notepad.exe
client send --->0038EXECUTE C:\Windows\System32\notepad.exe
server recive 4 first bits ---> 0038
now the server know the request length to recive : 38
server recive the message: EXECUTE C:\Windows\System32\notepad.exe
server now will check if the command is allowd and path exists.
server will execute the command and send back a response of the result :EXECUTE|S
server will send back the data generated (if needed) or info about the result.

```
The response format is: COMMANDNAME|S/F|DATA|REASON (S=SUCCESS, F=FAIL)<br>
The response will have data or reason only if needed like in the case of SCREENSHOT command that will send the img data.<br>
**note:** On this example the screenshor is sent in one chunk to simplify things but its not always the best way to send images.

