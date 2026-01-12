document.addEventListener('DOMContentLoaded', () => {
    // Configuration
    const CSV_URL = 'musicbook_songs.csv';

    // DOM Elements
    const tableBody = document.getElementById('musicTableBody');
    const loadingOverlay = document.getElementById('loadingOverlay');
    const searchInput = document.getElementById('searchInput');
    const volumeSelect = document.getElementById('volumeSelect');
    const totalCountEl = document.getElementById('totalCount');
    const headers = document.querySelectorAll('th[data-sort]');

    // State
    let allData = [];
    let currentData = [];
    let sortCol = '册別'; // Default sort
    let sortAsc = false; // Descending by default for volume? Let's stick to natural order first

    // CSV Parser
    const parseCSV = (text) => {
        const lines = text.split('\n').filter(line => line.trim() !== '');
        const headers = lines[0].split(',');

        return lines.slice(1).map(line => {
            // Handle simple CSV parsing (assuming no commas in fields for now based on previous simple structure)
            // If fields contain commas, regex split would be needed: line.split(/,(?=(?:(?:[^"]*"){2})*[^"]*$)/)
            const values = line.split(',');

            // Reconstruct object based on headers: 曲名,演唱歌手,冊別,頁別,備註
            // Map index to known fields to ensure safety if order changes
            // But for this specific CSV we generated: 0:書名, 1:曲名, 2:演唱歌手, 3:冊別, 4:頁別, 5:備註
            return {
                book: values[0] || '',
                song: values[1] || '',
                singer: values[2] || '',
                volume: values[3] || '',
                page: values[4] || '',
                remark: values[5] || ''
            };
        });
    };

    // Initialize
    const init = async () => {
        try {
            const response = await fetch(CSV_URL);
            if (!response.ok) throw new Error('Failed to load CSV');

            const text = await response.text();
            allData = parseCSV(text);
            currentData = [...allData];

            // Populate Volume Filter
            populateVolumes();

            // Initial Render
            renderTable(currentData);
            updateCount(currentData.length);

            // Hide Loader
            loadingOverlay.classList.add('hidden');

        } catch (error) {
            console.error('Error:', error);
            loadingOverlay.innerHTML = `<p style="color:red">無法載入資料庫<br>請確認是否使用 Local Server 開啟</p>`;
        }
    };

    // Render Table
    const renderTable = (data) => {
        // Clear existing
        tableBody.innerHTML = '';

        // Optimize rendering for large datasets? 
        // 9000 rows might be heavy. Let's render first 100 initially or just render all if browser handles it.
        // Chrome handles 9000 simple rows okay, but let's limit render for performance if needed. 
        // For now, render top 500 for speed, show more on scroll? Or just render all.
        // Let's render all for "Check all" requirement, but maybe use a fragment.

        // Performance check: 9000 rows is heavy. 
        // Let's implement lazy rendering or simple Limit cap for safety?
        // User asked for "Check All" (全部瀏覽).

        const fragment = document.createDocumentFragment();

        // Render max 2000 rows for DOM performance protection? 
        // Or render chunks. Let's try full render.

        // Limit to 5000 initially to prevent crash? 
        // No, user wants ALL. Let's assume modern browser.

        const displayData = data.slice(0, 2000); // Soft limit for initial UX? 
        // Better: Render first 100 immediately, then timeout render others?
        // For simplicity: Render all.

        data.forEach(row => {
            const tr = document.createElement('tr');
            tr.innerHTML = `
                <td>${row.book}</td>
                <td>${row.song}</td>
                <td>${row.singer}</td>
                <td><span class="badge volume">${row.volume}</span></td>
                <td>${row.page}</td>
                <td class="remark">${row.remark}</td>
            `;
            fragment.appendChild(tr);
        });

        tableBody.appendChild(fragment);

        if (data.length === 0) {
            tableBody.innerHTML = '<tr><td colspan="6" style="text-align:center; padding: 40px;">沒有找到符合的歌曲</td></tr>';
        }
    };

    // Populate Volume Filter with Unique Values
    const populateVolumes = () => {
        // Extract unique volumes and sort numericly descending
        const volumes = [...new Set(allData.map(item => item.volume))]
            .filter(v => v)
            .sort((a, b) => parseInt(b) - parseInt(a));

        volumes.forEach(vol => {
            const option = document.createElement('option');
            option.value = vol;
            option.textContent = `第 ${vol} 冊`;
            volumeSelect.appendChild(option);
        });
    };

    // Filter Logic
    const filterData = () => {
        const searchTerm = searchInput.value.toLowerCase().trim();
        const selectedVolume = volumeSelect.value;

        currentData = allData.filter(item => {
            const matchSearch = (
                item.song.toLowerCase().includes(searchTerm) ||
                item.singer.toLowerCase().includes(searchTerm)
            );
            const matchVolume = selectedVolume === 'all' || item.volume === selectedVolume;

            return matchSearch && matchVolume;
        });

        updateCount(currentData.length);
        renderTable(currentData);
    };

    // Update Count
    const updateCount = (count) => {
        totalCountEl.textContent = `共找到 ${count} 首歌曲`;
    };

    // Event Listeners
    searchInput.addEventListener('input', () => {
        // Debounce?
        filterData();
    });

    volumeSelect.addEventListener('change', filterData);

    // sorting (Simple implementation)
    headers.forEach(th => {
        th.addEventListener('click', () => {
            const key = th.dataset.sort;
            sortAsc = !sortAsc;

            currentData.sort((a, b) => {
                let valA = a[key];
                let valB = b[key];

                // Numeric sort for volume/page
                if (key === 'volume' || key === 'page') {
                    return sortAsc ? parseInt(valA) - parseInt(valB) : parseInt(valB) - parseInt(valA);
                }

                // String sort
                return sortAsc ? valA.localeCompare(valB) : valB.localeCompare(valA);
            });

            renderTable(currentData);
        });
    });

    // Start
    init();
});
