const csrfToken = document.querySelector('meta[name="csrf-token"]').getAttribute('content');

let currentProcesses = [];

function loadProcesses() {
    const content = document.getElementById('content');
    content.innerHTML = `
        <h1 class="bounce-in">Процессы</h1>
        <div class="card zoom-in">
            <div class="file-controls">
                <input type="text" id="processSearch" placeholder="Поиск по имени" oninput="filterProcesses()" class="slide-in">
                <select id="processSort" onchange="sortProcesses()" class="slide-in">
                    <option value="pid">По PID</option>
                    <option value="name">По имени</option>
                    <option value="cpu">По CPU</option>
                    <option value="memory">По RAM</option>
                </select>
            </div>
        </div>
        <div class="card table-card zoom-in" id="processList"></div>
    `;
    content.classList.add('fade-in');
    fetch('/api/processes')
        .then(response => response.json())
        .then(data => {
            currentProcesses = data;
            renderProcessList();
        });
}

function filterProcesses() {
    const search = document.getElementById('processSearch').value.toLowerCase();
    const filtered = currentProcesses.filter(proc => proc.name.toLowerCase().includes(search));
    renderProcessList(filtered);
}

function sortProcesses() {
    const sortBy = document.getElementById('processSort').value;
    currentProcesses.sort((a, b) => {
        if (sortBy === 'pid') return a.pid - b.pid;
        if (sortBy === 'name') return a.name.localeCompare(b.name);
        if (sortBy === 'cpu') return a.cpu - b.cpu;
        if (sortBy === 'memory') return a.memory - b.memory;
        return 0;
    });
    renderProcessList();
}

function renderProcessList(items = currentProcesses) {
    const list = document.getElementById('processList');
    list.innerHTML = '<table><tr><th>PID</th><th>Имя</th><th>CPU</th><th>RAM</th><th>Действия</th></tr>' +
        items.map((proc, index) => `
            <tr class="process-stagger" style="animation-delay: ${index * 0.05}s;">
                <td>${proc.pid}</td>
                <td>${proc.name}</td>
                <td>${proc.cpu}%</td>
                <td>${proc.memory}%</td>
                <td><button onclick="killProcess(${proc.pid})" class="bounce-in">Завершить</button></td>
            </tr>
        `).join('') + '</table>';
}

function killProcess(pid) {
    fetch('/api/processes/kill', {
        method: 'POST',
        headers: {'Content-Type': 'application/json', 'X-CSRFToken': csrfToken},
        body: JSON.stringify({pid})
    }).then(() => loadProcesses());
}

let cpuChart, ramChart, diskChart, netChart;

// Function to get chart colors based on theme
function getChartColors() {
    const isDark = document.body.classList.contains('dark');
    return {
        cpu: {
            border: isDark ? 'rgba(52, 152, 219, 1)' : 'rgba(75,192,192,1)',
            background: isDark ? 'rgba(52, 152, 219, 0.2)' : 'rgba(75,192,192,0.1)',
            gradient: isDark ? ['rgba(52, 152, 219, 0.3)', 'rgba(52, 152, 219, 0.05)'] : ['rgba(75,192,192,0.3)', 'rgba(75,192,192,0.05)']
        },
        ram: {
            border: isDark ? 'rgba(231, 76, 60, 1)' : 'rgba(255,99,132,1)',
            background: isDark ? 'rgba(231, 76, 60, 0.2)' : 'rgba(255,99,132,0.1)',
            gradient: isDark ? ['rgba(231, 76, 60, 0.3)', 'rgba(231, 76, 60, 0.05)'] : ['rgba(255,99,132,0.3)', 'rgba(255,99,132,0.05)']
        },
        disk: {
            border: isDark ? 'rgba(241, 196, 15, 1)' : 'rgba(255,206,86,1)',
            background: isDark ? 'rgba(241, 196, 15, 0.2)' : 'rgba(255,206,86,0.1)',
            gradient: isDark ? ['rgba(241, 196, 15, 0.3)', 'rgba(241, 196, 15, 0.05)'] : ['rgba(255,206,86,0.3)', 'rgba(255,206,86,0.05)']
        },
        net: {
            border: isDark ? 'rgba(155, 89, 182, 1)' : 'rgba(153,102,255,1)',
            background: isDark ? 'rgba(155, 89, 182, 0.2)' : 'rgba(153,102,255,0.1)',
            gradient: isDark ? ['rgba(155, 89, 182, 0.3)', 'rgba(155, 89, 182, 0.05)'] : ['rgba(153,102,255,0.3)', 'rgba(153,102,255,0.05)']
        },
        grid: isDark ? 'rgba(255,255,255,0.1)' : 'rgba(200,200,200,0.3)',
        tooltip: isDark ? 'rgba(0,0,0,0.9)' : 'rgba(0,0,0,0.8)'
    };
}

// Function to create gradient for charts
function createGradient(ctx, colors) {
    const gradient = ctx.createLinearGradient(0, 0, 0, 400);
    gradient.addColorStop(0, colors[0]);
    gradient.addColorStop(1, colors[1]);
    return gradient;
}

