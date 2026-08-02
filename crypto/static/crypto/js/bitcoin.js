
document.addEventListener("DOMContentLoaded", function () {

    /* =========================================================
       1. THREE.JS HERO BACKGROUND
    ========================================================= */

    const heroCanvas = document.getElementById("hero-canvas");

    if (heroCanvas && typeof THREE !== "undefined") {

        const renderer = new THREE.WebGLRenderer({
            canvas: heroCanvas,
            alpha: true,
            antialias: true
        });

        renderer.setSize(window.innerWidth, window.innerHeight);
        renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));

        const scene = new THREE.Scene();

        const camera = new THREE.PerspectiveCamera(
            75,
            window.innerWidth / window.innerHeight,
            0.1,
            1000
        );

        camera.position.z = 20;

        /* ---------- Polyhedrons ---------- */

        const polyhedrons = [];

        const geometry = new THREE.IcosahedronGeometry(1.2, 0);

        const material = new THREE.MeshStandardMaterial({
            color: 0xffd700,
            roughness: 0.2,
            emissive: 0x222222
        });

        for (let i = 0; i < 50; i++) {

            const mesh = new THREE.Mesh(
                geometry,
                material
            );

            mesh.position.x =
                (Math.random() - 0.5) * 40;

            mesh.position.y =
                (Math.random() - 0.5) * 20;

            mesh.position.z =
                (Math.random() - 0.5) * 30;

            mesh.rotation.x =
                Math.random() * Math.PI;

            mesh.rotation.y =
                Math.random() * Math.PI;

            scene.add(mesh);

            polyhedrons.push(mesh);
        }

        /* ---------- Lights ---------- */

        const light1 = new THREE.PointLight(
            0xffffff,
            1.5
        );

        light1.position.set(15, 15, 15);
        scene.add(light1);

        const light2 = new THREE.PointLight(
            0xffffff,
            1.0
        );

        light2.position.set(-15, -15, -15);
        scene.add(light2);

        const ambientLight =
            new THREE.AmbientLight(
                0xffffff,
                0.4
            );

        scene.add(ambientLight);

        
        function animatePolyhedrons() {

            requestAnimationFrame(
                animatePolyhedrons
            );

            const time = Date.now() * 0.001;

            polyhedrons.forEach((mesh, i) => {

                mesh.rotation.x +=
                    0.002 + i * 0.0001;

                mesh.rotation.y +=
                    0.002 + i * 0.0001;

                mesh.position.y +=
                    Math.sin(time + i) * 0.004;

                mesh.position.x +=
                    Math.cos(time + i) * 0.003;
            });

            renderer.render(
                scene,
                camera
            );
        }

        animatePolyhedrons();

       

        function resizeHero() {

            renderer.setSize(
                window.innerWidth,
                window.innerHeight
            );

            renderer.setPixelRatio(
                Math.min(window.devicePixelRatio, 2)
            );

            camera.aspect =
                window.innerWidth /
                window.innerHeight;

            camera.updateProjectionMatrix();
        }

        window.addEventListener(
            "resize",
            resizeHero
        );
    }

    const btcCanvas =
        document.getElementById("btcCalcCanvas");

    if (btcCanvas) {

        const ctx =
            btcCanvas.getContext("2d");

        function resizeBitcoinCanvas() {

            btcCanvas.width =
                window.innerWidth;

            btcCanvas.height =
                window.innerHeight;
        }

        resizeBitcoinCanvas();

        const logo = new Image();

        
        logo.src = "/static/images/btc.jpg";

        let angle = 0;

        const speed = 0.02;

        const positions = [];

        for (let i = 0; i < 10; i++) {

            positions.push({

                baseX:
                    Math.random() *
                    btcCanvas.width,

                y:
                    Math.random() *
                    btcCanvas.height,

                swingOffset:
                    Math.random() *
                    Math.PI * 2
            });
        }

        const size = 80;

        function animateBitcoin() {

            ctx.clearRect(
                0,
                0,
                btcCanvas.width,
                btcCanvas.height
            );

            const time =
                Date.now() * 0.001;

            positions.forEach(
                (pos, i) => {

                    ctx.save();

                    const swing =
                        Math.sin(
                            time +
                            pos.swingOffset
                        ) * 40;

                    ctx.translate(
                        pos.baseX + swing,
                        pos.y
                    );

                    ctx.rotate(
                        angle + i * 0.1
                    );

                    ctx.shadowColor =
                        "gold";

                    ctx.shadowBlur = 30;

                    ctx.beginPath();

                    ctx.arc(
                        0,
                        0,
                        size / 2,
                        0,
                        Math.PI * 2
                    );

                    ctx.closePath();

                    ctx.clip();

                    
                    if (logo.complete &&
                        logo.naturalWidth > 0) {

                        ctx.drawImage(
                            logo,
                            -size / 2,
                            -size / 2,
                            size,
                            size
                        );
                    }

                    ctx.restore();
                }
            );

            angle += speed;

            requestAnimationFrame(
                animateBitcoin
            );
        }

        logo.onload = function () {
            animateBitcoin();
        };

        if (logo.complete &&
            logo.naturalWidth > 0) {

            animateBitcoin();
        }

        window.addEventListener(
            "resize",
            resizeBitcoinCanvas
        );
    }


    const slides =
        document.querySelectorAll(
            ".carousel-slide"
        );

    const prev =
        document.querySelector(
            ".carousel-prev"
        );

    const next =
        document.querySelector(
            ".carousel-next"
        );

    let current = 0;

    let autoRotate = null;

    function showSlide(index) {

        slides.forEach(
            (slide, i) => {

                slide.classList.toggle(
                    "active",
                    i === index
                );
            }
        );
    }

    function startAutoRotate() {

        if (slides.length <= 1) {
            return;
        }

        clearInterval(autoRotate);

        autoRotate = setInterval(
            function () {

                current =
                    (current + 1) %
                    slides.length;

                showSlide(current);

            },
            2000
        );
    }

    function resetAutoRotate() {

        clearInterval(autoRotate);

        startAutoRotate();
    }

    if (slides.length > 0) {

        showSlide(current);

        startAutoRotate();

        if (prev) {

            prev.addEventListener(
                "click",
                function () {

                    current =
                        (current - 1 +
                        slides.length) %
                        slides.length;

                    showSlide(current);

                    resetAutoRotate();
                }
            );
        }

        if (next) {

            next.addEventListener(
                "click",
                function () {

                    current =
                        (current + 1) %
                        slides.length;

                    showSlide(current);

                    resetAutoRotate();
                }
            );
        }
    }


       
       HTML:
       <input id="btcAmount">
       <div id="calcResult">0</div>

     

    const btcInput =
        document.getElementById(
            "btcAmount"
        );

    const resultBox =
        document.getElementById(
            "calcResult"
        );

    const currencySelect =
        document.getElementById(
            "currencySelect"
        );


    
    if (!btcInput || !resultBox) {

        console.warn(
            "Bitcoin calculator elements not found."
        );

        return;
    }



    function getSelectedCurrency() {

        if (currencySelect) {

            return (
                currencySelect.value ||
                "usd"
            ).toLowerCase();

        }

        return "usd";
    }


    async function getBTCPrice(currency) {

        try {

            const response =
                await fetch(
                    "https://api.coingecko.com/api/v3/simple/price" +
                    "?ids=bitcoin" +
                    "&vs_currencies=" +
                    encodeURIComponent(currency),
                    {
                        method: "GET",
                        headers: {
                            "Accept":
                                "application/json"
                        }
                    }
                );

            if (!response.ok) {

                throw new Error(
                    "CoinGecko HTTP error: " +
                    response.status
                );
            }

            const data =
                await response.json();

            if (
                !data ||
                !data.bitcoin ||
                typeof data.bitcoin[currency] !==
                "number"
            ) {

                throw new Error(
                    "Invalid Bitcoin price response."
                );
            }

            return data.bitcoin[currency];

        } catch (error) {

            console.error(
                "Bitcoin price error:",
                error
            );

            return null;
        }
    }



    function formatCurrency(
        value,
        currency
    ) {

        try {

            return new Intl.NumberFormat(
                undefined,
                {
                    style: "currency",
                    currency:
                        currency.toUpperCase(),
                    maximumFractionDigits: 2
                }
            ).format(value);

        } catch (error) {

            return (
                value.toLocaleString() +
                " " +
                currency.toUpperCase()
            );
        }
    }

    let calculationRequest = 0;

    async function updateResult() {

        const amount =
            parseFloat(
                btcInput.value
            );

        /*
         * Empty / invalid amount
         */
        if (
            Number.isNaN(amount) ||
            amount <= 0
        ) {

            resultBox.textContent = "0";

            return;
        }

        const currency =
            getSelectedCurrency();

        /*
         * Show loading state
         */
        resultBox.textContent =
            "Loading...";

        /*
         * Prevent older API requests
         * from overwriting newer results.
         */
        const requestId =
            ++calculationRequest;

        const btcPrice =
            await getBTCPrice(
                currency
            );

        /*
         * A newer calculation happened
         * while this request was loading.
         */
        if (
            requestId !==
            calculationRequest
        ) {

            return;
        }

        if (
            btcPrice !== null &&
            Number.isFinite(btcPrice)
        ) {

            const worth =
                amount * btcPrice;

            resultBox.textContent =
                formatCurrency(
                    worth,
                    currency
                );

        } else {

            resultBox.textContent =
                "Unable to get BTC price";
        }
    }



    btcInput.addEventListener(
        "input",
        updateResult
    );

    if (currencySelect) {

        currencySelect.addEventListener(
            "change",
            updateResult
        );
    }


    btcInput.addEventListener(
        "keydown",
        function (event) {

            if (event.key === "Enter") {

                event.preventDefault();

                updateResult();
            }
        }
    );

});

