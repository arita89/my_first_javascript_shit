// Object to store the state of selected categories
const selectedCategories = {};

const categories = {
    'Fruits': ['Apples', 'Pears'],
    'Vegetables': ['Carrots', 'Tomatoes'],
    'Dairy': ['Milk', 'Cheese'],
    'Meat': ['Chicken', 'Beef']
};

// Initialize an empty object for storing selections
const selections = {};

function displayCategories() {
    const categoriesDiv = document.getElementById('categories');
    Object.keys(categories).forEach(category => {
        const button = document.createElement('button');
        button.innerText = category;
        button.onclick = () => selectItems(category);
        categoriesDiv.appendChild(button);
    });
}

function selectItems(category) {
    const itemsDiv = document.getElementById('items');
    itemsDiv.innerHTML = ''; // Clear previous items
    if (!selections[category]) selections[category] = {};

    categories[category].forEach(item => {
        const itemDiv = document.createElement('div');

        const checkbox = document.createElement('input');
        checkbox.type = 'checkbox';
        checkbox.id = item;
        checkbox.value = item;
        checkbox.checked = selections[category][item] ? true : false;
        checkbox.onchange = (e) => updateSelections(category, item, e.target.checked);
        itemDiv.appendChild(checkbox);

        const label = document.createElement('label');
        label.htmlFor = item;
        label.innerText = item;
        itemDiv.appendChild(label);

        // Optional flag
        const optionalLabel = document.createElement('label');
        optionalLabel.innerText = " Optional: ";
        itemDiv.appendChild(optionalLabel);

        const optionalSelect = document.createElement('select');
        optionalSelect.innerHTML = `<option value="true">True</option><option value="false">False</option>`;
        optionalSelect.value = selections[category][item]?.optional || "false";
        optionalSelect.disabled = !checkbox.checked;
        optionalSelect.onchange = () => updateDetails(category, item, 'optional', optionalSelect.value);
        itemDiv.appendChild(optionalSelect);

        // Amount
        const amountLabel = document.createElement('label');
        amountLabel.innerText = " Amount: ";
        itemDiv.appendChild(amountLabel);

        const amountInput = document.createElement('input');
        amountInput.type = 'number';
        amountInput.value = selections[category][item]?.amount || 0;
        amountInput.min = 0;
        amountInput.disabled = !checkbox.checked;
        amountInput.onchange = () => updateDetails(category, item, 'amount', amountInput.value);
        itemDiv.appendChild(amountInput);

        itemsDiv.appendChild(itemDiv);
    });
}

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

function updateSelections(category, item, isChecked) {
    if (isChecked) {
        if (!selections[category][item]) {
            selections[category][item] = { optional: "false", amount: 0 };
        }
    } else {
        delete selections[category][item];
    }
    selectItems(category); // Refresh items to update their status and controls
    updatePreview(); // Update the preview to reflect the current selections
}

function updateDetails(category, item, detail, value) {
    if (selections[category] && selections[category][item]) {
        selections[category][item][detail] = value;
    }
    updatePreview(); // Refresh the preview to show the latest details
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

// Remove 'onclick' attribute from your HTML button and add an event listener instead for better practice
document.addEventListener('DOMContentLoaded', function () {
    const button = document.querySelector('.btn'); // Adjust if necessary to select your button
    button.addEventListener('click', generateFiles);
});

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

function DownloadYAML(yamlText) {
    const yamlBlob = new Blob([yamlText], { type: 'text/plain' });
    const yamlHref = URL.createObjectURL(yamlBlob);
    const yamlLink = document.createElement('a');
    yamlLink.href = yamlHref;
    yamlLink.download = `${filenamePrefix}.yaml`;
    document.body.appendChild(yamlLink);
    yamlLink.click();
    document.body.removeChild(yamlLink);
}

function generateExcel(filenamePrefix) {
    const wb = XLSX.utils.book_new();
    Object.keys(selections).forEach(category => {
        if (Object.keys(selections[category]).length > 0) {
            const wsData = [["Item", "Optional", "Amount"]];
            Object.entries(selections[category]).forEach(([item, details]) => {
                wsData.push([item, details.optional, details.amount]);
            });
            const ws = XLSX.utils.aoa_to_sheet(wsData);
            XLSX.utils.book_append_sheet(wb, ws, category);
        }
    });
    XLSX.writeFile(wb, `${filenamePrefix}.xlsx`);
}

// Initialize the app
displayCategories();