// Function to update chart colors
function updateChartColors() {
    if (!cpuChart || !ramChart || !diskChart || !netChart) return;

    const colors = getChartColors();

    cpuChart.data.datasets[0].borderColor = colors.cpu.border;
    cpuChart.data.datasets[0].backgroundColor = createGradient(cpuChart.ctx, colors.cpu.gradient);
    cpuChart.options.scales.y.grid.color = colors.grid;
    cpuChart.options.scales.x.grid.color = colors.grid;
    cpuChart.options.plugins.tooltip.backgroundColor = colors.tooltip;

    ramChart.data.datasets[0].borderColor = colors.ram.border;
    ramChart.data.datasets[0].backgroundColor = createGradient(ramChart.ctx, colors.ram.gradient);
    ramChart.options.scales.y.grid.color = colors.grid;
    ramChart.options.scales.x.grid.color = colors.grid;
    ramChart.options.plugins.tooltip.backgroundColor = colors.tooltip;

    diskChart.data.datasets[0].borderColor = colors.disk.border;
    diskChart.data.datasets[0].backgroundColor = createGradient(diskChart.ctx, colors.disk.gradient);
    diskChart.options.scales.y.grid.color = colors.grid;
    diskChart.options.scales.x.grid.color = colors.grid;
    diskChart.options.plugins.tooltip.backgroundColor = colors.tooltip;

    netChart.data.datasets[0].borderColor = colors.net.border;
    netChart.data.datasets[0].backgroundColor = createGradient(netChart.ctx, colors.net.gradient);
    netChart.options.scales.y.grid.color = colors.grid;
    netChart.options.scales.x.grid.color = colors.grid;
    netChart.options.plugins.tooltip.backgroundColor = colors.tooltip;

    cpuChart.update();
    ramChart.update();
    diskChart.update();
    netChart.update();
}

function loadMonitoring() {
    const content = document.getElementById('content');
    content.innerHTML = `
        <h1 class="bounce-in">Мониторинг</h1>
        <div class="monitoring-header slide-up">
            <p>Local IP: <span id="localIP"></span></p>
            <p>External IP: <span id="externalIP"></span></p>
        </div>
        <div class="charts-grid">
            <div class="chart-card zoom-in stagger">
                <h3>CPU Usage</h3>
                <canvas id="cpuChart"></canvas>
                <div class="current-value" id="cpuValue">0%</div>
            </div>
            <div class="chart-card zoom-in stagger">
                <h3>RAM Usage</h3>
                <canvas id="ramChart"></canvas>
                <div class="current-value" id="ramValue">0%</div>
            </div>
            <div class="chart-card zoom-in stagger">
                <h3>Disk Usage</h3>
                <canvas id="diskChart"></canvas>
                <div class="current-value" id="diskValue">0%</div>
            </div>
            <div class="chart-card zoom-in stagger">
                <h3>Network</h3>
                <canvas id="netChart"></canvas>
                <div class="current-value" id="netValue">0 KB/s</div>
            </div>
        </div>
    `;

    const colors = getChartColors();

    // Initialize charts with enhanced options
    const chartOptions = {
        responsive: true,
        maintainAspectRatio: false,
        animation: { duration: 1000, easing: 'easeInOutQuad' },
        scales: {
            y: { beginAtZero: true, grid: { color: colors.grid } },
            x: { ticks: { autoSkip: true, maxTicksLimit: 20 }, grid: { color: colors.grid } }
        },
        plugins: {
            tooltip: {
                enabled: true,
                backgroundColor: colors.tooltip,
                titleColor: '#fff',
                bodyColor: '#fff',
                cornerRadius: 8,
                displayColors: false,
                callbacks: {
                    label: function(context) {
                        return context.parsed.y + (context.dataset.label.includes('%') ? '%' : ' KB/s');
                    }
                }
            },
            legend: { display: false }
        }
    };

    const cpuCtx = document.getElementById('cpuChart').getContext('2d');
    cpuChart = new Chart(cpuCtx, {
        type: 'line',
        data: {
            labels: [],
            datasets: [{
                label: 'CPU Usage (%)',
                data: [],
                borderColor: colors.cpu.border,
                backgroundColor: createGradient(cpuCtx, colors.cpu.gradient),
                tension: 0.4,
                fill: true,
                pointRadius: 4,
                pointHoverRadius: 6,
                pointBackgroundColor: colors.cpu.border,
                pointBorderColor: '#fff',
                pointBorderWidth: 2
            }]
        },
        options: { ...chartOptions, scales: { ...chartOptions.scales, y: { ...chartOptions.scales.y, max: 100 } } }
    });

    const ramCtx = document.getElementById('ramChart').getContext('2d');
    ramChart = new Chart(ramCtx, {
        type: 'line',
        data: {
            labels: [],
            datasets: [{
                label: 'RAM Usage (%)',
                data: [],
                borderColor: colors.ram.border,
                backgroundColor: createGradient(ramCtx, colors.ram.gradient),
                tension: 0.4,
                fill: true,
                pointRadius: 4,
                pointHoverRadius: 6,
                pointBackgroundColor: colors.ram.border,
                pointBorderColor: '#fff',
                pointBorderWidth: 2
            }]
        },
        options: { ...chartOptions, scales: { ...chartOptions.scales, y: { ...chartOptions.scales.y, max: 100 } } }
    });

    const diskCtx = document.getElementById('diskChart').getContext('2d');
    diskChart = new Chart(diskCtx, {
        type: 'line',
        data: {
            labels: [],
            datasets: [{
                label: 'Disk Usage (%)',
                data: [],
                borderColor: colors.disk.border,
                backgroundColor: createGradient(diskCtx, colors.disk.gradient),
                tension: 0.4,
                fill: true,
                pointRadius: 4,
                pointHoverRadius: 6,
                pointBackgroundColor: colors.disk.border,
                pointBorderColor: '#fff',
                pointBorderWidth: 2
            }]
        },
        options: { ...chartOptions, scales: { ...chartOptions.scales, y: { ...chartOptions.scales.y, max: 100 } } }
    });

    const netCtx = document.getElementById('netChart').getContext('2d');
    netChart = new Chart(netCtx, {
        type: 'line',
        data: {
            labels: [],
            datasets: [{
                label: 'Network (KB/s)',
                data: [],
                borderColor: colors.net.border,
                backgroundColor: createGradient(netCtx, colors.net.gradient),
                tension: 0.4,
                fill: true,
                pointRadius: 4,
                pointHoverRadius: 6,
                pointBackgroundColor: colors.net.border,
                pointBorderColor: '#fff',
                pointBorderWidth: 2
            }]
        },
        options: chartOptions
    });

    updateStats();
    setInterval(updateStats, 1000);
}

