import socket

ESP_IP = "192.168.0.136"
ESP_PORT = 80

def send_comand(comand):
    
    '''FUNÇÃO PARA ENVIAR COMANDOS PARA O ARDUINO VIA SOCKET
    
        RETORNA CHAR CORRESPONDENTE AO COMANDO ENVIADO PARA O ARDUINO
        
    '''
    
    F_ESP = {
        "None": "P",
        "AVANÇAR": "A",
        "DIREITA": "D",
        "ESQUERDA": "E",
        "PARAR": "P",
        "RECUAR": "R"
    }
    
    try:
        
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            
            sock.settimeout(5)
            sock.connect((ESP_IP, ESP_PORT))
            sock.sendall(F_ESP[comand].encode())
            
    except (socket.error, socket.timeout) as e:
        print(f"Erro ao enviar comando: {e}")