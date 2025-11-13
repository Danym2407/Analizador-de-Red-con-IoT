// Función para mostrar/ocultar el chatbot
function toggleChat() {
    const chatContainer = document.getElementById("chat-container");
    chatContainer.classList.toggle("hidden");
}

// Función que se ejecuta cuando el usuario envía un mensaje
// Función para enviar el mensaje y recibir la respuesta del chatbot
function sendMessage() {
    const message = document.getElementById("message-box").value;

    // Si el mensaje está vacío, no hacer nada
    if (message.trim() === "") return;

    // Agregar el mensaje del usuario al chat (lado derecho)
    addMessageToChat(message, "sent");

    // Mostrar la animación "escribiendo..."
    addTypingIndicator();

    // Limpiar el cuadro de entrada
    document.getElementById("message-box").value = "";

    // Hacer la solicitud POST a Flask
    fetch('/chat', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ message: message })
    })
    .then(response => response.json())
    .then(data => {
        // Remover la animación "escribiendo"
        removeTypingIndicator();
        
        // Agregar la respuesta del chatbot al chat (lado izquierdo)
        const reply = data.response;
        addMessageToChat(reply, "received");
    })
    .catch(error => {
        console.error("Error:", error);
        removeTypingIndicator();
    });
}

// Agregar el mensaje recibido al chat
function addMessageToChat(message, type) {
    const chatBody = document.getElementById("chat-body");
    const messageElement = document.createElement("div");
    messageElement.classList.add("message", type);
    messageElement.textContent = message;
    chatBody.appendChild(messageElement);
    chatBody.scrollTop = chatBody.scrollHeight;  // Mantener el scroll al final
}

// Configuración para enviar el mensaje cuando presionas "Enter"
document.getElementById("message-box").addEventListener("keydown", function(event) {
    if (event.key === "Enter") {
        event.preventDefault();
        sendMessage(); // Enviar el mensaje cuando se presiona "Enter"
    }
});



// Función para agregar la animación de "escribiendo"
function addTypingIndicator() {
    const chatBody = document.getElementById("chat-body");
    const typingElement = document.createElement("div");
    typingElement.classList.add("typing-indicator");
    typingElement.textContent = "Escribiendo...";
    chatBody.appendChild(typingElement);
}

// Función para eliminar la animación de "escribiendo"
function removeTypingIndicator() {
    const typingElements = document.getElementsByClassName("typing-indicator");
    if (typingElements.length > 0) {
        typingElements[0].remove();
    }
}

document.addEventListener('DOMContentLoaded', function () {
    const renderer = new THREE.WebGLRenderer({ alpha: true });
    renderer.outputColorSpace = THREE.SRGBColorSpace;
    renderer.setSize(window.innerWidth, window.innerHeight);
    renderer.setClearColor(0x000000, 0);
    renderer.setPixelRatio(window.devicePixelRatio);
    renderer.shadowMap.enabled = true;
    document.getElementById('model-container').appendChild(renderer.domElement);

    const scene = new THREE.Scene();
    const camera = new THREE.PerspectiveCamera(45, window.innerWidth / window.innerHeight, 1, 1000);
    camera.position.set(0, 100, 80);

    const controls = new THREE.OrbitControls(camera, renderer.domElement);
    controls.enableDamping = true;
    controls.target.set(0, 0, 0);
    controls.update();

    const ambientLight = new THREE.AmbientLight(0xffffff, 0.7);
    scene.add(ambientLight);

    const directionalLight = new THREE.DirectionalLight(0xffffff, 1.0);
    directionalLight.position.set(10, 100, 0);
    directionalLight.castShadow = true;
    scene.add(directionalLight);

    const textureLoader = new THREE.TextureLoader();
    const textures = {
        original: textureLoader.load('/static/Textures/BRICKTEXTURE.png'),
        green: textureLoader.load('/static/Textures/V_BRICKTEXTURE.png'),
        red: textureLoader.load('/static/Textures/R_BRICKTEXTURE.png'),
        grass: textureLoader.load('/static/Textures/GRASS.png'),
        stairs: textureLoader.load('/static/Textures/piedra.png')
    };

    const loader = new THREE.GLTFLoader().setPath('/static/img/');
    fetch('/static/img/13iberomapa_corrupted.glb')
        .then(response => response.arrayBuffer())
        .then(buffer => {
            const fixedBuffer = buffer.slice(12); // Corregir archivo corrupto
            loader.parse(fixedBuffer, '', (gltf) => {
                const model = gltf.scene;
                model.traverse((child) => {
                    if (child.isMesh) {
                        child.castShadow = true;
                        child.receiveShadow = true;
                        child.material.map = textures.original;
                    }
                });

                scene.add(model);
                document.getElementById('progress-container').style.display = 'none';
            });
        })
        .catch(error => {
            console.error('Error al cargar el modelo:', error);
            document.getElementById('progress').innerText = 'Error al cargar el mapa';
        });

    window.addEventListener('resize', () => {
        renderer.setSize(window.innerWidth, window.innerHeight);
        camera.aspect = window.innerWidth / window.innerHeight;
        camera.updateProjectionMatrix();
    });

    function animate() {
        requestAnimationFrame(animate);
        controls.update();
        renderer.render(scene, camera);
    }
    animate();
});