function updateStats() {
    fetch('/api/monitoring')
        .then(response => response.json())
        .then(data => {
            document.getElementById('localIP').textContent = data.local_ip;
            document.getElementById('externalIP').textContent = data.external_ip;

            document.getElementById('cpuValue').textContent = data.cpu + '%';
            document.getElementById('ramValue').textContent = data.ram + '%';
            document.getElementById('diskValue').textContent = data.disk + '%';
            document.getElementById('netValue').textContent = (data.net_in + data.net_out) + ' KB/s';

            const time = new Date().toLocaleTimeString();

            updateChart(cpuChart, time, data.cpu);
            updateChart(ramChart, time, data.ram);
            updateChart(diskChart, time, data.disk);
            updateChart(netChart, time, data.net_in + data.net_out);
        });
}

function updateChart(chart, time, value) {
    chart.data.labels.push(time);
    chart.data.datasets[0].data.push(value);
    if (chart.data.labels.length > 30) {
        chart.data.labels.shift();
        chart.data.datasets[0].data.shift();
    }
    chart.update('active');
}

let currentModule = '';
let currentScreenshotPaths = [];

function toggleMenu() {
    const menu = document.getElementById('nav-menu');
    const hamburger = document.querySelector('.hamburger');
    const content = document.getElementById('content');
    const isOpen = menu.classList.toggle('open');
    hamburger.classList.toggle('open', isOpen);
    hamburger.setAttribute('aria-expanded', isOpen);

    // Add blur to content when menu is open
    if (isOpen) {
        content.classList.add('blur');
    } else {
        content.classList.remove('blur');
    }

    // Add stagger fade-in animation to menu items
    const menuItems = menu.querySelectorAll('li');
    menuItems.forEach((item, index) => {
        if (isOpen) {
            item.style.animationDelay = `${index * 0.1}s`;
            item.classList.add('stagger-menu');
        } else {
            item.classList.remove('stagger-menu');
            item.style.animationDelay = '';
        }
    });
}

function toggleDropdown(event) {
    const dropdown = event.target.closest('.dropdown');
    dropdown.classList.toggle('open');
    // Close other dropdowns
    document.querySelectorAll('.dropdown').forEach(d => {
        if (d !== dropdown) d.classList.remove('open');
    });
}

// Close dropdowns when clicking outside
document.addEventListener('click', (e) => {
    if (!e.target.closest('.dropdown')) {
        document.querySelectorAll('.dropdown').forEach(d => d.classList.remove('open'));
    }
});

function setActive(module) {
    document.querySelectorAll('.nav-menu a').forEach(a => {
        a.classList.remove('active');
        a.removeAttribute('aria-current');
    });
    const activeLink = document.getElementById('nav-' + module);
    if (activeLink) {
        activeLink.classList.add('active');
        activeLink.setAttribute('aria-current', 'page');
    }
}

function loadModule(event, module) {
    if (event) event.preventDefault();
    if (currentModule === module) return;
    currentModule = module;

    const content = document.getElementById('content');

    // Add fade-out animation
    content.classList.add('fade-out');

    // Close menu
    const menu = document.getElementById('nav-menu');
    const hamburger = document.querySelector('.hamburger');
    menu.classList.remove('open');
    hamburger.classList.remove('open');
    hamburger.setAttribute('aria-expanded', 'false');
    content.classList.remove('blur');
    // Remove stagger animation
    const menuItems = menu.querySelectorAll('li');
    menuItems.forEach((item) => {
        item.classList.remove('stagger-menu');
        item.style.animationDelay = '';
    });

    setActive(module);
    history.pushState({module}, '', '/' + module + '#');

    setTimeout(() => {
        content.innerHTML = '<h1 class="fade-in">Loading...</h1>';
        content.classList.remove('fade-out');
        content.classList.add('fade-in');

        setTimeout(() => {
            if (module === 'processes') {
                loadProcesses();
            } else if (module === 'monitoring') {
                loadMonitoring();
            } else if (module === 'windows') {
                loadWindows();
            } else if (module === 'input') {
                loadInput();
            } else if (module === 'screenshots') {
                loadScreenshots();
            } else if (module === 'clipboard') {
                loadClipboard();
            } else if (module === 'logs') {
                loadLogs();
            } else if (module === 'control') {
                loadControl();
            }
            content.classList.add('fade-in');
        }, 300);
    }, 300);
}

// Handle back/forward
window.addEventListener('popstate', (event) => {
    if (event.state && event.state.module) {
        loadModule(null, event.state.module);
    }
});

// Theme toggle
function toggleTheme() {
    document.body.classList.toggle('dark');
    localStorage.setItem('theme', document.body.classList.contains('dark') ? 'dark' : 'light');
    updateChartColors(); // Update chart colors when theme changes
    toggleMenu(); // Close menu after toggling theme
}

// Keyboard navigation
document.addEventListener('keydown', (e) => {
    // Navigation keyboard support
    const navMenu = document.getElementById('nav-menu');
    const focusableElements = navMenu.querySelectorAll('a[tabindex="0"], button[tabindex="0"]');
    const activeElement = document.activeElement;
    if (navMenu.contains(activeElement)) {
        let index = Array.from(focusableElements).indexOf(activeElement);
        if (e.key === 'ArrowRight' || e.key === 'ArrowDown') {
            e.preventDefault();
            index = (index + 1) % focusableElements.length;
            focusableElements[index].focus();
        } else if (e.key === 'ArrowLeft' || e.key === 'ArrowUp') {
            e.preventDefault();
            index = (index - 1 + focusableElements.length) % focusableElements.length;
            focusableElements[index].focus();
        }
    }
});

