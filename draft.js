function generateFiles_new() {
    const now = new Date();
    const datetime = now.toISOString().slice(0, 19).replace(/-/g, "").replace("T", "_").replace(/:/g, "");
    const filenamePrefix = `grocery_list_${datetime}`;

    generateYAML_new(filenamePrefix);
    generateExcel_new(filenamePrefix);
}


function generateYAML_new(filenamePrefix) {
    let yamlText = '';
    Object.keys(selections).forEach(category => {
        if (selectedCategories[category]) { // Check if the category is selected
            yamlText += `${category}:\n`;
            Object.entries(selections[category]).forEach(([item, details]) => {
                yamlText += `  - ${item}:\n    optional: ${details.optional}\n    amount: ${details.amount}\n`;
            });
        }
    });

    const yamlBlob = new Blob([yamlText], { type: 'text/plain' });
    const yamlHref = URL.createObjectURL(yamlBlob);
    const yamlLink = document.createElement('a');
    yamlLink.href = yamlHref;
    yamlLink.download = `${filenamePrefix}.yaml`;
    document.body.appendChild(yamlLink);
    yamlLink.click();
    document.body.removeChild(yamlLink);
}

function generateExcel_new(filenamePrefix) {
    const wb = XLSX.utils.book_new();

    // Explanation sheet
    const wsExplanation = XLSX.utils.aoa_to_sheet([['Description']]);
    XLSX.utils.book_append_sheet(wb, wsExplanation, 'Explanation');

    // Sheets for each category
    Object.keys(selections).forEach(category => {
        if (selectedCategories[category] && Object.keys(selections[category]).length > 0) {
            // Create a sheet with item names as headers (first row of sheet)
            const items = Object.keys(selections[category]);
            const wsData = [items];

            // Add a single row of data; each item gets a column, no details
            const row = new Array(items.length).fill('');
            wsData.push(row);

            const ws = XLSX.utils.aoa_to_sheet(wsData);
            XLSX.utils.book_append_sheet(wb, ws, category);
        }
    });

    // Write the workbook
    XLSX.writeFile(wb, `${filenamePrefix}.xlsx`);
}

