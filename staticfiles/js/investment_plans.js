document.addEventListener("DOMContentLoaded", function() {
    const chartCanvas = document.getElementById('marketChart');
    if (chartCanvas) {
        const ctx = chartCanvas.getContext('2d');
        new Chart(ctx, {
            type: 'line',
            data: {
                labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun'],
                datasets: [{
                    label: 'Crypto Growth',
                    data: [12000, 15000, 18000, 22000, 26000, 30000],
                    borderColor: 'gold',
                    backgroundColor: 'rgba(255, 165, 0, 0.2)',
                    fill: true,
                    tension: 0.4
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: { labels: { color: '#fff' } }
                },
                scales: {
                    x: { ticks: { color: '#fff' } },
                    y: { ticks: { color: '#fff' } }
                }
            }
        });
    }

    const canvas = document.getElementById('moveableCanvas');
    if (canvas) {
        const ctx2 = canvas.getContext('2d');
        const stars = [];
        const numStars = 60;
        let angle = 0;

        for (let i = 0; i < numStars; i++) {
            stars.push({
                x: Math.random() * canvas.width,
                y: Math.random() * canvas.height,
                radius: Math.random() * 2 + 1
            });
        }

        function drawStars() {
            ctx2.fillStyle = "black";
            ctx2.fillRect(0, 0, canvas.width, canvas.height);

            stars.forEach(star => {
                ctx2.beginPath();
                ctx2.arc(star.x, star.y, star.radius, 0, Math.PI * 2);
                ctx2.fillStyle = "white";
                ctx2.shadowColor = "silver";
                ctx2.shadowBlur = 8;
                ctx2.fill();
                ctx2.shadowBlur = 0;
            });
        }

        function drawLightning() {
            ctx2.save();
            ctx2.translate(canvas.width / 2, canvas.height / 2);
            ctx2.rotate(angle);

            ctx2.beginPath();
            ctx2.arc(0, 0, 120, 0, Math.PI * 2);
            ctx2.strokeStyle = 'silver';
            ctx2.lineWidth = 2;
            ctx2.stroke();

            for (let i = 0; i < 10; i++) {
                ctx2.beginPath();
                ctx2.moveTo(0, 0);
                ctx2.lineTo(
                    Math.cos((i / 10) * 2 * Math.PI) * 120,
                    Math.sin((i / 10) * 2 * Math.PI) * 120
                );
                ctx2.strokeStyle = 'rgba(192,192,192,0.8)';
                ctx2.stroke();
            }

            ctx2.restore();
        }

        function animate() {
            ctx2.clearRect(0, 0, canvas.width, canvas.height);
            drawStars();
            drawLightning();
            angle += 0.01;
            requestAnimationFrame(animate);
        }

        animate();
    }

    const roiCtx = document.getElementById('roiChart');
    if (roiCtx) {
        new Chart(roiCtx.getContext('2d'), {
            type: 'bar',
            data: {
                labels: ['Starter', 'Pro', 'Elite'],
                datasets: [{
                    label: 'ROI %',
                    data: [10, 20, 35],
                    backgroundColor: ['#FFD700', '#FF8C00', '#C0C0C0']
                }]
            },
            options: { responsive: true, maintainAspectRatio: false }
        });
    }

    const riskCtx = document.getElementById('riskRewardChart');
    if (riskCtx) {
        new Chart(riskCtx.getContext('2d'), {
            type: 'scatter',
            data: {
                datasets: [{
                    label: 'Plans',
                    data: [
                        {x: 2, y: 10},
                        {x: 5, y: 20},
                        {x: 8, y: 35}
                    ],
                    backgroundColor: 'silver'
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                scales: {
                    x: { title: { display: true, text: 'Risk Level' } },
                    y: { title: { display: true, text: 'Reward %' } }
                }
            }
        });
    }

    const portfolioCtx = document.getElementById('portfolioChart');
    if (portfolioCtx) {
        new Chart(portfolioCtx.getContext('2d'), {
            type: 'pie',
            data: {
                labels: ['Bitcoin', 'Ethereum', 'Altcoins'],
                datasets: [{
                    data: [50, 30, 20],
                    backgroundColor: ['#FFD700', '#FF6600', '#C0C0C0']
                }]
            },
            options: { responsive: true, maintainAspectRatio: false }
        });
    }

    const volumeCtx = document.getElementById('volumeChart');
    if (volumeCtx) {
        new Chart(volumeCtx.getContext('2d'), {
            type: 'bar',
            data: {
                labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun'],
                datasets: [{
                    label: 'Volume (BTC)',
                    data: [500, 800, 1200, 900, 1500, 2000],
                    backgroundColor: 'rgba(192,192,192,0.8)'
                }]
            },
            options: { responsive: true, maintainAspectRatio: false }
        });
    }

    rotateCanvas("investBtnCanvas", "/static/images/btc.png");
    rotateCanvas("investEthCanvas", "/static/images/ethe.png");
    rotateCanvas("investUsdtCanvas", "/static/images/usdt.png");

});

function rotateCanvas(id, imageSrc) {
  const canvas = document.getElementById(id);
  if (!canvas) return;
  const ctx = canvas.getContext("2d");
  let angle = 0;
  const img = new Image();
  img.src = imageSrc;
  img.onload = function() {
    function draw() {
      ctx.clearRect(0, 0, canvas.width, canvas.height);
      ctx.save();
      ctx.translate(canvas.width/2, canvas.height/2);
      ctx.rotate(angle);
      ctx.drawImage(img, -50, -50, 100, 100);
      ctx.restore();
      angle += 0.02;
      requestAnimationFrame(draw);
    }
    draw();
  };
}