// Load theme on page load
window.addEventListener('load', () => {
    if (localStorage.getItem('theme') === 'dark') {
        document.body.classList.add('dark');
    }
    let path = window.location.pathname.substring(1);
    if (path.endsWith('#')) {
        path = path.slice(0, -1);
    }
    if (path && path !== 'login') {
        loadModule(null, path);
    } else if (path !== 'login' && path !== '') {
        loadModule(null, 'processes');
    }
});

// Scroll to top functionality
function scrollToTop() {
    window.scrollTo({ top: 0, behavior: 'smooth' });
}

window.addEventListener('scroll', () => {
    const scrollToTopBtn = document.getElementById('scrollToTop');
    if (window.scrollY > 100) {
        scrollToTopBtn.classList.add('show');
    } else {
        scrollToTopBtn.classList.remove('show');
    }
});

let currentWindows = [];

function loadWindows() {
    const content = document.getElementById('content');
    content.innerHTML = `
        <h1 class="bounce-in">Окна</h1>
        <div class="card zoom-in">
            <div class="window-controls">
                <button onclick="minimizeAllWindows()" class="bounce-in">Свернуть всё</button>
                <button onclick="showAllHiddenWindows()" class="bounce-in">Показать всё скрытое</button>
                <button onclick="closeAllWindows()" class="bounce-in">Закрыть всё</button>
            </div>
            <div class="file-controls">
                <input type="text" id="windowSearch" placeholder="Поиск по заголовку" oninput="filterWindows()" class="slide-in">
                <select id="windowSort" onchange="sortWindows()" class="slide-in">
                    <option value="hwnd">По HWND</option>
                    <option value="title">По заголовку</option>
                    <option value="class">По классу</option>
                </select>
            </div>
        </div>
        <div class="card table-card zoom-in" id="windowList"></div>
    `;
    fetch('/api/windows')
        .then(response => response.json())
        .then(data => {
            currentWindows = data;
            renderWindowList();
        });
}

function filterWindows() {
    const search = document.getElementById('windowSearch').value.toLowerCase();
    const filtered = currentWindows.filter(win => win.title.toLowerCase().includes(search));
    renderWindowList(filtered);
}

function sortWindows() {
    const sortBy = document.getElementById('windowSort').value;
    currentWindows.sort((a, b) => {
        if (sortBy === 'hwnd') return a.hwnd - b.hwnd;
        if (sortBy === 'title') return a.title.localeCompare(b.title);
        if (sortBy === 'class') return a.class.localeCompare(b.class);
        return 0;
    });
    renderWindowList();
}

function renderWindowList(items = currentWindows) {
    const list = document.getElementById('windowList');
    list.innerHTML = '<table><tr><th>HWND</th><th>Заголовок</th><th>Класс</th><th>Действия</th></tr>' +
        items.map((win, index) => `
            <tr class="window-stagger" style="animation-delay: ${index * 0.05}s;">
                <td>${win.hwnd}</td>
                <td>${win.title}</td>
                <td>${win.class}</td>
                <td class="action-cell">
                    <button onclick="hideWindow(${win.hwnd})" class="action-btn">Скрыть</button>
                    <button onclick="showWindow(${win.hwnd})" class="action-btn">Показать</button>
                    <button onclick="minimizeWindow(${win.hwnd})" class="action-btn">Свернуть</button>
                    <button onclick="maximizeWindow(${win.hwnd})" class="action-btn">Развернуть</button>
                    <button onclick="focusWindow(${win.hwnd})" class="action-btn">Фокус</button>
                    <button onclick="closeWindow(${win.hwnd})" class="action-btn">✕ Закрыть</button>
                </td>
            </tr>
        `).join('') + '</table>';
}

function hideWindow(hwnd) {
    fetch('/api/windows/hide', {method: 'POST', headers: {'Content-Type': 'application/json', 'X-CSRFToken': csrfToken}, body: JSON.stringify({hwnd})});
}

function showWindow(hwnd) {
    fetch('/api/windows/show', {method: 'POST', headers: {'Content-Type': 'application/json', 'X-CSRFToken': csrfToken}, body: JSON.stringify({hwnd})});
}

function minimizeWindow(hwnd) {
    fetch('/api/windows/minimize', {method: 'POST', headers: {'Content-Type': 'application/json', 'X-CSRFToken': csrfToken}, body: JSON.stringify({hwnd})});
}

function maximizeWindow(hwnd) {
    fetch('/api/windows/maximize', {method: 'POST', headers: {'Content-Type': 'application/json', 'X-CSRFToken': csrfToken}, body: JSON.stringify({hwnd})});
}

function focusWindow(hwnd) {
    fetch('/api/windows/focus', {method: 'POST', headers: {'Content-Type': 'application/json', 'X-CSRFToken': csrfToken}, body: JSON.stringify({hwnd})});
}

function closeWindow(hwnd) {
    fetch('/api/windows/close', {method: 'POST', headers: {'Content-Type': 'application/json', 'X-CSRFToken': csrfToken}, body: JSON.stringify({hwnd})});
}

function minimizeAllWindows() {
    currentWindows.forEach(win => minimizeWindow(win.hwnd));
}

function showAllHiddenWindows() {
    currentWindows.forEach(win => showWindow(win.hwnd));
}

function closeAllWindows() {
    if (confirm('Вы уверены, что хотите закрыть все окна?')) {
        currentWindows.forEach(win => closeWindow(win.hwnd));
    }
}

