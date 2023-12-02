import socket
import json
import os
# Danh sách tài khoản
users = {"trong": "123", "user2": "pass2", "user3": "pass3"}

# Tập hợp chứa thông tin về các sân đã đặt
san_da_dat = set()

def handle_client(client_socket):
    global san_da_dat

    # Kiểm tra đăng nhập
    username = client_socket.recv(1024).decode()
    password = client_socket.recv(1024).decode()

    if username in users and users[username] == password:
        client_socket.send("truse".encode())

        while True:
            # os.system("cls")
            # Nhận lựa chọn từ client
            choice = client_socket.recv(1024).decode()

            if choice == "thoat":
                break
            elif choice == "datsan":
                # Gửi danh sách sân trống về client
                san_trong = get_san_trong()
                data_to_send = {"san_trong": san_trong}
                client_socket.send(json.dumps(data_to_send).encode())

                # Nhận thông tin về sân và giờ đặt từ client
                data_received = client_socket.recv(1024).decode()
                data = json.loads(data_received)
                chosen_san = data["chosen_san"]
                chosen_gio_dat = data["chosen_gio_dat"]

                # Kiểm tra xem sân đã đặt hay chưa
                if chosen_san in san_trong:
                    # Thêm vào tập hợp sân đã đặt
                    san_da_dat.add((chosen_san, chosen_gio_dat))

                    # Xử lý đặt sân
                    success = True
                else:
                    success = False

                # Gửi kết quả đặt sân về client
                if success:
                    print("Người dùng đặt sân :"+ chosen_san+ " - thời gian:"+chosen_gio_dat)
                    confirm = input("Bạn muốn xác nhận đặt sân thành công (yes/no)? ")
                    if confirm.lower() == "yes":
                        client_socket.send("thành công".encode())
                    else:
        
                       san_da_dat.remove((chosen_san, chosen_gio_dat))
                       fail_message = input("Lý do đặt sân không thành công: ")
                       client_socket.send(f"Đặt sân thất bại, {fail_message}".encode())
                else:
                    client_socket.send("Nhập sai thông tin".encode())
            elif choice == "lichsu":
                # Gửi danh sách sân đã đặt về client
                san_da_dat_info = {"san_da_dat": list(san_da_dat)}
                client_socket.send(json.dumps(san_da_dat_info).encode())
            elif choice == "huydat":
                # Nhận thông tin về sân cần hủy đặt từ client
                chosen_san = client_socket.recv(1024).decode()

                # Kiểm tra xem sân đã đặt hay chưa
                if (chosen_san, chosen_gio_dat) in san_da_dat:
                    # Hủy đặt sân
                    san_da_dat.remove((chosen_san, chosen_gio_dat))
                    result = f"Da huy dat san {chosen_san} vao luc {chosen_gio_dat}"
                else:
                    result = f"San {chosen_san} chua duoc dat, khong the huy."

                # Gửi kết quả hủy đặt sân về client
                client_socket.send(result.encode())
            else:
                client_socket.send("Invalid choice".encode())

    else:
        client_socket.send("Login failed".encode())

    client_socket.close()

def get_san_trong():
    # Trả về danh sách sân còn trống (chưa được đặt)
    san_trong = {"san1", "san2", "san3"} - set([san for san, _ in san_da_dat])
    return ",".join(san_trong)

def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(("127.0.0.1", 8080))
    server.listen(5)

    print("- Lắng nghe các kết nối")

    while True:
        client, addr = server.accept()
        print("- Chấp nhận kếu nối từ : %s:%d" % (addr[0], addr[1]))

        handle_client(client)

if __name__ == "__main__":
    main()
