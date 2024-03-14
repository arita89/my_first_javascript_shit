const categories = {
    'Fruits': ['Apples', 'Pears'],
    'Vegetables': ['Carrots', 'Tomatoes'],
    'Dairy': ['Milk', 'Cheese'],
    'Meat': ['Chicken', 'Beef']
};

function displayCategories() {
    const categoriesDiv = document.getElementById('categories');
    Object.keys(categories).forEach(category => {
        const button = document.createElement('button');
        button.innerText = category;
        button.onclick = () => selectItems(category);
        categoriesDiv.appendChild(button);
    });
}

const selections = {}; // Object to store selected items across categories

function selectItems(category) {
    if (!selections[category]) selections[category] = [];

    const itemsDiv = document.getElementById('items');
    itemsDiv.innerHTML = ''; // Clear previous items
    categories[category].forEach(item => {
        const checkbox = document.createElement('input');
        checkbox.type = 'checkbox';
        checkbox.id = item;
        checkbox.value = item;
        checkbox.checked = selections[category].includes(item);
        checkbox.onchange = () => updateSelections(category, item, checkbox.checked);

        const label = document.createElement('label');
        label.htmlFor = item;
        label.innerText = item;

        itemsDiv.appendChild(checkbox);
        itemsDiv.appendChild(label);
        itemsDiv.appendChild(document.createElement('br'));
    });
}

function updateSelections(category, item, isChecked) {
    if (isChecked) {
        selections[category].push(item);
    } else {
        const index = selections[category].indexOf(item);
        if (index !== -1) {
            selections[category].splice(index, 1);
        }
    }
}

function generateYAML() {
    let yamlText = '';
    Object.keys(selections).forEach(category => {
        if (selections[category].length > 0) {
            yamlText += `${category}:\n`;
            selections[category].forEach(item => {
                yamlText += `  - ${item}\n`;
            });
        }
    });

    const blob = new Blob([yamlText], { type: 'text/plain' });
    const href = URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.href = href;
    link.download = "GroceryList.yaml";
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
}

// Display categories on page load
displayCategories();
