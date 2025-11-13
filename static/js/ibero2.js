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
        let model; // Guardar referencia al modelo
        fetch('/static/img/13iberomapa_corrupted.glb')
            .then(response => response.arrayBuffer())
            .then(buffer => {
                const fixedBuffer = buffer.slice(12); // Corregir archivo corrupto
                loader.parse(fixedBuffer, '', (gltf) => {
                    model = gltf.scene;
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
    
        // Función para cambiar de color una parte específica del modelo
        function highlightPart(partName) {
            if (!model) return; // Asegurarse de que el modelo está cargado
            model.traverse((child) => {
                if (child.isMesh) {
                    if (child.name === partName) {
                        // Aplicar textura o material verde
                        child.material.map = textures.green;
                    } else {
                        // Restablecer a la textura original
                        child.material.map = textures.original;
                    }
                    child.material.needsUpdate = true; // Actualizar material
                }
            });
        }
    
        // Manejar clics en el menú
        function handleMenuClick(option) {
            highlightPart(option);
        }
    
        // Animar la escena
        function animate() {
            requestAnimationFrame(animate);
            controls.update();
            renderer.render(scene, camera);
        }
        animate();
    
        // Exponer la función globalmente para usarla en los botones
        window.handleMenuClick = handleMenuClick;
    });
    