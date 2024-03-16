import { selectItems } from './items.js';

export const categories = {
    'Fruits': ['Apples', 'Pears', 'Bananas', 'Oranges', 'Grapes'],
    'Vegetables': ['Carrots', 'Tomatoes', 'Lettuce', 'Cucumbers', 'Peppers'],
    'Dairy': ['Milk', 'Cheese', 'Yogurt', 'Butter', 'Cream'],
    'Meat': ['Chicken', 'Beef', 'Pork', 'Lamb', 'Turkey'],
    'Bakery': ['Bread', 'Croissant', 'Bagels', 'Muffins', 'Cake'],
    'Frozen': ['Ice Cream', 'Frozen Pizza', 'Frozen Vegetables', 'Frozen Desserts', 'Frozen Dinners'],
    'Beverages': ['Coffee', 'Tea', 'Soda', 'Juice', 'Water'],
    'Snacks': ['Chips', 'Chocolate', 'Nuts', 'Popcorn', 'Candy'],
    'Personal Care': ['Shampoo', 'Soap', 'Toothpaste', 'Deodorant', 'Lotion'],
    'Household': ['Laundry Detergent', 'Dish Soap', 'Cleaners', 'Paper Towels', 'Trash Bags'],
    'Pantry': ['Flour', 'Sugar', 'Rice', 'Pasta', 'Canned Goods'],
    'Spices': ['Salt', 'Pepper', 'Curry Powder', 'Garlic Powder', 'Paprika'],
    'Garden': ['Seeds', 'Tools'],
    'Animals': ['Pet Food', 'Toys'],
    'Cleaning': ['Disinfectants', 'Wipes'],
    'Electronics': ['Batteries', 'Chargers'],
    'Books': ['Novels', 'Magazines'],
    'Toys & Games': ['Board Games', 'Action Figures'],
    'Clothing': ['Shirts', 'Pants'],
    'Baby Clothing': ['Shirts', 'Dress'],
    'Garage': ['Bike', 'Car'],
    // Add more as needed
};

// Define a mapping for category colors
export const categoryColors = {
    'Fruits': '#90ee90', // Light green
    'Vegetables': '#90ee90', // Light green
    'Dairy': '#90ee90', // Light green
    'Meat': '#90ee90', // Light green
    'Bakery': '#fdd5b1', // Light orange
    'Frozen': '#fdd5b1', // Light orange
    'Beverages': '#fdd5b1', // Light orange
    'Snacks': '#b0e0e6', // Powder blue
    'Personal Care': '#b0e0e6', // Powder blue
    'Household': '#b0e0e6', // Powder blue
    'default': '#d3d3d3' // Light grey for any category not explicitly defined
};

function darkenColor(color, amount = 40) {
    let usePound = false;
    if (color[0] == "#") {
        color = color.slice(1);
        usePound = true;
    }
    let num = parseInt(color, 16);
    let r = (num >> 16) - amount;
    let b = ((num >> 8) & 0x00FF) - amount;
    let g = (num & 0x0000FF) - amount;
    if (r > 255) r = 255;
    else if (r < 0) r = 0;
    if (b > 255) b = 255;
    else if (b < 0) b = 0;
    if (g > 255) g = 255;
    else if (g < 0) g = 0;
    return (usePound ? "#" : "") + (g | (b << 8) | (r << 16)).toString(16);
}

let lastSelectedButton = null; // Keep track of the last selected button

function displayCategories() {
    const categoriesDiv = document.getElementById('categories');
    Object.keys(categories).forEach(category => {
        const button = document.createElement('button');
        button.innerText = category;
        const baseColor = categoryColors[category] || categoryColors['default'];
        button.style.backgroundColor = baseColor;
        button.setAttribute('data-category', category); // For easy identification

        button.onclick = () => {
            // Reset appearance of all category buttons
            document.querySelectorAll('#categories button').forEach(btn => {
                btn.style.backgroundColor = categoryColors[btn.getAttribute('data-category')] || categoryColors['default'];
                btn.classList.remove('selected-category');
                btn.innerHTML = btn.getAttribute('data-category'); // Remove symbols/icons
            });

            // Mark the currently checked category
            button.style.backgroundColor = darkenColor(baseColor);
            button.classList.add('selected-category');
            button.innerHTML = '✔ ' + button.innerText; // Add a symbol for visual marking

            selectItems(category, categories[category]);
        };

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
