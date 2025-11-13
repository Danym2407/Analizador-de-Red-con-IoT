# Analizador de Red con IoT

Un sistema completo para el análisis de redes con capacidades de monitoreo IoT desarrollado con Flask.

## Características

- Análisis de velocidad de internet
- Monitoreo de latencia
- Escaneo de dispositivos en la red
- Análisis de ancho de banda
- Simulador de red
- Análisis WiFi
- Integración con OpenAI para análisis inteligente

## Instalación

1. Clona el repositorio:
```bash
git clone https://github.com/Danym2407/Analizador-de-Red-con-IoT.git
cd Analizador-de-Red-con-IoT
```

2. Crea un entorno virtual:
```bash
python -m venv venv
```

3. Activa el entorno virtual:
```bash
# Windows
venv\Scripts\activate
# Linux/Mac
source venv/bin/activate
```

4. Instala las dependencias:
```bash
pip install -r requirements.txt
```

5. Configura las variables de entorno:
```bash
# Copia el archivo de ejemplo
cp .env.example .env
# Edita .env y agrega tu API key de OpenAI
```

6. Ejecuta la aplicación:
```bash
python app.py
```

## Configuración

### Variables de Entorno

Crea un archivo `.env` en la raíz del proyecto con las siguientes variables:

```
OPENAI_API_KEY=tu_api_key_de_openai_aqui
```

### Requisitos del Sistema

- Python 3.7 o superior
- Nmap (para escaneo de red)
- Permisos administrativos (para algunas funciones de red)

## Uso

1. Navega a `http://localhost:5000` en tu navegador
2. Explora las diferentes herramientas de análisis de red
3. Utiliza el simulador para probar configuraciones
4. Revisa los análisis generados por IA

## Estructura del Proyecto

```
├── app.py                 # Aplicación principal Flask
├── requirements.txt       # Dependencias Python
├── .env.example          # Plantilla para variables de entorno
├── static/               # Archivos estáticos (CSS, JS, imágenes)
├── templates/            # Plantillas HTML
└── README.md            # Este archivo
```

## Contribuir

1. Fork el repositorio
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## Licencia

Este proyecto está bajo la Licencia MIT - ve el archivo LICENSE para más detalles.

## Autor

- **Danny M** - [@Danym2407](https://github.com/Danym2407)

## Agradecimientos

- IBERO Universidad
- Proyecto de Redes - 5to Semestre