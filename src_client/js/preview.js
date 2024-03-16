
function updatePreview(selections) {
    const previewDiv = document.getElementById('preview');
    previewDiv.innerHTML = '<h2>Preview</h2>'; // Reset the preview area

    const table = document.createElement('table');
    Object.entries(selections).forEach(([category, items]) => {
        // Check if the category has any selected subitems before adding to preview
        if (Object.values(items).some(item => item)) {
            let row = table.insertRow(-1);
            let cell = row.insertCell(-1);
            cell.colSpan = 3;
            cell.innerHTML = `<strong>${category}</strong>`;

            Object.entries(items).forEach(([item, details]) => {
                if (details) { // Ensure the item is selected
                    row = table.insertRow(-1);
                    row.insertCell(-1).innerText = item;
                    row.insertCell(-1).innerText = `Optional: ${details.optional}`;
                    row.insertCell(-1).innerText = `Amount: ${details.amount}`;
                }
            });
        }
    });

    if (table.rows.length > 1) { // Check if the table has more than just the header row
        previewDiv.appendChild(table);
    } else {
        previewDiv.innerHTML += '<p>No selections made.</p>'; // Indicate no selections if table is empty
    }
}

export { updatePreview };