function loadInput() {
    const content = document.getElementById('content');
    content.innerHTML = `
        <h1 class="bounce-in">Клавиатура / Мышь</h1>
        <div class="card zoom-in">
            <h3>Мышь</h3>
            <button onclick="getMousePosition()" class="bounce-in">Получить позицию</button>
            <span id="currentPos"></span><br><br>
            Абсолютное перемещение:<br>
            X: <input type="number" id="mouseX" class="slide-in">
            Y: <input type="number" id="mouseY" class="slide-in">
            <button onclick="moveMouse()" class="bounce-in">Переместить</button><br><br>
            Относительное перемещение:<br>
            <input type="number" id="movePixels" value="10" min="1" class="slide-in"> пикселей<br>
            <button onclick="moveRelative(0, -parseInt(document.getElementById('movePixels').value))" class="bounce-in">Вверх</button>
            <button onclick="moveRelative(0, parseInt(document.getElementById('movePixels').value))" class="bounce-in">Вниз</button>
            <button onclick="moveRelative(-parseInt(document.getElementById('movePixels').value), 0)" class="bounce-in">Влево</button>
            <button onclick="moveRelative(parseInt(document.getElementById('movePixels').value), 0)" class="bounce-in">Вправо</button><br><br>
            <button onclick="clickMouse('left')" class="bounce-in">ЛКМ</button>
            <button onclick="clickMouse('right')" class="bounce-in">ПКМ</button><br><br>
            Скролл:<br>
            Интенсивность: <input type="range" id="scrollIntensity" min="1" max="10" value="1" class="slide-in"> <span id="intensityValue">1</span><br>
            <button onmousedown="startScroll(1)" onmouseup="stopScroll()" ontouchstart="startScroll(1)" ontouchend="stopScroll()" class="bounce-in">Вверх</button>
            <button onmousedown="startScroll(-1)" onmouseup="stopScroll()" ontouchstart="startScroll(-1)" ontouchend="stopScroll()" class="bounce-in">Вниз</button>
        </div>
        <div class="card zoom-in">
            <h3>Клавиатура</h3>
            <input type="text" id="textInput" placeholder="Текст" class="slide-in">
            <button onclick="typeText()" class="bounce-in">Ввести текст</button><br><br>
            <input type="text" id="keyInput" placeholder="Клавиша" class="slide-in">
            <button onclick="pressKey()" class="bounce-in">Нажать клавишу</button><br><br>
            <h4>Список клавиш:</h4>
            <div style="display: grid; grid-template-columns: repeat(auto-fill, minmax(100px, 1fr)); gap: 5px;">
                ${['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z',
                   '0','1','2','3','4','5','6','7','8','9',
                   'f1','f2','f3','f4','f5','f6','f7','f8','f9','f10','f11','f12',
                   'escape','tab','capslock','shift','ctrl','alt','space','enter','backspace','delete',
                   'up','down','left','right','home','end','pageup','pagedown'].map(key => `<button onclick="pressKey('${key}')" class="bounce-in">${key}</button>`).join('')}
            </div>
        </div>
    `;
    document.getElementById('scrollIntensity').addEventListener('input', function() {
        document.getElementById('intensityValue').textContent = this.value;
    });
}

function getMousePosition() {
    fetch('/api/input/mouse/position')
        .then(response => response.json())
        .then(data => {
            document.getElementById('currentPos').textContent = `X: ${data.x}, Y: ${data.y}`;
        });
}

function moveMouse() {
    const x = document.getElementById('mouseX').value;
    const y = document.getElementById('mouseY').value;
    fetch('/api/input/mouse/move', {method: 'POST', headers: {'Content-Type': 'application/json', 'X-CSRFToken': csrfToken}, body: JSON.stringify({x: parseInt(x), y: parseInt(y)})});
}

function moveRelative(dx, dy) {
    fetch('/api/input/mouse/move_relative', {method: 'POST', headers: {'Content-Type': 'application/json', 'X-CSRFToken': csrfToken}, body: JSON.stringify({dx, dy})});
}

function clickMouse(button) {
    fetch('/api/input/mouse/click', {method: 'POST', headers: {'Content-Type': 'application/json', 'X-CSRFToken': csrfToken}, body: JSON.stringify({button})});
}

let scrollInterval;

function startScroll(direction) {
    const intensity = parseInt(document.getElementById('scrollIntensity').value);
    scrollInterval = setInterval(() => {
        fetch('/api/input/mouse/scroll', {method: 'POST', headers: {'Content-Type': 'application/json', 'X-CSRFToken': csrfToken}, body: JSON.stringify({clicks: direction, intensity})});
    }, 100);
}

function stopScroll() {
    clearInterval(scrollInterval);
}

function scrollMouse(clicks) {
    const intensity = parseInt(document.getElementById('scrollIntensity').value);
    fetch('/api/input/mouse/scroll', {method: 'POST', headers: {'Content-Type': 'application/json', 'X-CSRFToken': csrfToken}, body: JSON.stringify({clicks, intensity})});
}

function typeText() {
    const text = document.getElementById('textInput').value;
    fetch('/api/input/keyboard/type', {method: 'POST', headers: {'Content-Type': 'application/json', 'X-CSRFToken': csrfToken}, body: JSON.stringify({text})});
}

function pressKey() {
    const key = document.getElementById('keyInput').value;
    fetch('/api/input/keyboard/press', {method: 'POST', headers: {'Content-Type': 'application/json', 'X-CSRFToken': csrfToken}, body: JSON.stringify({key})});
}

