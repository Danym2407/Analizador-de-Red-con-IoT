import * as THREE from 'three';
import { GLTFLoader } from 'three/addons/loaders/GLTFLoader.js';
import { OrbitControls } from 'three/addons/controls/OrbitControls.js';

// Configuración del renderizador
const renderer = new THREE.WebGLRenderer({ alpha: true });
renderer.outputColorSpace = THREE.SRGBColorSpace;
renderer.setSize(window.innerWidth, window.innerHeight);
renderer.setClearColor(0x000000, 0);
renderer.setPixelRatio(window.devicePixelRatio);
renderer.shadowMap.enabled = false;

document.getElementById('model-container').appendChild(renderer.domElement);

// Configuración de la escena y la cámara
const scene = new THREE.Scene();
const camera = new THREE.PerspectiveCamera(45, window.innerWidth / window.innerHeight, 1, 1000);
camera.position.set(0, 100, 80);
camera.lookAt(new THREE.Vector3(0, 0, 0));

const controls = new OrbitControls(camera, renderer.domElement);
controls.enableDamping = true;
controls.enablePan = false;
controls.maxDistance = 100;
controls.minDistance = 30;
controls.enableZoom = true;
controls.zoomSpeed = 1.2;
controls.autoRotate = false;
controls.target = new THREE.Vector3(0, 0, 0);
controls.update();

// Raycaster y mouse para detectar interacciones
const raycaster = new THREE.Raycaster();
const mouse = new THREE.Vector2();
let selectedObject = null;
let modelMesh = null;

// Luz ambiental y direccional
const ambientLight = new THREE.AmbientLight(0xffffff, 0.7);
scene.add(ambientLight);
const directionalLight = new THREE.DirectionalLight(0xffffff, 1.0);
directionalLight.position.set(10, 100, 0);
directionalLight.castShadow = true;
scene.add(directionalLight);

// LOD (Level of Detail)
const lod = new THREE.LOD();
const loader = new GLTFLoader().setPath('Img/');

// Configuración de texturas
const textureLoader = new THREE.TextureLoader();
const originalTexture = textureLoader.load('Textures/BRICKTEXTURE.png');
const greenTexture = textureLoader.load('Textures/V_BRICKTEXTURE.png');
const redTexture = textureLoader.load('Textures/R_BRICKTEXTURE.png');
const grassTexture = textureLoader.load('Textures/GRASS.png');
const stairsTexture = textureLoader.load('Textures/piedra.png');

// Cargar el archivo GLB corrupto y eliminar los 12 bytes
function loadCorruptedGLB() {
  fetch('Img/13iberomapa_corrupted.glb')
    .then(response => response.arrayBuffer())
    .then(buffer => {
      const fixedBuffer = buffer.slice(12); // Elimina los primeros 12 bytes corruptos
      
      loader.parse(fixedBuffer, '', (gltf) => {
        modelMesh = gltf.scene;
        modelMesh.traverse((child) => {
          if (child.isMesh) {
            console.log(`Mesh cargado: ${child.name}`);
            child.castShadow = true;
            child.receiveShadow = true;

            if (child.name.includes('Grass')) {
              child.material.map = grassTexture;
            } else if (child.name.includes('tair') || child.name.includes('Piso')) {
              child.material.map = stairsTexture;
            } else {
              child.material.map = originalTexture;
            }
            child.material.needsUpdate = true;
          }
        });

        modelMesh.position.set(0, 0, 0);
        scene.add(modelMesh);
        document.getElementById('progress-container').style.display = 'none';
      }, undefined, (error) => console.error(error));
    })
    .catch(error => console.error('Error al cargar el archivo:', error));
}

loadCorruptedGLB(); // Cargar el modelo GLB corrupto y corregido

// Ajustar tamaño del renderizador al redimensionar la ventana
window.addEventListener('resize', () => {
  renderer.setSize(window.innerWidth, window.innerHeight);
  camera.aspect = window.innerWidth / window.innerHeight;
  camera.updateProjectionMatrix();
});

//-----------BOTONES--------

document.getElementById('greenTextureButton').addEventListener('click', () => {
  console.log("Botón de textura verde presionado");
  if (modelMesh) {
    const H_PB_verde = modelMesh.getObjectByName('H-PB');

    if (H_PB_verde && H_PB_verde.isMesh) {
      H_PB_verde.material.map = greenTexture;
      H_PB_verde.material.needsUpdate = true;
    } else {
      console.warn("No se encontró 'H-PB' o no es un Mesh");
    }
  }
});

document.getElementById('redTextureButton').addEventListener('click', () => {
  console.log("Botón de textura roja presionado");
  if (modelMesh) {
    const H_PB_rojo = modelMesh.getObjectByName('H-PB');

    if (H_PB_rojo && H_PB_rojo.isMesh) {
      H_PB_rojo.material.map = redTexture;
      H_PB_rojo.material.needsUpdate = true;
    } else {
      console.warn("No se encontró 'H-PB' o no es un Mesh");
    }
  }
});

document.getElementById('originalTextureButton').addEventListener('click', () => {
  console.log("Botón de textura original presionado");
  if (modelMesh) {
    const H_PB_original = modelMesh.getObjectByName('H-PB');

    if (H_PB_original && H_PB_original.isMesh) {
      H_PB_original.material.map = originalTexture;
      H_PB_original.material.needsUpdate = true;
    } else {
      console.warn("No se encontró 'H-PB' o no es un Mesh");
    }
  }
});

// Animación
function animate() {
  requestAnimationFrame(animate);
  controls.update();
  lod.update(camera);
  renderer.render(scene, camera);
}
animate();
