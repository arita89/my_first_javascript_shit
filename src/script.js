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

function selectItems(category) {
    const itemsDiv = document.getElementById('items');
    itemsDiv.innerHTML = ''; // Clear previous items
    categories[category].forEach(item => {
        const checkbox = document.createElement('input');
        checkbox.type = 'checkbox';
        checkbox.id = item;
        checkbox.name = 'items';
        checkbox.value = item;

        const label = document.createElement('label');
        label.htmlFor = item;
        label.appendChild(document.createTextNode(item));

        itemsDiv.appendChild(checkbox);
        itemsDiv.appendChild(label);
        itemsDiv.appendChild(document.createElement('br'));
    });
}

function generateYAML() {
    const selectedItems = document.querySelectorAll('input[name="items"]:checked');
    let yamlText = "";
    selectedItems.forEach(item => {
        yamlText += `- ${item.value}\n`;
    });
    alert(`YAML Configuration:\n${yamlText}`);
}

displayCategories();
