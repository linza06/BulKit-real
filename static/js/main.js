
document.addEventListener('DOMContentLoaded', () => {
    loadFonts();
    setupDropZones();
    setupColorSwatches();
    setupFormatChips();
});

async function loadFonts() {
    try {
        const res = await fetch('/get_fonts');
        const data = await res.json();
        const sel = document.getElementById('font_name');
        sel.innerHTML = '';
        data.fonts.forEach(f => {
            const opt = document.createElement('option');
            opt.value = f;
            opt.textContent = f.replace(/\.ttf$/i, '').replace(/_/g, ' ');
            sel.appendChild(opt);
        });
    } catch {
        document.getElementById('font_name').innerHTML = '<option value="arial.ttf">Arial</option>';
    }
}


function setupDropZones() {
   
    const imgZones = [
        { inputId: 'first_template',       zoneId: 'zone-first',  icon: '🥇', badge: '<span class="dz-badge badge-1st">1st Place</span>' },
        { inputId: 'second_template',      zoneId: 'zone-second', icon: '🥈', badge: '<span class="dz-badge badge-2nd">2nd Place</span>' },
        { inputId: 'third_template',       zoneId: 'zone-third',  icon: '🥉', badge: '<span class="dz-badge badge-3rd">3rd Place</span>' },
        { inputId: 'participant_template', zoneId: 'zone-part',   icon: '🎓', badge: '<span class="dz-badge badge-part">Participant</span>' },
    ];

    imgZones.forEach(({ inputId, zoneId }) => {
        const input = document.getElementById(inputId);
        const zone  = document.getElementById(zoneId);
        if (!input || !zone) return;

        const thumb    = zone.querySelector('.dz-thumbnail');
        const thumbImg = thumb?.querySelector('img');
        const thumbBar = thumb?.querySelector('.dz-thumbnail-bar span');
        const clearBtn = thumb?.querySelector('.dz-thumbnail-bar button');

        input.addEventListener('change', () => {
            const file = input.files[0];
            if (!file) return;
            showImagePreview(file, zone, thumbImg, thumbBar);
        });

        clearBtn?.addEventListener('click', (e) => {
            e.stopPropagation();
            e.preventDefault();
            clearZone(input, zone, thumbImg);
        });

        setupDragDrop(zone, input, (file) => {
            showImagePreview(file, zone, thumbImg, thumbBar);
        });
    });


    const csvInput = document.getElementById('csv_file');
    const csvZone  = document.getElementById('zone-csv');
    if (csvInput && csvZone) {
        const infoEl   = csvZone.querySelector('.dz-file-info');
        const nameEl   = csvZone.querySelector('.dz-file-info-name');
        const subEl    = csvZone.querySelector('.dz-file-info-sub');
        const clearBtn = csvZone.querySelector('.dz-file-info button');

        csvInput.addEventListener('change', () => {
            const file = csvInput.files[0];
            if (!file) return;
            showCsvPreview(file, csvZone, nameEl, subEl, infoEl);
        });

        clearBtn?.addEventListener('click', (e) => {
            e.stopPropagation();
            e.preventDefault();
            csvZone.classList.remove('has-file');
            csvInput.value = '';
        });

        setupDragDrop(csvZone, csvInput, (file) => {
            showCsvPreview(file, csvZone, nameEl, subEl, infoEl);
        });
    }
}

function showImagePreview(file, zone, thumbImg, thumbBar) {
    const reader = new FileReader();
    reader.onload = (e) => {
        if (thumbImg) thumbImg.src = e.target.result;
        if (thumbBar) thumbBar.textContent = file.name;
        zone.classList.add('has-file');
    };
    reader.readAsDataURL(file);
}

function showCsvPreview(file, zone, nameEl, subEl, infoEl) {
    if (nameEl) nameEl.textContent = file.name;
    if (subEl)  subEl.textContent  = `${(file.size / 1024).toFixed(1)} KB`;
    if (infoEl) infoEl.style.display = 'flex';
    zone.classList.add('has-file');
}

function clearZone(input, zone, thumbImg) {
    input.value = '';
    zone.classList.remove('has-file');
    if (thumbImg) thumbImg.src = '';
}

function setupDragDrop(zone, input, onFile) {
    zone.addEventListener('dragover', (e) => {
        e.preventDefault();
        zone.classList.add('dragover');
    });
    zone.addEventListener('dragleave', () => zone.classList.remove('dragover'));
    zone.addEventListener('drop', (e) => {
        e.preventDefault();
        zone.classList.remove('dragover');
        const file = e.dataTransfer?.files[0];
        if (!file) return;
        const dt = new DataTransfer();
        dt.items.add(file);
        input.files = dt.files;
        onFile(file);
    });
}

function setupColorSwatches() {
    const colorInput = document.getElementById('color');
    const colorDisplay = document.getElementById('swatch-custom-display');

    document.querySelectorAll('.swatch[data-color]').forEach(sw => {
        sw.addEventListener('click', () => {
            setActiveColor(sw.dataset.color, sw);
        });
    });

    colorInput?.addEventListener('input', () => {
        document.querySelectorAll('.swatch[data-color]').forEach(s => s.classList.remove('active'));
        if (colorDisplay) colorDisplay.style.background = colorInput.value;
    });
}

function setActiveColor(hex, activeSwatch) {
    document.querySelectorAll('.swatch').forEach(s => s.classList.remove('active'));
    if (activeSwatch) activeSwatch.classList.add('active');
    const input = document.getElementById('color');
    if (input) input.value = hex;
}

function setupFormatChips() {
    const fmtVal = document.getElementById('export_format_val');
    document.querySelectorAll('.chip[data-fmt]').forEach(chip => {
        chip.addEventListener('click', () => {
            document.querySelectorAll('.chip[data-fmt]').forEach(c => c.classList.remove('active'));
            chip.classList.add('active');
            if (fmtVal) fmtVal.value = chip.dataset.fmt;
        });
    });
}

async function updatePreview() {
    const form      = document.getElementById('certForm');
    const spinner   = document.getElementById('previewSpinner');
    const statusEl  = document.getElementById('previewStatus');
    const badge     = document.getElementById('previewBadge');

    spinner.classList.add('show');
    statusEl.textContent = 'Generating…';
    if (badge) { badge.textContent = '…'; badge.className = 'preview-badge'; }

    try {
        const res  = await fetch('/preview', { method: 'POST', body: new FormData(form) });
        const data = await res.json();

        if (data.preview_url) {
            const img = document.getElementById('previewImg');
            img.onload = () => {
                document.getElementById('previewPlaceholder').style.display = 'none';
                img.style.display = 'block';
                statusEl.textContent = 'Showing first row from your CSV';
                if (badge) { badge.textContent = 'Updated ✓'; badge.className = 'preview-badge updated'; }
            };
            img.src = data.preview_url + '?t=' + Date.now();
        } else {
            statusEl.textContent = '⚠ ' + (data.error || 'Preview failed');
            if (badge) { badge.textContent = 'Error'; badge.className = 'preview-badge'; }
            alert(data.error || 'Preview failed');
        }
    } catch {
        statusEl.textContent = '⚠ Network error';
    } finally {
        spinner.classList.remove('show');
    }
}