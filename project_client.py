"""
Distributed Systems Project
09.04.2024

Sources used for creation of code:

"""

import socket
import threading
import sqlite3

# Use Server defined parameters for IP, Port, Buffer Size
SERVER_HOST = '127.0.0.1'
SERVER_PORT = 5555
BUFFER_SIZE = 1024

# Receive messages sent to the server
def receive_messages(client_socket):
    while True:
        try:
            message = client_socket.recv(BUFFER_SIZE).decode()
            print(message)
        except Exception as e:
            print(e)
            break

# Send messages to the server
def send_message(client_socket):
    while True:
        message = input()
        # If client types: /quit in console, It will disconnect
        if message == '/quit':
            client_socket.close()
            break
        client_socket.send(message.encode())

# Main function to start the client
if __name__ == "__main__":
    try:
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((SERVER_HOST, SERVER_PORT))
        print("Connected to the server")

        # Prompt user for username and password
        username = input("Enter your username: ")
        password = input("Enter your password: ")
        
        # Send username and password to the server for authentication
        client_socket.send(f"{username},{password}".encode())
        
        # Receive response from the server
        response = client_socket.recv(BUFFER_SIZE).decode()

        if response == "LOGIN":
            print("You are logged in.")
            
        elif response == "REGISTER":
            print("You don't have an account. Please register.")
            while True:
                try:
                    new_username = input("Enter your new username: ")
                    new_password = input("Enter your new password: ")
                    email = input("Enter your email: ")
                    client_socket.send(f"{new_username},{new_password},{email}".encode())
                    register_response = client_socket.recv(BUFFER_SIZE).decode()
                    
                    if register_response == "REGISTER_SUCCESS":
                        print("Registration successful. You can now log in.")
                        break
                    
                    elif register_response == "USERNAME_TAKEN":
                        print("Username already taken. Please choose a different username.")
                        
                except Exception as e:
                    print("An error occurred during registration:", e)
                    break

        # Start threads for sending and receiving messages
        receive_thread = threading.Thread(target=receive_messages, args=(client_socket,))
        send_thread = threading.Thread(target=send_message, args=(client_socket,))
        receive_thread.start()
        send_thread.start()

        receive_thread.join()
        send_thread.join()

        client_socket.close()
    except Exception as e:
        print("Unexpected error occurred:", e)

