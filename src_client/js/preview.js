function updatePreview() {
    const previewDiv = document.getElementById('preview');
    previewDiv.innerHTML = '<h2>Preview</h2>'; // Reset the preview area

    const table = document.createElement('table');
    Object.entries(selections).forEach(([category, items]) => {
        let row = table.insertRow(-1);
        let cell = row.insertCell(-1);
        cell.colSpan = 3;
        cell.innerHTML = `<strong>${category}</strong>`;

        Object.entries(items).forEach(([item, details]) => {
            row = table.insertRow(-1);
            row.insertCell(-1).innerText = item;
            row.insertCell(-1).innerText = `Optional: ${details.optional}`;
            row.insertCell(-1).innerText = `Amount: ${details.amount}`;
        });
    });

    previewDiv.appendChild(table);
}

export { updatePreview };
