// Making rows clickable in the task's table

document.addEventListener('DOMContentLoaded', () => {
    const rows = document.querySelectorAll('.clickable-row');
    rows.forEach(row => {
        row.style.cursor = 'pointer'; // add the pointer cursor dynamically
        row.addEventListener('click', event => {
            const href = row.dataset.href;
            if (href) {
                window.location = href;
            }
        });
    });
});
