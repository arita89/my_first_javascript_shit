import { selections } from './items.js';

function setupGenerateFilesButton() {
    const button = document.querySelector('.btn'); // Adjust if necessary to select your button
    button.addEventListener('click', generateFiles);
}

function generateYAML(filenamePrefix) {
    let yamlText = '';
    yamlText += `Description:\n`;
    yamlText += `  Explanation:\n    optional: false\n`;
    Object.keys(selections).forEach(category => {
        if (Object.keys(selections[category]).length > 0) {
            yamlText += `${category}:\n`;
            Object.entries(selections[category]).forEach(([item, details]) => {
                yamlText += `  ${item}:\n    optional: ${details.optional}\n    amount: ${details.amount}\n`;
            });
        }
    });

    // DownloadYAML(yamlText)

    return yamlText;
}

function generateFiles() {
    // Get current date and time, and format it as YYYYMMDD_HHMMSS
    const now = new Date();
    const datetime = now.toISOString().slice(0, 19).replace(/-/g, "").replace("T", "_").replace(/:/g, "");

    const filenamePrefix = `grocery_list_${datetime}`;

    // YAML Generation (You can comment this out if you only need the Excel file)
    const yamlText = generateYAML(filenamePrefix);

    // Convert the YAML text to a Blob
    const blob = new Blob([yamlText], { type: 'text/plain' });

    // Create a FormData object and append the Blob as 'file'
    const formData = new FormData();
    formData.append('file', blob, `${filenamePrefix}.yaml`);

    // Send the FormData with the YAML file to the Flask server
    fetch('http://127.0.0.1:8080/yaml2excel/generate-excel', {
        method: 'POST',
        body: formData,
    })
        .then(response => {
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            return response.blob();
        })
        .then(blob => {
            // Create a URL for the blob object
            const url = window.URL.createObjectURL(blob);

            // Create an anchor element and click it to download the file
            const a = document.createElement('a');
            a.href = url;
            a.download = `${filenamePrefix}.xlxs`; // The filename for the downloaded Excel file
            document.body.appendChild(a);
            a.click();

            // Clean up the URL and remove the anchor element
            window.URL.revokeObjectURL(url);
            a.remove();
        })
        .catch(error => {
            console.error('There has been a problem with your fetch operation:', error);
        });
}

export { setupGenerateFilesButton };
