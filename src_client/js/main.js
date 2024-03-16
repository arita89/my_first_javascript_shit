import { displayCategories } from './categories.js';
import { setupGenerateFilesButton } from './api.js';

// Initialize the app
document.addEventListener('DOMContentLoaded', function () {
    displayCategories();
    setupGenerateFilesButton();
});
