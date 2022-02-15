import threading
from client_gui import window, start_home_window, current_client_socket
from client_receive import client_receive

threading.Thread(target=client_receive, args=(current_client_socket,), daemon=True).start()
start_home_window()
window.mainloop()
