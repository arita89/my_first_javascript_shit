import { selectItems } from './items.js';

export const categories = {
    'Fruits': ['Apples', 'Pears'],
    'Vegetables': ['Carrots', 'Tomatoes'],
    'Dairy': ['Milk', 'Cheese'],
    'Meat': ['Chicken', 'Beef']
};

// Optional: Define a mapping for category colors
const categoryColors = {
    'Fruits': '#90ee90', // Light green
    'Vegetables': '#90ee90', // Light green
    // Default color for other categories
    'default': '#add8e6' // Light blue
};

function displayCategories() {
    const categoriesDiv = document.getElementById('categories');
    Object.keys(categories).forEach(category => {
        const button = document.createElement('button');
        button.innerText = category;
        // Apply color based on the category or use default
        button.style.backgroundColor = categoryColors[category] || categoryColors['default'];
        button.onclick = () => selectItems(category, categories[category]);
        categoriesDiv.appendChild(button);
    });
}

// NOTE ON THE BUTTONS STYLE:  styles directly to an element via JavaScript 
// (e.g., button.style.backgroundColor = ...), these styles are added as inline styles on the HTML element. 
// Inline styles have a higher specificity than styles defined in external or internal CSS sheets, 
// meaning the inline styles will "rule" or take precedence over CSS-defined styles for the same properties.
// The JavaScript-applied styles will only override the specific properties they set (in this case, backgroundColor), 
// and all other styles from your CSS will still apply.

export { displayCategories };