function loadScreenshots() {
    const content = document.getElementById('content');
    content.innerHTML = `
        <h1 class="bounce-in">Скриншоты</h1>
        <div class="card screenshot-card zoom-in" style="max-width: 1000px; margin: 0 auto; padding: 30px;">
            <div class="screenshot-controls" style="display: flex; flex-wrap: wrap; justify-content: center; gap: 20px; margin-bottom: 30px;">
                <button onclick="takeScreenshot()" id="screenshot-btn" class="btn-screenshot bounce-in" title="Создать скриншот">
                    <i class="fas fa-camera"></i> Создать скриншот
                </button>
            </div>
            <div class="screenshot-options slide-up" style="display: flex; flex-wrap: wrap; justify-content: center; gap: 20px; margin-bottom: 20px; align-items: center;">
                <div class="option-group">
                    <label for="monitor-select" style="font-weight: bold; margin-right: 10px;">Выбор монитора:</label>
                    <select id="monitor-select" title="Выберите монитор" style="padding: 8px; border-radius: 4px; border: 1px solid #ccc;" class="slide-in">
                        <option value="all">Все мониторы</option>
                    </select>
                </div>
                <div class="option-group">
                    <label for="cursor-checkbox" title="Показать крестик на месте курсора мыши">
                        <input type="checkbox" id="cursor-checkbox" style="margin-right: 8px;" class="slide-in"> Показать курсор
                    </label>
                </div>
            </div>
            <div id="loadingIndicator" style="text-align: center; display: none; margin: 20px 0;">
                <i class="fas fa-spinner fa-spin" style="font-size: 24px; color: #007bff;"></i>
                <p>Создание скриншота...</p>
            </div>
            <div id="errorMessage" style="display: none; background: #f8d7da; color: #721c24; padding: 10px; border-radius: 4px; margin: 10px 0; text-align: center;"></div>
            <div class="screenshot-display" style="text-align: center;">
                <div id="screenshots-container" style="display: flex; flex-wrap: wrap; justify-content: center; gap: 10px;"></div>
                <div id="downloadSection" style="margin-top: 15px; display: none;">
                    <button onclick="downloadAllScreenshots()" class="btn-download bounce-in" title="Скачать все скриншоты">
                        <i class="fas fa-download"></i> Скачать все
                    </button>
                </div>
            </div>
        </div>
    `;
    loadMonitors();
}

function loadMonitors() {
    fetch('/api/monitors')
        .then(response => response.json())
        .then(data => {
            const select = document.getElementById('monitor-select');
            // Clear existing options except "all"
            select.innerHTML = '<option value="all">Все мониторы</option>';
            data.forEach(monitor => {
                const option = document.createElement('option');
                option.value = monitor.id;
                option.textContent = `${monitor.name} (${monitor.bounds.width}x${monitor.bounds.height})`;
                select.appendChild(option);
            });
        })
        .catch(err => {
            console.error('Error loading monitors:', err);
            showError('Ошибка загрузки списка мониторов');
        });
}

function takeScreenshot() {
    const select = document.getElementById("monitor-select");
    const selectedValue = select.value;
    const showCursor = document.getElementById("cursor-checkbox").checked;

    let mode, monitorId;
    if (selectedValue === "all") {
        mode = "all";
        monitorId = null;
    } else {
        mode = "selected";
        monitorId = parseInt(selectedValue);
    }

    const data = {
        mode: mode,
        show_cursor: showCursor
    };
    if (monitorId !== null) {
        data.monitor_id = monitorId;
    }

    // Show loading
    document.getElementById('loadingIndicator').style.display = 'block';
    document.getElementById('errorMessage').style.display = 'none';
    document.getElementById('screenshot-btn').disabled = true;

    fetch("/api/screenshot", {
        method: "POST",
        headers: {'Content-Type': 'application/json', 'X-CSRFToken': csrfToken},
        body: JSON.stringify(data)
    })
        .then(response => {
            if (response.ok) {
                return response.json();
            } else {
                return response.json().then(err => { throw new Error(err.error || `HTTP ${response.status}`); });
            }
        })
        .then(data => {
            currentScreenshotPaths = data.paths;
            const container = document.getElementById('screenshots-container');
            container.innerHTML = '';
            data.paths.forEach(path => {
                const img = document.createElement('img');
                img.src = path + '?' + new Date().getTime();
                img.style.maxWidth = '45%';
                img.style.border = '2px solid #ddd';
                img.style.borderRadius = '8px';
                img.style.boxShadow = '0 4px 8px rgba(0,0,0,0.1)';
                container.appendChild(img);
            });
            document.getElementById('downloadSection').style.display = 'block';
        })
        .catch(err => {
            console.error('Error taking screenshot:', err);
            showError('Ошибка создания скриншота: ' + err.message);
        })
        .finally(() => {
            // Hide loading
            document.getElementById('loadingIndicator').style.display = 'none';
            document.getElementById('screenshot-btn').disabled = false;
        });
}

function showError(message) {
    const errorDiv = document.getElementById('errorMessage');
    errorDiv.textContent = message;
    errorDiv.style.display = 'block';
}

function downloadAllScreenshots() {
    currentScreenshotPaths.forEach(path => {
        const a = document.createElement('a');
        a.href = path;
        a.download = path.split('/').pop();
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
    });
}

function loadClipboard() {
    const content = document.getElementById('content');
    content.innerHTML = `
        <h1 class="bounce-in">Буфер обмена</h1>
        <div class="card zoom-in">
            <button onclick="readClipboard()" class="bounce-in">Прочитать</button>
            <textarea id="clipboardText" placeholder="Текст" class="slide-in"></textarea>
            <button onclick="writeClipboard()" class="bounce-in">Записать</button>
            <button onclick="clearClipboard()" class="bounce-in">Очистить</button>
        </div>
    `;
}

function readClipboard() {
    fetch('/api/clipboard/read')
        .then(response => response.json())
        .then(data => document.getElementById('clipboardText').value = data.text);
}

function writeClipboard() {
    const text = document.getElementById('clipboardText').value;
    fetch('/api/clipboard/write', {method: 'POST', headers: {'Content-Type': 'application/json', 'X-CSRFToken': csrfToken}, body: JSON.stringify({text})});
}

