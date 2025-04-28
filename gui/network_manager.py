import socket
import threading
import json
import pickle
import time

class NetworkManager:
    def __init__(self, is_server=False, host='localhost', port=5000):
        self.is_server = is_server
        self.host = host
        self.port = port
        self.socket = None
        self.connection = None
        self.address = None
        self.callback = None
        self.running = True
        self.server_ready = False

    @staticmethod
    def get_local_ip():
        try:
            # Tạo socket để kết nối với Google DNS
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80))
            local_ip = s.getsockname()[0]
            s.close()
            return local_ip
        except Exception:
            # Nếu không kết nối được, lấy IP từ hostname
            return socket.gethostbyname(socket.gethostname())

    def start_server(self):
        try:
            # Lấy địa chỉ IP của máy
            local_ip = self.get_local_ip()
            print(f"Starting server on IP: {local_ip}:{self.port}")
            
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.socket.bind(('0.0.0.0', self.port))  # Lắng nghe trên tất cả các interface
            self.socket.listen(1)
            print(f"Server is now listening for connections on {local_ip}:{self.port}")
            
            # Chấp nhận kết nối trong một thread riêng
            accept_thread = threading.Thread(target=self._accept_connection)
            accept_thread.daemon = True
            accept_thread.start()
            
            # Đánh dấu server đã sẵn sàng
            self.server_ready = True
            return local_ip  # Trả về IP của máy chủ
        except Exception as e:
            print(f"Failed to start server: {e}")
            self.close()
            return None

    def connect_to_server(self):
        try:
            print(f"Attempting to connect to server at {self.host}:{self.port}")
            
            # Kiểm tra xem server có đang chạy không
            test_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            test_socket.settimeout(5)  # Tăng timeout lên 5 giây
            result = test_socket.connect_ex((self.host, self.port))
            test_socket.close()
            
            if result != 0:
                print(f"Server is not running on {self.host}:{self.port}")
                print("Please make sure the server is running and the IP address is correct")
                return False
                
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.settimeout(5)  # Tăng timeout cho socket chính
            self.socket.connect((self.host, self.port))
            print(f"Successfully connected to server at {self.host}:{self.port}")
            
            # Bắt đầu lắng nghe tin nhắn trong một thread riêng
            receive_thread = threading.Thread(target=self._receive_messages)
            receive_thread.daemon = True
            receive_thread.start()
            return True
        except socket.timeout:
            print(f"Connection timed out. Server may be busy or not responding")
            return False
        except Exception as e:
            print(f"Failed to connect: {e}")
            self.close()
            return False

    def _accept_connection(self):
        while self.running:
            try:
                if self.socket:
                    print("Waiting for client connection...")
                    self.connection, self.address = self.socket.accept()
                    print(f"Accepted connection from {self.address}")
                    
                    # Bắt đầu lắng nghe tin nhắn từ client
                    receive_thread = threading.Thread(target=self._receive_messages)
                    receive_thread.daemon = True
                    receive_thread.start()
                    break
            except Exception as e:
                if self.running:
                    print(f"Error accepting connection: {e}")
                time.sleep(0.1)

    def _receive_messages(self):
        while self.running:
            try:
                if self.is_server and self.connection:
                    data = self.connection.recv(4096)
                elif not self.is_server and self.socket:
                    data = self.socket.recv(4096)
                else:
                    break

                if not data:
                    print("Connection closed by remote host")
                    break
                
                try:
                    message = pickle.loads(data)
                    print(f"Received message: {message}")
                    if self.callback:
                        self.callback(message)
                except Exception as e:
                    print(f"Error decoding message: {e}")
                    continue
            except socket.timeout:
                print("Socket timeout while receiving message")
                continue
            except Exception as e:
                if self.running:
                    print(f"Error receiving message: {e}")
                break

    def send_message(self, message):
        try:
            print(f"Sending message: {message}")
            if self.is_server and self.connection:
                self.connection.send(pickle.dumps(message))
            elif not self.is_server and self.socket:
                self.socket.send(pickle.dumps(message))
            print("Message sent successfully")
        except Exception as e:
            print(f"Error sending message: {e}")

    def set_callback(self, callback):
        self.callback = callback

    def close(self):
        self.running = False
        try:
            if self.connection:
                self.connection.close()
            if self.socket:
                self.socket.close()
        except Exception as e:
            print(f"Error closing connection: {e}")
        finally:
            self.connection = None
            self.socket = None 