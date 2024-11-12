// utils.js - State Management and Utility Functions

/**
 * State Store Implementation
 */
class StateStore {
    constructor() {
        this.state = {};
        this.listeners = new Map();
    }

    /**
     * Get state value by key
     * @param {string} key - State key
     * @returns {any} State value
     */
    get(key) {
        return this.state[key];
    }

    /**
     * Set state value and notify listeners
     * @param {string} key - State key
     * @param {any} value - New state value
     */
    set(key, value) {
        const oldValue = this.state[key];
        this.state[key] = value;

        if (this.listeners.has(key)) {
            this.listeners.get(key).forEach(listener => {
                listener(value, oldValue);
            });
        }
    }

    /**
     * Subscribe to state changes
     * @param {string} key - State key to watch
     * @param {Function} callback - Callback function
     * @returns {Function} Unsubscribe function
     */
    subscribe(key, callback) {
        if (!this.listeners.has(key)) {
            this.listeners.set(key, new Set());
        }
        this.listeners.get(key).add(callback);

        return () => {
            const listeners = this.listeners.get(key);
            if (listeners) {
                listeners.delete(callback);
                if (listeners.size === 0) {
                    this.listeners.delete(key);
                }
            }
        };
    }
}

/**
 * Event Bus System
 */
class EventBus {
    constructor() {
        this.events = new Map();
    }

    /**
     * Subscribe to an event
     * @param {string} event - Event name
     * @param {Function} callback - Event handler
     * @returns {Function} Unsubscribe function
     */
    on(event, callback) {
        if (!this.events.has(event)) {
            this.events.set(event, new Set());
        }
        this.events.get(event).add(callback);

        return () => {
            const handlers = this.events.get(event);
            if (handlers) {
                handlers.delete(callback);
                if (handlers.size === 0) {
                    this.events.delete(event);
                }
            }
        };
    }

    /**
     * Emit an event
     * @param {string} event - Event name
     * @param {any} data - Event data
     */
    emit(event, data) {
        const handlers = this.events.get(event);
        if (handlers) {
            handlers.forEach(handler => {
                try {
                    handler(data);
                } catch (error) {
                    console.error(`Error in event handler for ${event}:`, error);
                }
            });
        }
    }
}

/**
 * Data Persistence
 */
class StorageManager {
    constructor(prefix = 'app_') {
        this.prefix = prefix;
    }

    /**
     * Save data to localStorage
     * @param {string} key - Storage key
     * @param {any} value - Value to store
     */
    save(key, value) {
        try {
            const serialized = JSON.stringify(value);
            localStorage.setItem(this.prefix + key, serialized);
        } catch (error) {
            console.error('Error saving to localStorage:', error);
        }
    }

    /**
     * Load data from localStorage
     * @param {string} key - Storage key
     * @returns {any} Stored value
     */
    load(key) {
        try {
            const serialized = localStorage.getItem(this.prefix + key);
            return serialized ? JSON.parse(serialized) : null;
        } catch (error) {
            console.error('Error loading from localStorage:', error);
            return null;
        }
    }

    /**
     * Remove data from localStorage
     * @param {string} key - Storage key
     */
    remove(key) {
        localStorage.removeItem(this.prefix + key);
    }

    /**
     * Clear all app data from localStorage
     */
    clear() {
        Object.keys(localStorage)
            .filter(key => key.startsWith(this.prefix))
            .forEach(key => localStorage.removeItem(key));
    }
}

/**
 * Utility Functions
 */

/**
 * Debounce function
 * @param {Function} func - Function to debounce
 * @param {number} wait - Delay in milliseconds
 * @returns {Function} Debounced function
 */
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

/**
 * Memoization helper
 * @param {Function} func - Function to memoize
 * @returns {Function} Memoized function
 */
function memoize(func) {
    const cache = new Map();
    return function memoized(...args) {
        const key = JSON.stringify(args);
        if (cache.has(key)) {
            return cache.get(key);
        }
        const result = func.apply(this, args);
        cache.set(key, result);
        return result;
    };
}

/**
 * Format date string
 * @param {string|Date} date - Date to format
 * @param {string} format - Format string
 * @returns {string} Formatted date string
 */
function formatDate(date, format = 'YYYY-MM-DD') {
    const d = new Date(date);
    const year = d.getFullYear();
    const month = String(d.getMonth() + 1).padStart(2, '0');
    const day = String(d.getDate()).padStart(2, '0');
    
    return format
        .replace('YYYY', year)
        .replace('MM', month)
        .replace('DD', day);
}

/**
 * Deep clone object
 * @param {any} obj - Object to clone
 * @returns {any} Cloned object
 */
function deepClone(obj) {
    return JSON.parse(JSON.stringify(obj));
}

// Initialize global instances
const store = new StateStore();
const eventBus = new EventBus();
const storage = new StorageManager();

// Export utilities
export {
    store,
    eventBus,
    storage,
    debounce,
    memoize,
    formatDate,
    deepClone
};
