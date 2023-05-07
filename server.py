import socket
import threading
import json

# Tin nhắn
host = 'localhost'
port = 5000
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((host, port))
server_socket.listen(1)
print(f"Đang lắng nghe từ {host}:{port}")

clients = []
client_names = []
def handle_client(client_conn, client_addr):
    login_message = client_conn.recv(1024).decode()
    try:
        # Giải mã file
        message_data = json.loads(login_message)
        username = message_data.get("user")

        # Thêm client vào danh sách clients và client_names
        clients.append(client_conn)
        client_names.append((client_addr[0], username))
        client_index = len(clients) - 1

        print('Client connected:', client_addr, '+', username)

    except json.JSONDecodeError as e:
        print(f'{e}')
        client_conn.close()
        return
    connect_mes = client_conn.recv(1024).decode()
    original_connect_name = json.loads(connect_mes).get('connect')

    while True:

        message = client_conn.recv(102400000)
        try:
            message_str = message.decode('utf-8')
        except UnicodeDecodeError:
            message_str = None
        if message_str:
            sender_name = client_names[client_index][1]
            try:
                # Thêm tên người gửi vào tin nhắn
                message_with_sender = f"{sender_name}:{message_str}"

                # Gửi tin nhắn đến client B
                mes_data = json.loads(connect_mes)
                connect_name  = mes_data.get('connect')
                print(f'{sender_name} đã gửi tin nhắn đến {connect_name} ')
                for i, (addr, name) in enumerate(client_names):
                    if clients[i] != client_conn and name == connect_name:
                        try:
                            clients[i].sendall(message_with_sender.encode('utf-8'))
                        except ConnectionResetError:
                            print('Đóng kết nối : ', client_addr)
                            break
                # Kiểm tra nếu có yêu cầu thay đổi người nhận tin nhắn
                if connect_name != original_connect_name:
                    connect_mes = json.dumps({'connect': connect_name})
                    original_connect_name = connect_name

            except UnicodeDecodeError as e:
                print(f"{e}")
            except ConnectionResetError:
                # Nếu không nhận được tin nhắn nữa, đóng kết nối với client
                client_conn.close()
                clients.remove(client_conn)
                client_names.pop(client_index)
                break
        else:
            if message:
                sender_name = client_names[client_index][1]
                print('Chiều dài dữ liệu message nhận từ client: ',len(message))
                img = b''
                a = 0
                while True:
                    try:
                        data = message
                        img += data
                        a += len(message)
                        if len(img) == a:
                            break
                        print(len(img))
                    except ConnectionResetError:
                        print(f"Kết nối với {client_addr[0]}:{client_addr[1]} đã bị đóng")
                        break
                    except TimeoutError:
                        break
                    if not message:
                        break

                print('Chuỗi sau khi thoát vòng while: ',len(img))

                mes_data = json.loads(connect_mes)
                connect_name = mes_data.get('connect')
                # Gửi tin nhắn đến client B
                for i, (addr, name) in enumerate(client_names):
                    if name == connect_name and clients[i] != client_conn:
                        try:
                            clients[i].sendall(img)
                        except ConnectionResetError:
                            print('Đóng kết nối : ', client_addr)
                            break
                print('đã gửi thành công')
                # Kiểm tra nếu có yêu cầu thay đổi người nhận tin nhắn
                if connect_name != original_connect_name:
                    connect_mes = json.dumps({'connect': connect_name})
                    original_connect_name = connect_name

            else:
                client_conn.close()
                clients.remove(client_conn)
if __name__ == '__main__':
    while True:
        client_conn, client_addr = server_socket.accept()
        threading.Thread(target=handle_client, args=(client_conn, client_addr)).start()