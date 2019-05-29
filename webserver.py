import socket #communicating via sockets
import threading #


#declaring the variables that the server needs to know to affect the communication
host = "127.0.0.1"
port = 8080
connection_directory = "Mywebpage"

#Creating a socket in order to access the internet
socket_nadeesha=socket.socket(socket.AF_INET, socket.SOCK_STREAM)

def begin_server():
    #starts the server
    try:
        print("Starting the server on {host}:{port}" +str(host)+":"+str(port))
        socket_nadeesha.bind((host, port))
        print("Started server on port {port}."+str(port))
        listen_to_port()

    except OSError:
        print("Port and/or Host is/are already in use")
        shutdown_server()


def shutdown_server():
    #shuts down the server
    try:
        print("Shutting down the server")
        socket_nadeesha.shutdown(socket.SHUT_RDWR)

    except Exception as Error:
        pass #If the server is already closed

def header_generation(code_of_response, type_of_file):
    #This returns an HTTP header for the given response code and type of file
    header= ""
    if code_of_response == 200:
        header += "HTTP/1.1 200 OK!\n"
        
    elif code_of_response == 404:
        header += "HTTP/1.1 404 Not Found\n"
        
    elif code_of_response == 400:
        header += "HTTP/1.1 400 Bad Request\n"


    if type_of_file == 'htm' or type_of_file == 'html':
        header += 'Content-Type: text/html\n'
        
    elif type_of_file == 'jpg' or type_of_file == 'jpeg':
        header += 'Content-Type: image/jpeg\n'
        
    elif type_of_file == 'png':
        header += 'Content-Type: image/png\n'
        
    elif type_of_file == 'css':
        header += 'Content-Type: text/css\n'
        

    header += 'Connection: close\n\n'
    return header

def listen_to_port():
    socket_nadeesha.listen(6) #listen to the port for the incoming connections(maximum no of invalid connections=6)
    while True:
        (client_connection, client_address) = socket_nadeesha.accept()
        client_connection.settimeout(65)
        threading.Thread(target=request_handling, args=(client_connection,)).start()

def request_handling(client_connection):
    PACKET_SIZE = 1024 #the maximum packet size is set to 1024
    while True:
        try:
            requested_data = client_connection.recv(PACKET_SIZE).decode() #This receives a data packet from a client and decodes it
            if not requested_data: break

        except Exception as e:
            print("Request has timed out" + str(e))
            break
        print(requested_data)

        try:
            requested_file = requested_data.split(' ')[1]

            requested_file = requested_file.split('?')[0]

            if requested_file == "/":
                requested_file = "/index.html"

            path_to_file = connection_directory + requested_file

            type_of_file = requested_file.split('.')[1]

            #load and serve the contents in the file

            file = open((connection_directory+requested_file), 'rb')
            data_responding = file.read()
            file.close()
            print("Requested File : " + path_to_file)
            responding_header = header_generation(200,type_of_file) #type_of_file)

        except IndexError as e:
            print("File Requested")
            responding_header = header_generation(400, '')
            data_responding = b"Malformed request"

        except UnboundLocalError as e:  
            print(e)
            responding_header = header_generation(400, '')
            data_responding = b"Malformed request"

        except FileNotFoundError as e:
            print(e)
            responding_header = header_generation(404,'')
            data_responding = b"<html><body><h2>Error 404 - File Not Found</h2></body></html>"

        response = responding_header.encode()

        response += data_responding

        client_connection.send(response)
        client_connection.close()
        break


begin_server()

            
            

