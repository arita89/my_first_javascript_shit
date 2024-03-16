import { updatePreview } from './preview.js';

let selections = {};

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

export { selectItems, updateSelections, updateDetails };
