// TermManager.js - Term Management Component

class TermManager {
    constructor() {
        this.initializeElements();
        this.attachEventListeners();
        this.modal = null;
        this.currentTermId = null;
    }

    initializeElements() {
        this.termCards = document.querySelectorAll('.term-card');
        this.modal = document.getElementById('termEditModal');
        this.form = document.getElementById('termEditForm');
    }

    attachEventListeners() {
        // Attach listeners to all term cards
        this.termCards.forEach(card => {
            const editBtn = card.querySelector('.edit-term');
            const deleteBtn = card.querySelector('.delete-term');

            if (editBtn) {
                editBtn.addEventListener('click', () => this.openEditModal(card));
            }
            if (deleteBtn) {
                deleteBtn.addEventListener('click', () => this.handleDelete(card));
            }
        });

        // Modal event listeners
        if (this.modal) {
            const closeBtn = this.modal.querySelector('.close-modal');
            const cancelBtn = this.modal.querySelector('.cancel-edit');
            const form = this.modal.querySelector('#termEditForm');

            closeBtn.addEventListener('click', () => this.closeModal());
            cancelBtn.addEventListener('click', () => this.closeModal());
            form.addEventListener('submit', (e) => this.handleSubmit(e));

            // Close modal if clicking outside
            this.modal.addEventListener('click', (e) => {
                if (e.target === this.modal) {
                    this.closeModal();
                }
            });
        }

        // Date validation
        const startDate = document.getElementById('startDate');
        const endDate = document.getElementById('endDate');

        if (startDate && endDate) {
            startDate.addEventListener('change', () => this.validateDates());
            endDate.addEventListener('change', () => this.validateDates());
        }
    }

    async openEditModal(card) {
        this.currentTermId = card.dataset.termId;
        
        try {
            const response = await fetch(`/api/terms/${this.currentTermId}/`);
            if (!response.ok) throw new Error('Failed to fetch term data');
            
            const termData = await response.json();
            this.populateForm(termData);
            this.modal.style.display = 'block';
        } catch (error) {
            console.error('Error fetching term data:', error);
            this.showError('Failed to load term data');
        }
    }

    closeModal() {
        this.modal.style.display = 'none';
        this.form.reset();
        this.currentTermId = null;
    }

    populateForm(termData) {
        const form = this.form;
        
        form.querySelector('#termName').value = termData.name;
        form.querySelector('#termType').value = termData.term_type;
        form.querySelector('#startDate').value = this.formatDate(termData.start_date);
        form.querySelector('#endDate').value = this.formatDate(termData.end_date);
        form.querySelector('#description').value = termData.description || '';
    }

    formatDate(dateString) {
        const date = new Date(dateString);
        return date.toISOString().split('T')[0];
    }

    validateDates() {
        const startDate = new Date(document.getElementById('startDate').value);
        const endDate = new Date(document.getElementById('endDate').value);
        
        if (endDate < startDate) {
            this.showError('End date cannot be before start date');
            return false;
        }
        return true;
    }

    async handleSubmit(event) {
        event.preventDefault();

        if (!this.validateDates()) {
            return;
        }

        const formData = new FormData(this.form);
        const termData = {
            name: formData.get('name'),
            term_type: formData.get('term_type'),
            start_date: formData.get('start_date'),
            end_date: formData.get('end_date'),
            description: formData.get('description')
        };

        try {
            const response = await fetch(`/api/terms/${this.currentTermId}/`, {
                method: 'PUT',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': this.getCsrfToken()
                },
                body: JSON.stringify(termData)
            });

            if (!response.ok) throw new Error('Failed to update term');

            const updatedTerm = await response.json();
            this.updateTermCard(updatedTerm);
            this.closeModal();
            this.showSuccess('Term updated successfully');
        } catch (error) {
            console.error('Error updating term:', error);
            this.showError('Failed to update term');
        }
    }

    async handleDelete(card) {
        const termId = card.dataset.termId;
        
        if (!confirm('Are you sure you want to delete this term?')) {
            return;
        }

        try {
            const response = await fetch(`/api/terms/${termId}/`, {
                method: 'DELETE',
                headers: {
                    'X-CSRFToken': this.getCsrfToken()
                }
            });

            if (!response.ok) throw new Error('Failed to delete term');

            card.remove();
            this.showSuccess('Term deleted successfully');
        } catch (error) {
            console.error('Error deleting term:', error);
            this.showError('Failed to delete term');
        }
    }

    updateTermCard(termData) {
        const card = document.querySelector(`[data-term-id="${termData.id}"]`);
        if (!card) return;

        // Update term card content
        card.querySelector('.term-name').textContent = termData.name;
        card.querySelector('.date-value:first-child').textContent = 
            new Date(termData.start_date).toLocaleDateString();
        card.querySelector('.date-value:last-child').textContent = 
            new Date(termData.end_date).toLocaleDateString();
        
        const description = card.querySelector('.term-description');
        if (description) {
            description.textContent = termData.description || '';
        }

        // Update term type
        const typeValue = card.querySelector('.meta-value');
        if (typeValue) {
            typeValue.textContent = termData.term_type;
        }
    }

    getCsrfToken() {
        return document.querySelector('[name=csrfmiddlewaretoken]').value;
    }

    showSuccess(message) {
        // Implement success notification
        console.log('Success:', message);
    }

    showError(message) {
        // Implement error notification
        console.error('Error:', message);
    }
}

// Initialize term manager when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    const termManager = new TermManager();
});
