// main.js - Main application entry point
import { store, eventBus, storage } from './utils.js';
import api from './api.js';

// Initialize app when DOM is ready
document.addEventListener('DOMContentLoaded', () => {
    // Make utilities available globally for debugging if needed
    window.app = {
        store,
        eventBus,
        storage,
        api
    };
});
