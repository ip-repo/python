import socket 
import os
from shutil import get_terminal_size, copy
from pyautogui import screenshot

from glob import glob
from colorama import Fore, Back, Style


def process_client_request(request : str) -> dict:
	"""
	This function get the client request and check if its valid.
	If its valid it will execute the client command and return a dict with the data and result.
	If its not valid it will return a dict with data and the reason why its not valid.
	"""
	splited_request = request.split(" ")
	allowed_commands = ["DIR", "DELETE", "COPY", "EXECUTE", "EXIT", "SCREENSHOT"]
	if len(splited_request) == 1:
		client_command = splited_request[0].upper()
		if client_command == "EXIT":
			return {"COMMAND" : "EXIT", "SUCCESS" : True}
		
		elif client_command == "SCREENSHOT":
			screen_shot_path = r"screenshot-server.jpg"
			screenshot(screen_shot_path)
			if os.path.exists(screen_shot_path):
				with open(screen_shot_path, "rb") as screen_shot:
					screen_shot_bytes = screen_shot.read()
				print("\tscreenshot saved on server.")
				return {"COMMAND" : "SCREENSHOT", "SUCCESS" : True, "DATA" : screen_shot_bytes, "PATH": screen_shot_path}
			else:
				return {"COMMAND" : "SCREENSHOT", "SUCCESS" : False, "REASON" : "UNKOWN ERROR"}
			
		else:
			return{"COMMAND" : "UNKNOWN", "SUCCESS" : False, "REASON" : "UNKNOWN COMMAND"}
	
	else:
		client_command = splited_request[0].upper()
		if client_command in allowed_commands:
			if client_command == "DIR":
				client_command_path = splited_request[1]
				if os.path.exists(client_command_path):
					files_list = glob(client_command_path + "\\*.*")
					if files_list:
						return  {"COMMAND" : "DIR", "SUCCESS" : True, "DATA" :"\t" + "\n\t".join(files_list)}
					else:
						return  {"COMMAND" : "DIR", "SUCCESS" : False, "REASON" : "DIRECTORY FOUND BUT COMMAND FAILED"}
				else:
					return  {"COMMAND" : "DIR", "SUCCESS" : False, "REASON" : "DIRECTORY DO NOT EXISTS"}
		
			elif client_command == "DELETE":
				client_command_path = splited_request[1]
				if os.path.exists(client_command_path):
					os.remove(client_command_path)
					if os.path.exists(client_command_path):
						return {"COMMAND" : "DELETE", "SUCCESS" : False, "REASON" :"FOUND FILE TO DELETE BUT SOMTHING WENT WRONG"}
					else:
						return {"COMMAND" : "DELETE", "SUCCESS" : True}
				else:
					return {"COMMAND" : "DELETE", "SUCCESS" : False, "REASON" :"COULD NOT FIND THE FILE TO DELETE "}
				
			elif client_command == "COPY":
				if len(splited_request) == 3:
					client_command_path = splited_request[1]
					if os.path.exists(client_command_path):
						copy_to_path = r"{}".format(splited_request[2])
						if "\\" not in copy_to_path:
							return {"COMMAND" : "COPY", "SUCCESS" : False, "REASON" : "MAKE SURE TO ENTER A FULL PATH"}
						else:
							if os.path.exists("\\".join(copy_to_path.split("\\")[:-1])):
								copy_result = copy(r"{}".format(client_command_path), r"{}".format(copy_to_path))
								return {"COMMAND" : "COPY", "SUCCESS" : True, "DATA" : copy_result}
							else:
								print("c3")
								return {"COMMAND" : "COPY", "SUCCESS" : False, "REASON" : "COULD NOT FIND THE PATH TO COPY TO"}
					else:
						return{"COMMAND" : "COPY", "SUCCESS" : False, "REASON" : "COULD NOT FIND FILE TO COPY"}
				else:
					return{"COMMAND" : "COPY", "SUCCESS" : False, "REASON" : "COPY COMMAND NOT USED THE RIGHT WAY"}
			
			elif client_command == "EXECUTE":
				client_command_path = splited_request[1]
				if os.path.exists(client_command_path):
					execute_result = os.system(r"{}".format(client_command_path))
					if execute_result == 0:
						return {"COMMAND" : "EXECUTE", "SUCCESS" : True}
					else:
						return {"COMMAND" : "EXECUTE", "SUCCESS" : False, "REASON" : "FOUND PATH BUT SOMETHING WENT WRONG"}
				else:
					return {"COMMAND" : "EXECUTE", "SUCCESS" : False, "REASON" :"PATH NOT FOUND"}
			
		else:
			return{"COMMAND" : "UNKNOWN", "SUCCESS" : False, "REASON" : "UNKOWN COMMAND"}
		...
	