function clearClipboard() {
    fetch('/api/clipboard/clear', {method: 'POST', headers: {'X-CSRFToken': csrfToken}});
}

let currentLogs = [];
let currentOffset = 0;
const pageSize = 15;
let hasMore = true;
let currentSearch = '';
let currentLevelFilter = '';

function loadLogs() {
    const content = document.getElementById('content');
    content.innerHTML = `
        <h1 class="bounce-in">Логи</h1>
        <div class="card zoom-in">
            <div class="file-controls">
                <input type="text" id="logSearch" placeholder="Поиск по сообщению" oninput="onSearchChange()" class="slide-in">
                <select id="logLevelFilter" onchange="onFilterChange()" class="slide-in">
                    <option value="">Все уровни</option>
                    <option value="INFO">INFO</option>
                    <option value="WARNING">WARNING</option>
                    <option value="ERROR">ERROR</option>
                </select>
                <select id="logSort" onchange="sortLogs()" class="slide-in">
                    <option value="time_desc">По времени (новые сверху)</option>
                    <option value="time_asc">По времени (старые сверху)</option>
                    <option value="level">По уровню</option>
                </select>
            </div>
        </div>
        <div class="card table-card zoom-in" id="logsTable"></div>
        <div id="loadMoreSection" style="text-align: center; margin-top: 20px; display: none;">
            <button onclick="loadMoreLogs()" class="btn-download bounce-in" id="loadMoreBtn">Загрузить еще +15</button>
        </div>
        <div id="downloadSection" style="text-align: center; margin-top: 20px;">
            <button onclick="clearLogs()" class="btn-download bounce-in" style="background: #dc3545; margin-right: 10px;">Очистить логи</button>
            <button onclick="downloadLogs()" class="btn-download bounce-in">Скачать все логи</button>
        </div>
    `;
    content.classList.add('fade-in');
    currentOffset = 0;
    currentLogs = [];
    currentSearch = '';
    currentLevelFilter = '';
    loadLogsData();
}

function onSearchChange() {
    currentSearch = document.getElementById('logSearch').value;
    resetAndLoad();
}

function onFilterChange() {
    currentLevelFilter = document.getElementById('logLevelFilter').value;
    resetAndLoad();
}

function resetAndLoad() {
    currentOffset = 0;
    currentLogs = [];
    loadLogsData();
}

function loadLogsData() {
    const params = new URLSearchParams({
        limit: pageSize,
        offset: currentOffset,
        search: currentSearch,
        level: currentLevelFilter
    });
    fetch('/api/logs?' + params)
        .then(response => response.json())
        .then(data => {
            const newLogs = parseLogs(data.logs);
            currentLogs = currentLogs.concat(newLogs);
            hasMore = currentLogs.length < data.total;
            document.getElementById('loadMoreSection').style.display = hasMore ? 'block' : 'none';
            renderLogsTable();
        });
}

function loadMoreLogs() {
    currentOffset += pageSize;
    loadLogsData();
}

function parseLogs(logLines) {
    return logLines.map(line => {
        const match = line.match(/^(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2},\d{3}) - (\w+) - (.+)$/);
        if (match) {
            return {
                time: match[1],
                level: match[2],
                message: match[3]
            };
        }
        return {
            time: '',
            level: 'UNKNOWN',
            message: line
        };
    });
}

function sortLogs() {
    const sortBy = document.getElementById('logSort').value;
    currentLogs.sort((a, b) => {
        if (sortBy === 'time_desc') return new Date(b.time) - new Date(a.time);
        if (sortBy === 'time_asc') return new Date(a.time) - new Date(b.time);
        if (sortBy === 'level') return a.level.localeCompare(b.level);
        return 0;
    });
    renderLogsTable();
}

function renderLogsTable(items = currentLogs) {
    const table = document.getElementById('logsTable');
    table.innerHTML = '<table><tr><th>Время</th><th>Уровень</th><th>Сообщение</th></tr>' +
        items.map((log, index) => `
            <tr class="log-stagger" style="animation-delay: ${index * 0.02}s;">
                <td>${log.time}</td>
                <td class="log-level log-${log.level.toLowerCase()}">${log.level}</td>
                <td>${log.message}</td>
            </tr>
        `).join('') + '</table>';
}

function clearLogs() {
    if (confirm('Вы уверены, что хотите очистить все логи?')) {
        fetch('/api/logs/clear', { method: 'POST', headers: {'X-CSRFToken': csrfToken} })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    loadLogs(); // Reload logs
                } else {
                    alert('Ошибка очистки логов');
                }
            });
    }
}

function downloadLogs() {
    const a = document.createElement('a');
    a.href = '/api/logs/download';
    a.download = 'actions.log';
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
}

// Server-side screenshot-based implementation for screen control
let controlInterval = null;
let controlFps = 30;
let controlShowCursor = true;
let controlMonitorId = 1;
let controlFrameCount = 0;
let controlFpsDisplay = 0;
let controlFpsUpdateTime = 0;

