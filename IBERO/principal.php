<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <title>IBERO RED</title>
    <link rel="stylesheet" href="Styles/index.css">
    <script async src="https://unpkg.com/es-module-shims@1.6.3/dist/es-module-shims.js"></script>
    <script type="importmap">
      {
        "imports": {
          "three": "https://unpkg.com/three@v0.163.0/build/three.module.js",
          "three/addons/": "https://unpkg.com/three@v0.163.0/examples/jsm/"
        }
      }
    </script>
  </head>
  <header>
    <div class="left">
        <img src="Img/ibero.jpg" class="logo-ibero">
        <span class="header-text">CampusNet</span>
        <span class="header-text">Anális de Red</span>
    </div>



  </header>
  <body>
    <div id="container">
      <div id="model-container">
        <h1 id="heading">IBERO RED</h1>
        
        
        <div id="progress-container">
            <div id="progress">Cargando el mapa...</div>
          </div>
          
          <script type="module" src="./ibero2.js"></script>
    
    
    

  <div id="side-container">
  <button id="greenTextureButton">Verde</button>
  <button id="redTextureButton">Rojo</button>
  <button id="originalTextureButton">Original</button>
</div>

  
      
    </div>
   


  </body>
</html>
