from flask import Flask, render_template, request, jsonifyfrom flask import Flask, render_template, request, jsonify

import openaiimport openai

import osimport os

from dotenv import load_dotenvfrom dotenv import load_dotenv

import timeimport time

import speedtestimport speedtest

import subprocessimport subprocess

import reimport re

import requestsimport requests

import psutil  # Importar psutil para monitorear el uso del ancho de bandaimport psutil  # Importar psutil para monitorear el uso del ancho de banda

import plotly.express as pximport plotly.express as px

import plotly.io as pioimport plotly.io as pio

import nmap  # Biblioteca para interactuar con nmapimport nmap  # Biblioteca para interactuar con nmap

from scapy.all import ARP, Ether, srp, IP, TCP, sr1from scapy.all import ARP, Ether, srp, IP, TCP, sr1

from flask_sqlalchemy import SQLAlchemyfrom flask_sqlalchemy import SQLAlchemy

from flask import Flask, render_template, request, redirect, url_forfrom flask import Flask, render_template, request, redirect, url_for

from flask_sqlalchemy import SQLAlchemyfrom flask_sqlalchemy import SQLAlchemy



# Cargar variables de entorno# Cargar variables de entorno

load_dotenv()load_dotenv()



app = Flask(__name__)app = Flask(__name__)





# Configuración de la base de datos (SQLite en este caso)# Configuración de la base de datos (SQLite en este caso)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///testimonials.db'app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///testimonials.db'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = Falseapp.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False



# Crear la instancia de SQLAlchemy# Crear la instancia de SQLAlchemy

db = SQLAlchemy(app)db = SQLAlchemy(app)





# Configura tu clave API de OpenAI desde variable de entorno# Configura tu clave API de OpenAI desde variable de entorno

openai.api_key = os.getenv('OPENAI_API_KEY')openai.api_key = os.getenv('OPENAI_API_KEY')



# NOTA: El resto del código de tu aplicación va aquí# Función para clasificar métricas

# Por seguridad, solo incluyo las partes principales# Función para categorizar las métricas de velocidad, latencia y conexiones

# Puedes agregar el resto de tus funciones y rutasdef categorize_metric(value, thresholds, labels):

    """Categoriza una métrica dada en función de los umbrales y las etiquetas proporcionadas."""

if __name__ == '__main__':    for threshold, label in zip(thresholds, labels):

    # Crear las tablas de la base de datos        if value <= threshold:

    with app.app_context():            return label

        db.create_all()    return labels[-1]

    # Función para realizar el análisis de red

    app.run(debug=True, host='0.0.0.0', port=5000)# Función para realizar el análisis de red
