function formatForexInfo(base, quote, rate) {
    if (!rate || rate.change_percent === 'N/A') {
        return `
            <div class="forex-info-row">
                <p><strong>Currency pair:</strong> <span class="pair">${base} / ${quote}</span></p>
                <p><strong>Status:</strong> No data available for this pair.</p>
            </div>
        `;
    }

    return `
        <div class="forex-info-row">
            <p><strong>Currency pair:</strong> <span class="pair">${base} / ${quote}</span></p>
            <p><strong>Change percent:</strong> ${rate.change_percent}%</p>
            <p><strong>Change value:</strong> ${rate.change_value}</p>
            <p><strong>Status:</strong> ${rate.change_percent >= 0 ? 'Gain' : 'Loss'}</p>
        </div>
    `;
}

function selectForexCell(cell) {
    const selected = document.querySelector('.forex-table td.selected');
    if (selected) selected.classList.remove('selected');
    cell.classList.add('selected');

    const base = cell.dataset.base;
    const quote = cell.dataset.quote;
    const changePercent = cell.dataset.changePercent || 'N/A';
    const changeValue = cell.dataset.changeValue || 'N/A';
    const infoPanel = document.querySelector('.forex-info-panel');
    infoPanel.innerHTML = formatForexInfo(base, quote, {
        change_percent: changePercent,
        change_value: changeValue,
    });
}

function createCell(rate, base, quote) {
    const td = document.createElement('td');
    td.dataset.base = base;
    td.dataset.quote = quote;
    td.tabIndex = 0;
    td.classList.add('interactive');

    if (rate) {
        td.textContent = `${rate.change_percent}% (${rate.change_value})`;
        td.classList.add(rate.change_percent >= 0 ? 'positive' : 'negative');
        td.dataset.changePercent = rate.change_percent;
        td.dataset.changeValue = rate.change_value;
    } else {
        td.textContent = '–';
        td.classList.add('empty');
        td.dataset.changePercent = '';
        td.dataset.changeValue = '';
    }

    td.addEventListener('click', () => selectForexCell(td));
    td.addEventListener('keydown', (event) => {
        if (event.key === 'Enter' || event.key === ' ') {
            event.preventDefault();
            selectForexCell(td);
        }
    });
    return td;
}

function refreshForexTable() {
    fetch('/forex-table-api/')
        .then(response => response.json())
        .then(data => {
            const tbody = document.querySelector('.forex-table tbody');
            const infoPanel = document.querySelector('.forex-info-panel');
            tbody.innerHTML = ''; 
            infoPanel.innerHTML = '<p>Select any positive or negative rate cell to see the currency pair details here.</p>';

            data.table_rows.forEach(row => {
                const tr = document.createElement('tr');
                const th = document.createElement('th');
                th.textContent = row.base;
                tr.appendChild(th);

                row.rates.forEach((rate, index) => {
                    const quote = data.currencies ? data.currencies[index] : 'N/A';
                    const td = createCell(rate, row.base, quote);
                    tr.appendChild(td);
                });

                tbody.appendChild(tr);
            });
        })
        .catch(error => {
            console.error('Failed to load forex data:', error);
        });
}

setInterval(refreshForexTable, 30000);

document.addEventListener('DOMContentLoaded', refreshForexTable);
