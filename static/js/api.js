// api.js - API Integration Layer

import { storage } from './utils.js';

/**
 * API Client Implementation
 */
class ApiClient {
    constructor(baseUrl = '/api') {
        this.baseUrl = baseUrl;
        this.cache = new Map();
        this.cacheTimeout = 5 * 60 * 1000; // 5 minutes
    }

    /**
     * Generate cache key for request
     * @param {string} endpoint - API endpoint
     * @param {Object} params - Query parameters
     * @returns {string} Cache key
     */
    getCacheKey(endpoint, params = {}) {
        return `${endpoint}?${new URLSearchParams(params).toString()}`;
    }

    /**
     * Check if cached response is valid
     * @param {Object} cachedData - Cached response data
     * @returns {boolean} Is cache valid
     */
    isCacheValid(cachedData) {
        if (!cachedData) return false;
        return (Date.now() - cachedData.timestamp) < this.cacheTimeout;
    }

    /**
     * Set cached response
     * @param {string} key - Cache key
     * @param {any} data - Response data
     */
    setCache(key, data) {
        this.cache.set(key, {
            data,
            timestamp: Date.now()
        });
    }

    /**
     * Clear cache for endpoint
     * @param {string} endpoint - API endpoint
     */
    clearCache(endpoint) {
        for (const key of this.cache.keys()) {
            if (key.startsWith(endpoint)) {
                this.cache.delete(key);
            }
        }
    }

    /**
     * Make API request
     * @param {string} endpoint - API endpoint
     * @param {Object} options - Request options
     * @returns {Promise} API response
     */
    async request(endpoint, options = {}) {
        const url = `${this.baseUrl}${endpoint}`;
        const defaultOptions = {
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': this.getCsrfToken()
            },
            credentials: 'same-origin'
        };

        const requestOptions = {
            ...defaultOptions,
            ...options,
            headers: {
                ...defaultOptions.headers,
                ...options.headers
            }
        };

        try {
            const response = await fetch(url, requestOptions);
            
            // Handle HTTP errors
            if (!response.ok) {
                throw await this.handleErrorResponse(response);
            }

            // Parse response
            const data = await response.json();
            return data;
        } catch (error) {
            throw this.handleRequestError(error);
        }
    }

    /**
     * Handle error response
     * @param {Response} response - Fetch response
     * @returns {Error} Formatted error
     */
    async handleErrorResponse(response) {
        let error;
        try {
            const data = await response.json();
            error = new Error(data.detail || data.message || 'API request failed');
            error.status = response.status;
            error.data = data;
        } catch {
            error = new Error(`HTTP ${response.status}: ${response.statusText}`);
            error.status = response.status;
        }
        return error;
    }

    /**
     * Handle request error
     * @param {Error} error - Original error
     * @returns {Error} Formatted error
     */
    handleRequestError(error) {
        if (error.status) return error;
        
        const formattedError = new Error('Network error occurred');
        formattedError.originalError = error;
        return formattedError;
    }

    /**
     * Get CSRF token
     * @returns {string} CSRF token
     */
    getCsrfToken() {
        return document.querySelector('[name=csrfmiddlewaretoken]')?.value;
    }

    /**
     * Generic GET request with caching
     * @param {string} endpoint - API endpoint
     * @param {Object} params - Query parameters
     * @param {boolean} useCache - Use cached response
     * @returns {Promise} API response
     */
    async get(endpoint, params = {}, useCache = true) {
        const cacheKey = this.getCacheKey(endpoint, params);
        
        if (useCache) {
            const cached = this.cache.get(cacheKey);
            if (this.isCacheValid(cached)) {
                return cached.data;
            }
        }

        const queryString = new URLSearchParams(params).toString();
        const url = queryString ? `${endpoint}?${queryString}` : endpoint;
        
        const data = await this.request(url, { method: 'GET' });
        
        if (useCache) {
            this.setCache(cacheKey, data);
        }
        
        return data;
    }

    /**
     * Generic POST request
     * @param {string} endpoint - API endpoint
     * @param {Object} data - Request data
     * @returns {Promise} API response
     */
    async post(endpoint, data) {
        const response = await this.request(endpoint, {
            method: 'POST',
            body: JSON.stringify(data)
        });
        
        this.clearCache(endpoint);
        return response;
    }

    /**
     * Generic PUT request
     * @param {string} endpoint - API endpoint
     * @param {Object} data - Request data
     * @returns {Promise} API response
     */
    async put(endpoint, data) {
        const response = await this.request(endpoint, {
            method: 'PUT',
            body: JSON.stringify(data)
        });
        
        this.clearCache(endpoint);
        return response;
    }

    /**
     * Generic DELETE request
     * @param {string} endpoint - API endpoint
     * @returns {Promise} API response
     */
    async delete(endpoint) {
        const response = await this.request(endpoint, {
            method: 'DELETE'
        });
        
        this.clearCache(endpoint);
        return response;
    }
}

/**
 * API Endpoints
 */
class SchoolCalendarApi {
    constructor() {
        this.client = new ApiClient();
    }

    // Calendar Events
    async getEvents(startDate, endDate) {
        return this.client.get('/events/', { start_date: startDate, end_date: endDate });
    }

    async createEvent(eventData) {
        return this.client.post('/events/', eventData);
    }

    async updateEvent(eventId, eventData) {
        return this.client.put(`/events/${eventId}/`, eventData);
    }

    async deleteEvent(eventId) {
        return this.client.delete(`/events/${eventId}/`);
    }

    // Terms
    async getTerms(schoolYearId = null) {
        const params = schoolYearId ? { school_year: schoolYearId } : {};
        return this.client.get('/terms/', params);
    }

    async getTerm(termId) {
        return this.client.get(`/terms/${termId}/`);
    }

    async createTerm(termData) {
        return this.client.post('/terms/', termData);
    }

    async updateTerm(termId, termData) {
        return this.client.put(`/terms/${termId}/`, termData);
    }

    async deleteTerm(termId) {
        return this.client.delete(`/terms/${termId}/`);
    }

    // School Years
    async getSchoolYears() {
        return this.client.get('/school-years/');
    }

    async getSchoolYear(yearId) {
        return this.client.get(`/school-years/${yearId}/`);
    }

    async createSchoolYear(yearData) {
        return this.client.post('/school-years/', yearData);
    }

    async updateSchoolYear(yearId, yearData) {
        return this.client.put(`/school-years/${yearId}/`, yearData);
    }

    async deleteSchoolYear(yearId) {
        return this.client.delete(`/school-years/${yearId}/`);
    }
}

// Initialize and export API instance
const api = new SchoolCalendarApi();
export default api;