def send_server_response(processed_data :dict, client_socket :socket.socket):
	"""
	This function get a dict with the client request result and then send it 
	back to the client.
	"""
	command = processed_data["COMMAND"]
	if command == "EXIT":
		response = "EXIT"
		response = str(len(response)).zfill(4) + response
		client_socket.send(response.encode())
		return command
	
	elif command == "DELETE":
		success = processed_data["SUCCESS"]
		if success:
			response = "DELETE|S"
			response = str(len(response)).zfill(4) + response
			client_socket.send(response.encode())
			return "DELETE|S"
		else:
			response = "DELETE|F|" + processed_data["REASON"]
			response = str(len(response)).zfill(4) + response
			client_socket.send(response.encode())
			return "DELETE|F"
	
	elif command == "COPY":
		success = processed_data["SUCCESS"]
		if success:
			response = "COPY|S|" + processed_data["DATA"]
			response = str(len(response)).zfill(4) + response
			client_socket.send(response.encode())
			return "COPY|S"
		else:
			response = "COPY|F|" + processed_data["REASON"]
			response = str(len(response)).zfill(4) + response
			client_socket.send(response.encode())
			return "COPY|F"
	
	elif command == "EXECUTE":
		success = processed_data["SUCCESS"]
		if success:
			response = "EXECUTE|S"
			response = str(len(response)).zfill(4) + response
			client_socket.send(response.encode())
			return "EXECUTE|S"
		else:
			response = "EXECUTE|F|" + processed_data["REASON"]
			response = str(len(response)).zfill(4) + response
			client_socket.send(response.encode())
			return "EXECUTE|F"
		
	elif command == "SCREENSHOT":
		success = processed_data["SUCCESS"]
		if success :
			response = "SCREENSHOT|S|" + str(len(processed_data["DATA"]))
			response = str(len(response)).zfill(4) + response
			client_socket.send(response.encode())
			client_socket.send(processed_data["DATA"])
			return "SCREENSHOT|S"
		else:
			response = "SCREENSHOT|F|" + processed_data["REASON"]
			response = str(len(response)).zfill(4) + response
			client_socket.send(response.encode())
			return "SCREENSHOT|F"
		
	elif command == "DIR":
		success = processed_data["SUCCESS"]
		if success:
			response = "DIR|S|" + processed_data["DATA"]
			response = str(len(response)).zfill(4) + response
			client_socket.send(response.encode())
			return "DIR|S"
			
		else:
			response = "DIR|F|"  + processed_data["REASON"]
			response = str(len(response)).zfill(4) + response
			client_socket.send(response.encode())
			return "DIR|F"
		
	else:
		response = "UNKOWN|" + processed_data["REASON"]
		response = str(len(response)).zfill(4) + response
		client_socket.send(response.encode())
		return "UNKOWN"
			

	
	...

if __name__ == "__main__":
	LINE = Back.LIGHTBLUE_EX  + "Server" + " " * (get_terminal_size()[0] - 6) + Style.RESET_ALL
	ENDLINE = Back.LIGHTBLUE_EX + (" " * get_terminal_size()[0]) + Style.RESET_ALL
	MIDLINE = Fore.BLUE + ("-" * get_terminal_size()[0]) + Style.RESET_ALL
	LENGTH_PROTOCOL = 4
	HOST = "127.0.0.1"
	PORT = 9001

	os.system("cls")
	with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
		print(LINE, end="")
		print(Fore.RED + "Waiting for client to connect ..." + Style.RESET_ALL)
		server_socket.bind((HOST, PORT))
		server_socket.listen()
		client_socket, client_address = server_socket.accept()
		with client_socket:
			os.system("cls")
			print(LINE, end="")
			print(Fore.GREEN + "Client is now connected !" + Style.RESET_ALL)
			while True:
				client_request_length = int(client_socket.recv(LENGTH_PROTOCOL).decode())
				client_request = client_socket.recv(client_request_length).decode()
				print("Client request:" + client_request)
				processed_data = process_client_request(request=client_request)
				print("\t" + "COMMAND: " + processed_data["COMMAND"] +"\n\tSUCCESS: " + str(processed_data["SUCCESS"]) + "\n" + MIDLINE)
				#print(MIDLINE, end="")
				command_used = send_server_response(processed_data=processed_data, client_socket=client_socket)
				if command_used == "EXIT":
					print(Fore.RED + "Session is over!" + Style.RESET_ALL)
					print(ENDLINE, end="")
					break
				else:
					continue
				
				

	
			