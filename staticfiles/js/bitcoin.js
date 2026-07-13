window.onload = function() {
   
    const heroCanvas = document.getElementById("hero-canvas");
    const renderer = new THREE.WebGLRenderer({ canvas: heroCanvas, alpha: true, antialias: true });
    renderer.setSize(window.innerWidth, window.innerHeight);

    const scene = new THREE.Scene();
    const camera = new THREE.PerspectiveCamera(75, window.innerWidth/window.innerHeight, 0.1, 1000);
    camera.position.z = 20;

    const polyhedrons = [];
    const geometry = new THREE.IcosahedronGeometry(1.2, 0);
    const material = new THREE.MeshStandardMaterial({
        color: 0xffd700, 
        roughness: 0.2,
        emissive: 0x222222
    });

    for (let i = 0; i < 50; i++) {
        const mesh = new THREE.Mesh(geometry, material);
        mesh.position.x = (Math.random() - 0.5) * 40;
        mesh.position.y = (Math.random() - 0.5) * 20;
        mesh.position.z = (Math.random() - 0.5) * 30;
        scene.add(mesh);
        polyhedrons.push(mesh);
    }

    const light1 = new THREE.PointLight(0xffffff, 1.5);
    light1.position.set(15, 15, 15);
    scene.add(light1);
    const light2 = new THREE.PointLight(0xffffff, 1.0);
    light2.position.set(-15, -15, -15);
    scene.add(light2);
    scene.add(new THREE.AmbientLight(0xffffff, 0.4));

    function animatePolyhedrons() {
        requestAnimationFrame(animatePolyhedrons);
        polyhedrons.forEach((mesh, i) => {
            mesh.rotation.x += 0.002 + i * 0.0001;
            mesh.rotation.y += 0.002 + i * 0.0001;
            mesh.position.y += Math.sin(Date.now() * 0.001 + i) * 0.004;
            mesh.position.x += Math.cos(Date.now() * 0.001 + i) * 0.003;
        });
        renderer.render(scene, camera);
    }
    animatePolyhedrons();

    window.addEventListener("resize", () => {
        renderer.setSize(window.innerWidth, window.innerHeight);
        camera.aspect = window.innerWidth / window.innerHeight;
        camera.updateProjectionMatrix();
    });

    
    const btcCanvas = document.getElementById("bitcoinCanvas");
    const ctx = btcCanvas.getContext("2d");
    btcCanvas.width = window.innerWidth;
    btcCanvas.height = window.innerHeight;

    const logo = new Image();
    logo.src = "/static/images/btc.jpg"; 
    let angle = 0;
    let speed = 0.02;

    
    const positions = [];
    for (let i = 0; i < 10; i++) {
        positions.push({
            x: Math.random() * btcCanvas.width,
            y: Math.random() * btcCanvas.height,
            baseX: Math.random() * btcCanvas.width,
            swingOffset: Math.random() * Math.PI * 2 
        });
    }

    const size = 80; // smaller coin size

    function animateBitcoin() {
        ctx.clearRect(0, 0, btcCanvas.width, btcCanvas.height);

        positions.forEach((pos, i) => {
            ctx.save();
           
            const swing = Math.sin(Date.now() * 0.001 + pos.swingOffset) * 40; 
            ctx.translate(pos.baseX + swing, pos.y);
            ctx.rotate(angle + i * 0.1);
            ctx.shadowColor = "gold";
            ctx.shadowBlur = 30;
            ctx.beginPath();
            ctx.arc(0, 0, size / 2, 0, Math.PI * 2);
            ctx.closePath();
            ctx.clip();
            ctx.drawImage(logo, -size / 2, -size / 2, size, size);
            ctx.restore();
        });

        angle += speed;
        requestAnimationFrame(animateBitcoin);
    }

    logo.onload = animateBitcoin;

    window.onresize = function() {
        btcCanvas.width = window.innerWidth;
        btcCanvas.height = window.innerHeight;
        renderer.setSize(window.innerWidth, window.innerHeight);
        camera.aspect = window.innerWidth / window.innerHeight;
        camera.updateProjectionMatrix();
    };

   
    const slides = document.querySelectorAll(".carousel-slide");
    const prev = document.querySelector(".carousel-prev");
    const next = document.querySelector(".carousel-next");
    let current = 0;
    let autoRotate;

    function showSlide(index) {
        slides.forEach((slide, i) => {
            slide.classList.toggle("active", i === index);
        });
    }

    function startAutoRotate() {
        autoRotate = setInterval(() => {
            current = (current + 1) % slides.length;
            showSlide(current);
        }, 2000);
    }

    function resetAutoRotate() {
        clearInterval(autoRotate);
        startAutoRotate();
    }

    if (slides.length > 0) {
        showSlide(current);
        startAutoRotate();
        if (prev) prev.addEventListener("click", () => {
            current = (current - 1 + slides.length) % slides.length;
            showSlide(current);
            resetAutoRotate();
        });
        if (next) next.addEventListener("click", () => {
            current = (current + 1) % slides.length;
            showSlide(current);
            resetAutoRotate();
        });
    }
};

document.addEventListener("DOMContentLoaded", () => {
  const btcInput = document.getElementById("btcAmount");
  const resultBox = document.getElementById("calcResult");
  const currencySelect = document.getElementById("currencySelect");

  async function getBTCPrice(currency) {
    try {
      const response = await fetch(
        `https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=${currency}`
      );
      const data = await response.json();
      return data.bitcoin[currency.toLowerCase()];
    } catch (error) {
      console.error("Error fetching BTC price:", error);
      return null;
    }
  }

  async function updateResult() {
    const amount = parseFloat(btcInput.value);
    const currency = currencySelect.value;

    if (!amount || amount <= 0) {
      resultBox.textContent = "0";
      return;
    }

    const btcPrice = await getBTCPrice(currency);
    if (btcPrice) {
     
      const worth = amount * btcPrice;
      resultBox.textContent = `${worth.toLocaleString()} ${currency}`;
    } else {
      resultBox.textContent = "Error";
    }
  }

  btcInput.addEventListener("input", updateResult);
  currencySelect.addEventListener("change", updateResult);
});