function loadControl() {
    const content = document.getElementById('content');
    content.innerHTML = `
        <h1 class="bounce-in">Управление</h1>
        <div class="control-container" style="display: flex; flex-direction: column; align-items: center; gap: 20px;">
            <div class="control-panel" style="display: flex; flex-wrap: wrap; justify-content: center; gap: 15px; padding: 20px; background: var(--card-bg); border-radius: 8px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); width: 100%; max-width: 800px;">
                <div class="monitor-control" style="display: flex; align-items: center; gap: 10px;">
                    <label for="monitorSelect" style="font-weight: bold;">Монитор:</label>
                    <select id="monitorSelect" onchange="changeMonitor()" style="padding: 5px; border-radius: 4px; border: 1px solid #ccc;">
                        <option value="1">Монитор 1</option>
                    </select>
                </div>
                <button id="startStopBtn" onclick="toggleStream()" class="bounce-in" style="padding: 10px 20px; background: #28a745; color: white; border: none; border-radius: 5px; cursor: pointer;">Начать</button>
                <div class="fps-control" style="display: flex; align-items: center; gap: 10px;">
                    <label for="fpsSelect" style="font-weight: bold;">FPS:</label>
                    <select id="fpsSelect" onchange="changeFps()" style="padding: 5px; border-radius: 4px; border: 1px solid #ccc;">
                        <option value="15">15</option>
                        <option value="30" selected>30</option>
                        <option value="60">60</option>
                        <option value="custom">Кастомный</option>
                    </select>
                    <input type="number" id="customFps" min="1" max="120" value="30" onchange="changeCustomFps()" style="width: 60px; padding: 5px; border-radius: 4px; border: 1px solid #ccc; display: none;">
                </div>
                <div class="cursor-control" style="display: flex; align-items: center; gap: 10px;">
                    <label for="showCursor" style="font-weight: bold;">Показывать курсор:</label>
                    <input type="checkbox" id="showCursor" checked onchange="toggleCursor()">
                </div>
                <div class="fps-display" style="font-weight: bold;">Реальный FPS: <span id="realFps">0</span></div>
            </div>
            <div class="video-panel" style="position: relative; border: 2px solid #ddd; border-radius: 8px; overflow: hidden; max-width: 70%; max-height: 70vh;">
                <img id="controlImage" style="display: block; max-width: 100%; max-height: 100%;" alt="Screen stream">
                <div id="fpsOverlay" style="position: absolute; top: 10px; right: 10px; background: rgba(0,0,0,0.7); color: white; padding: 5px 10px; border-radius: 4px; font-size: 14px;">FPS: 0</div>
            </div>
            <div id="errorMessage" style="display: none; background: #f8d7da; color: #721c24; padding: 10px; border-radius: 4px; max-width: 800px;"></div>
        </div>
    `;
    content.classList.add('fade-in');

    loadMonitors();
}

function loadMonitors() {
    fetch('/api/control/monitors')
        .then(response => response.json())
        .then(data => {
            const select = document.getElementById('monitorSelect');
            select.innerHTML = '';
            data.forEach(monitor => {
                const option = document.createElement('option');
                option.value = monitor.id;
                option.textContent = monitor.name;
                select.appendChild(option);
            });
            controlMonitorId = data[0]?.id || 1;
        })
        .catch(err => {
            console.error('Error loading monitors:', err);
            showControlError('Ошибка загрузки списка мониторов');
        });
}

function changeMonitor() {
    controlMonitorId = parseInt(document.getElementById('monitorSelect').value);
}

function toggleStream() {
    if (controlInterval) {
        stopStream();
    } else {
        startStream();
    }
}

function startStream() {
    controlFrameCount = 0;
    controlFpsDisplay = 0;
    controlFpsUpdateTime = performance.now();
    controlInterval = setInterval(fetchFrame, 1000 / controlFps);
    document.getElementById('startStopBtn').textContent = 'Остановить';
    document.getElementById('startStopBtn').style.background = '#dc3545';
}

function stopStream() {
    if (controlInterval) {
        clearInterval(controlInterval);
        controlInterval = null;
    }
    document.getElementById('startStopBtn').textContent = 'Начать';
    document.getElementById('startStopBtn').style.background = '#28a745';
    document.getElementById('realFps').textContent = '0';
    document.getElementById('fpsOverlay').textContent = 'FPS: 0';
}

function fetchFrame() {
    fetch('/api/control/stream', {
        method: 'POST',
        headers: {'Content-Type': 'application/json', 'X-CSRFToken': csrfToken},
        body: JSON.stringify({
            monitor_id: controlMonitorId,
            show_cursor: controlShowCursor
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.error) {
            showControlError(data.error);
            stopStream();
            return;
        }
        document.getElementById('controlImage').src = data.image;
        controlFrameCount++;
        const now = performance.now();
        if (now - controlFpsUpdateTime >= 1000) {
            controlFpsDisplay = Math.round(controlFrameCount / ((now - controlFpsUpdateTime) / 1000));
            document.getElementById('realFps').textContent = controlFpsDisplay;
            document.getElementById('fpsOverlay').textContent = 'FPS: ' + controlFpsDisplay;
            controlFrameCount = 0;
            controlFpsUpdateTime = now;
        }
        showControlError('');
    })
    .catch(err => {
        console.error('Error fetching frame:', err);
        showControlError('Ошибка получения кадра');
        stopStream();
    });
}

function changeFps() {
    const select = document.getElementById('fpsSelect');
    const customInput = document.getElementById('customFps');
    if (select.value === 'custom') {
        customInput.style.display = 'inline';
        controlFps = parseInt(customInput.value) || 30;
    } else {
        customInput.style.display = 'none';
        controlFps = parseInt(select.value);
    }
    if (controlInterval) {
        stopStream();
        startStream();
    }
}

function changeCustomFps() {
    const value = parseInt(document.getElementById('customFps').value);
    if (value >= 1 && value <= 120) {
        controlFps = value;
        if (controlInterval) {
            stopStream();
            startStream();
        }
    } else {
        document.getElementById('customFps').value = controlFps;
    }
}

function toggleCursor() {
    controlShowCursor = document.getElementById('showCursor').checked;
}

function showControlError(message) {
    const errorDiv = document.getElementById('errorMessage');
    if (message) {
        errorDiv.textContent = message;
        errorDiv.style.display = 'block';
    } else {
        errorDiv.style.display = 'none';
    }
}