def analyze_network():
    """Analiza la red incluyendo velocidad, latencia, ubicación, conexiones activas e ISP."""
    try:
        # Inicializa Speedtest
        test = speedtest.Speedtest()
        test.get_best_server()
        
        # Mide la latencia inicial en reposo
        latency_idle = test.results.ping  # ms

        # Mide el tiempo de descarga
        start_download = time.time()
        download_speed = test.download() / 1_000_000  # Mbps
        end_download = time.time()
        download_latency = round((end_download - start_download) * 1000, 2)  # ms

        # Mide el tiempo de subida
        start_upload = time.time()
        upload_speed = test.upload() / 1_000_000  # Mbps
        end_upload = time.time()
        upload_latency = round((end_upload - start_upload) * 1000, 2)  # ms

        # Obtener información de pérdida de paquetes
        packet_loss_data = get_packet_loss()  # Aquí se obtiene la pérdida de paquetes

        # Obtener conexiones activas
        try:
            result = subprocess.run(['netstat', '-an'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            
            # Contadores de los estados de las conexiones
            established_count = len(re.findall(r'\sESTABLISHED', result.stdout))
            listen_count = len(re.findall(r'\sLISTEN', result.stdout))
            time_wait_count = len(re.findall(r'\sTIME-WAIT', result.stdout))
            syn_sent_count = len(re.findall(r'\sSYN_SENT', result.stdout))
            syn_received_count = len(re.findall(r'\sSYN_RECEIVED', result.stdout))
            fin_wait_1_count = len(re.findall(r'\sFIN_WAIT_1', result.stdout))
            fin_wait_2_count = len(re.findall(r'\sFIN_WAIT_2', result.stdout))
            close_wait_count = len(re.findall(r'\sCLOSE_WAIT', result.stdout))
            closing_count = len(re.findall(r'\sCLOSING', result.stdout))
            last_ack_count = len(re.findall(r'\sLAST_ACK', result.stdout))
            closed_count = len(re.findall(r'\sCLOSED', result.stdout))
            
        except Exception:
            established_count = listen_count = time_wait_count = syn_sent_count = syn_received_count = fin_wait_1_count = fin_wait_2_count = close_wait_count = closing_count = last_ack_count = closed_count = "No disponible"

        # Obtener datos de ubicación e ISP
        try:
            response = requests.get("https://ipinfo.io/json")
            if response.status_code == 200:
                ip_data = response.json()
                location = f"{ip_data.get('city', 'Desconocido')}, {ip_data.get('region', 'Desconocido')}, {ip_data.get('country', 'Desconocido')}"
                lat, lon = ip_data.get('loc', '0,0').split(',')
                isp = ip_data.get("org", "Proveedor desconocido")
            else:
                location, lat, lon, isp = "No disponible", "0", "0", "No disponible"
        except Exception:
            location, lat, lon, isp = "Error al obtener datos", "0", "0", "Error al obtener datos"

        # Clasificaciones
        download_description = categorize_metric(
            download_speed, [2, 10, 25],
            ["Muy Mala", "Deficiente", "Aceptable", "Buena"]
        )
        upload_description = categorize_metric(
            upload_speed, [1, 3, 10],
            ["Muy Mala", "Deficiente", "Aceptable", "Buena"]
        )
        latency_description = categorize_metric(
            latency_idle, [20, 50, 100],
            ["Buena", "Aceptable", "Deficiente", "Muy Mala"]
        )
        connections_description = (
            "No disponible" if isinstance(established_count, str) else
            categorize_metric(established_count, [50, 200], ["Buena/Estable", "Aceptable", "Alta/Congestionada"])
        )

        # Timestamp
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

        return {
            "download_speed": round(download_speed, 2),
            "download_description": download_description,
            "upload_speed": round(upload_speed, 2),
            "upload_description": upload_description,
            "idle_latency": round(latency_idle, 2),
            "download_latency": download_latency,
            "upload_latency": upload_latency,
            "latency_description": latency_description,
            "established_count": established_count,
            "listen_count": listen_count,
            "time_wait_count": time_wait_count,
            "syn_sent_count": syn_sent_count,
            "syn_received_count": syn_received_count,
            "fin_wait_1_count": fin_wait_1_count,
            "fin_wait_2_count": fin_wait_2_count,
            "close_wait_count": close_wait_count,
            "closing_count": closing_count,
            "last_ack_count": last_ack_count,
            "closed_count": closed_count,
            "connections_description": connections_description,
            "location": location,
            "latitude": lat,
            "longitude": lon,
            "isp": isp,
            "timestamp": timestamp,
            "packet_loss_data": packet_loss_data,  # Aquí se agrega la pérdida de paquetes
            "status": "Estable" if download_speed > 10 else "Inestable"
        }

    except Exception as e:
        return {
            "error": str(e),
            "status": "Disconnected",
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
        }
      
        
# Función para simular errores en la red
def simulate_network_errors(error_type):
    """Simula errores de red según el tipo seleccionado."""
    simulation_result = analyze_network()  # Usa la función existente como base
    if "error" in simulation_result:
        return simulation_result  # Retorna error si el análisis básico falla

    # Simulaciones según el tipo de error
    if error_type == "high_latency":
        simulation_result["idle_latency"] += 500  # Aumenta la latencia en ms
        simulation_result["latency_description"] = "Muy Alta (Simulada)"
    elif error_type == "low_speed":
        simulation_result["download_speed"] = max(0.5, simulation_result["download_speed"] * 0.1)
        simulation_result["upload_speed"] = max(0.2, simulation_result["upload_speed"] * 0.1)
        simulation_result["download_description"] = "Muy Baja (Simulada)"
        simulation_result["upload_description"] = "Muy Baja (Simulada)"
    elif error_type == "packet_loss":
        simulation_result["active_connections"] = "No disponible (Pérdida de paquetes simulada)"
        simulation_result["connections_description"] = "Problema de conectividad (Simulado)"
    else:
        return {"error": "Tipo de error no soportado"}

    simulation_result["status"] = "Simulación de Error"
    return simulation_result

# Función para obtener el consumo de ancho de banda por dispositivo
def analyze_bandwidth():
    """Obtiene el consumo de ancho de banda por dispositivo en la red."""
    network_info = psutil.net_io_counters(pernic=True)  # Obtiene información de red por interfaz de red
    bandwidth_usage = {}

    for interface, stats in network_info.items():
        # El campo stats.bytes_sent y stats.bytes_recv nos dan el consumo en bytes enviados y recibidos
        bandwidth_usage[interface] = {
            'bytes_sent': stats.bytes_sent / 1_000_000,  # Convertimos a MB
            'bytes_recv': stats.bytes_recv / 1_000_000,  # Convertimos a MB
        }
    
    # Ordenar las interfaces de mayor a menor consumo de ancho de banda recibido (bytes_recv)
    sorted_bandwidth_usage = sorted(bandwidth_usage.items(), key=lambda x: x[1]['bytes_recv'], reverse=True)

    return sorted_bandwidth_usage

# Rutas existentes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

# Ruta para el análisis
@app.route('/analisis')
def analisis():
    # Llamar a la función de análisis de red
    network_data = analyze_network()

    # Si el análisis tiene un error, se retorna el mensaje de error
    if "error" in network_data:
        return render_template('analisis.html', error=network_data["error"])

    # Datos para las gráficas (puedes reemplazar con los datos reales)
    download_speed = [network_data['download_speed'], 20, 15, 30, 10]  # Velocidad de descarga en Mbps
    latency = [network_data['idle_latency'], 60, 50, 45, 55]  # Latencia en ms
    time = ['1', '2', '3', '4', '5']  # Tiempo (puede ser horas, días, etc.)

    # Crear un gráfico para la velocidad de descarga
    download_speed_fig = px.line(x=time, y=download_speed, labels={'x': 'Tiempo', 'y': 'Velocidad de Descarga (Mbps)'}, title='Historial de Velocidad de Descarga')

    # Crear un gráfico para la latencia
    latency_fig = px.line(x=time, y=latency, labels={'x': 'Tiempo', 'y': 'Latencia (ms)'}, title='Historial de Latencia')

    # Convertir las gráficas a HTML para incluirlas en el template
    download_speed_graph = pio.to_html(download_speed_fig, full_html=False)
    latency_graph = pio.to_html(latency_fig, full_html=False)

    return render_template('analisis.html', 
                           download_speed_graph=download_speed_graph, 
                           latency_graph=latency_graph, 
                           network_data=network_data)
    

def scan_local_network(network="192.168.1.0/24"):
    """Escanea dispositivos y servicios activos en la red local utilizando scapy."""
    try:
        # Escaneo ARP para detectar dispositivos activos
        arp_request = ARP(pdst=network)
        ether = Ether(dst="ff:ff:ff:ff:ff:ff")
        packet = ether / arp_request
        answered_list = srp(packet, timeout=2, verbose=0)[0]

        devices = []
        for sent, received in answered_list:
            device_info = {
                "ip": received.psrc,
                "mac": received.hwsrc,
                "services": []  # Servicios serán detectados en un paso posterior
            }

            # Escaneo de servicios (puertos comunes)
            common_ports = [21, 22, 80, 443]
            for port in common_ports:
                tcp_packet = IP(dst=received.psrc) / TCP(dport=port, flags="S")
                response = sr1(tcp_packet, timeout=1, verbose=0)
                if response and response.haslayer(TCP) and response[TCP].flags == "SA":
                    device_info["services"].append({
                        "port": port,
                        "state": "open",
                        "service": "Desconocido"  # Puedes usar una lista para mapear nombres de servicios
                    })
            devices.append(device_info)

        return devices
    except Exception as e:
        return {"error": str(e)}

@app.route('/servicios/wifi_analyzer')
def wifi_analyzer():
    return render_template('wifi_analyzer.html')

@app.route('/servicios/network_simulator')
def network_simulator():
    return render_template('network_simulator.html')

@app.route('/servicios/analyze_bandwidth')
def analyze_bandwidth_route():
    bandwidth_data = analyze_bandwidth()  # Llamada a la función de análisis
    return render_template('analyze_bandwidth.html', bandwidth_data=bandwidth_data)

@app.route('/servicios/network_services')
def network_services():
    network = request.args.get('network', '192.168.1.0/24')  # Red por defecto
    services = scan_local_network(network)
    if "error" in services:
        return render_template('network_services.html', error=services["error"])
    return render_template('network_services.html', devices=services)


@app.route('/contact')
def contact():
    return render_template('contact.html')

# Modelo para los testimonios
class Testimonial(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    message = db.Column(db.String(500), nullable=False)
    rating = db.Column(db.Integer, nullable=False)  # Calificación de 1 a 5 estrellas

    def __repr__(self):
        return f"<Testimonial {self.name}>"
    
# Ruta para mostrar los testimonios
@app.route('/testimonials', methods=['GET', 'POST'])
def testimonials():
    if request.method == 'POST':
        # Obtener los datos del formulario
        name = request.form['name']
        message = request.form['message']
        rating = int(request.form['rating'])

        # Crear un nuevo testimonio
        new_testimonial = Testimonial(name=name, message=message, rating=rating)

        # Agregar a la base de datos
        db.session.add(new_testimonial)
        db.session.commit()

        return redirect(url_for('testimonials'))

    # Obtener todos los testimonios desde la base de datos
    testimonials = Testimonial.query.all()
    return render_template('testimonials.html', testimonials=testimonials)



@app.route('/submit_testimonial', methods=['POST'])
def submit_testimonial():
    name = request.form['name']
    position = request.form['position']
    message = request.form['message']
    rating = int(request.form['rating'])
    
    new_testimonial = Testimonial(
        name=name,
        position=position,
        message=message,
        rating=rating,
        avatar="default_avatar.jpg"  # Aquí puedes agregar la lógica para las imágenes si quieres
    )
    
    db.session.add(new_testimonial)
    db.session.commit()
    
    return redirect(url_for('testimonials'))

# Ruta para manejar el chat
@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.json.get("message")
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "Eres Nibble, un asistente experto en redes y pruebas de velocidad..."},
                {"role": "user", "content": user_message}
            ],
            temperature=1,
            max_tokens=256,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0
        )
        reply = response['choices'][0]['message']['content']
        return jsonify({'response': reply})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Ruta para datos de análisis de red
@app.route('/api/network_data')
def network_data():
    return jsonify(analyze_network())

# Ruta para simular errores de red
@app.route('/api/simulate_network_error', methods=['POST'])
def simulate_error():
    error_type = request.json.get("error_type", "")
    result = simulate_network_errors(error_type)
    return jsonify(result)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Crear las tablas si no existen
    app.run(debug=True)
