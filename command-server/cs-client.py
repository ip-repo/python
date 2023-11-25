import os
import socket
from shutil import get_terminal_size
from colorama import Fore, Back, Style

if __name__ == "__main__":
	HOST = "127.0.0.1"
	PORT = 9001
	LINE = Back.LIGHTBLUE_EX  + "Client" + " " * (get_terminal_size()[0] - 6) + Style.RESET_ALL
	ENDLINE = Back.LIGHTBLUE_EX + (" " * get_terminal_size()[0]) + Style.RESET_ALL
	MIDLINE = Fore.BLUE + ("-" * get_terminal_size()[0]) + Style.RESET_ALL
	LENGTH_PROTOCOL = 4
	os.system("cls")
	with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
		client_socket.connect((HOST, PORT))
		print(LINE, end="")
		print(Fore.GREEN + "Connected to server !" + Style.RESET_ALL)

		while True:
			user_input = input("Enter command:").rstrip()
			if len(user_input) > 9999:
				print(Fore.RED + "Command length cannot be longer then 9999 characters." + Style.RESET_ALL, end="")
				continue
			elif len(user_input) == 0:
				print(Fore.RED + "Command cannot be a empty string." + Style.RESET_ALL, end="")
			else:
				user_input_with_length = str(len(user_input)).zfill(LENGTH_PROTOCOL) + user_input
				client_socket.send(user_input_with_length.encode())
				response_length = int(client_socket.recv(4).decode())
				response = client_socket.recv(response_length).decode().split("|")
				if response[0] == "EXIT":
					print(Fore.RED + "Session is over!" + Style.RESET_ALL)
					print(MIDLINE, end="")
					print(ENDLINE, end="")
					break

				elif response[0] == "UNKOWN":
					print(Fore.RED + "\tUNKOWN COMMAND" + Style.RESET_ALL)

				elif response[0] == "SCREENSHOT":
					if response[1] == "S":
						img_bytes = client_socket.recv(int(response[2]))
						with open("client-screenshot.jpg", "wb") as screen_shot:
							screen_shot.write(img_bytes)
						print("\tScreenshot saved.")
					else:
						print(Fore.RED + "\tscreenshot failed." + Style.RESET_ALL)
				elif response[0] == "DELETE":
					if response[1] == "S":
						print("\tFile deleted.")
					else:

						print(Fore.RED + "\t" + response[2] + Style.RESET_ALL)
				elif response[0] == "DIR":
					if response[1] == "S":
						print(response[2])
					else:
						print(Fore.RED + "\t" + response[2] + Style.RESET_ALL)
				elif response[0] == "COPY":
					if response[1] == "S":
						print("\tFile copied:" + response[2])
					else:
						print(Fore.RED + "\t" + response[2] + Style.RESET_ALL)
				elif response[0] == "EXECUTE":
					if response[1] == "S":
						print("\t" + "Executed")
					else:
						print(Fore.RED + "\t" + response[2] + Style.RESET_ALL)
				
			print(MIDLINE, end="")


#copy_result