import serial
import requests
import time

# --- CONFIGURAÇÕES OBRIGATÓRIAS ---

# 1. Coloque aqui a sua Porta Serial (encontre na Arduino IDE)
#    Exemplo para Windows: 'COM5'
#    Exemplo para Mac: '/dev/tty.usbmodem14201'
SERIAL_PORT = 'COM6' # Você já configurou esta corretamente

# 2. Coloque aqui a sua "Write API Key" (Chave de Escrita) do ThingSpeak
THINGSPEAK_API_KEY = '6NFPU91FP0YLBFYG'

# --- FIM DAS CONFIGURAÇÕES ---

BAUD_RATE = 9600
THINGSPEAK_URL = 'https://api.thingspeak.com/update'

print("Iniciando a ponte entre Arduino e ThingSpeak...")
print(f"Escutando a porta serial: {SERIAL_PORT}")

try:
    arduino = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=2)
    time.sleep(2) 
except serial.SerialException as e:
    print(f"ERRO: Não foi possível conectar à porta '{SERIAL_PORT}'.")
    print("Verifique se a porta está correta e se o Arduino está conectado.")
    exit()

while True:
    try:
        line = arduino.readline().decode('utf-8').strip()
        
        if line:
            print(f"Recebido do Arduino: {line}")
            
            # --- CORREÇÃO AQUI ---
            # Só tenta processar a linha se ela contiver uma vírgula
            if ',' in line:
                try:
                    temp, humidity = line.split(',')
                    
                    payload = {
                        'api_key': THINGSPEAK_API_KEY,
                        'field1': temp,
                        'field2': humidity
                    }
                    
                    response = requests.get(THINGSPEAK_URL, params=payload)
                    
                    if response.status_code == 200:
                        print(">> Dados enviados para o ThingSpeak com sucesso!")
                    else:
                        print(f">> Falha ao enviar dados. Resposta: {response.text}")

                except ValueError:
                    # Este erro agora é menos provável, mas é bom mantê-lo
                    print(f"Formato de dados inválido recebido: '{line}'")
            else:
                # Informa que a linha foi ignorada
                print(">> Linha ignorada (não contém dados de sensor).")
                
    except KeyboardInterrupt:
        print("\nPrograma interrompido.")
        break
    except Exception as e:
        print(f"Ocorreu um erro: {e}")
        time.sleep(5)

arduino.close()
print("Conexão serial fechada.")