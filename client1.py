import socket
import json
import os
def main():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(("127.0.0.1", 8080))

    # Nhập thông tin đăng nhập
    username = input("Enter username: ")
    password = input("Enter password: ")

    # Gửi thông tin đăng nhập đến server
    client.send(username.encode())
    client.send(password.encode())

    # Nhận kết quả xác thực
    auth_result = client.recv(1024).decode()
    print(auth_result)

    if auth_result == "truse":
        while True:
            os.system("cls")
            # Hiển thị menu lựa chọn
            print("1. Datsan")
            print("2. Lichsu")
            print("3. Huydat")
            print("4. Thoat")

            choice = input("Enter your choice: ")

            # Gửi lựa chọn đến server
            client.send(choice.encode())

            if choice == "thoat":
                break
            elif choice == "datsan":
                # Nhận và hiển thị danh sách sân trống
                data_received = client.recv(1024).decode()
                san_trong_info = json.loads(data_received)
                print("Danh sách sân trống:", san_trong_info["san_trong"])

                # Cho phép client chọn sân và giờ để đặt
                chosen_san = input("Chon san de dat: ")
                chosen_gio_dat = input("Nhap gio dat: ")
                data_to_send = {"chosen_san": chosen_san, "chosen_gio_dat": chosen_gio_dat}
                client.send(json.dumps(data_to_send).encode())

                # Nhận kết quả đặt sân từ server
                result = client.recv(1024).decode()
                print(result)
            elif choice == "lichsu":
                # Nhận và hiển thị danh sách sân đã đặt
                data_received = client.recv(1024).decode()
                san_da_dat_info = json.loads(data_received)
                print("Danh sách sân đã đặt:", san_da_dat_info["san_da_dat"])
            elif choice == "huydat":
                # Nhập thông tin về sân cần hủy đặt
                chosen_san_to_cancel = input("Nhap san can huy dat: ")
                client.send(chosen_san_to_cancel.encode())

                # Nhận kết quả hủy đặt sân từ server
                result = client.recv(1024).decode()
                print(result)
            else:
                print("Invalid choice")

    client.close()

if __name__ == "__main__":
    main()
