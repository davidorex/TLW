// Calendar.js - Calendar Widget Component

class Calendar {
    constructor(containerId) {
        this.container = document.getElementById(containerId);
        this.currentDate = new Date();
        this.currentView = 'month';
        this.events = [];
        
        this.initializeElements();
        this.attachEventListeners();
        this.render();
    }

    initializeElements() {
        // Navigation elements
        this.prevButton = this.container.querySelector('#prevButton');
        this.nextButton = this.container.querySelector('#nextButton');
        this.titleElement = this.container.querySelector('#currentMonth');
        
        // View containers
        this.monthView = this.container.querySelector('#monthView');
        this.weekView = this.container.querySelector('#weekView');
        this.dayView = this.container.querySelector('#dayView');
        
        // View control buttons
        this.viewButtons = this.container.querySelectorAll('[data-view]');
    }

    attachEventListeners() {
        // Navigation listeners
        this.prevButton.addEventListener('click', () => this.navigate(-1));
        this.nextButton.addEventListener('click', () => this.navigate(1));
        
        // View change listeners
        this.viewButtons.forEach(button => {
            button.addEventListener('click', (e) => {
                this.changeView(e.target.dataset.view);
                this.updateViewButtons(e.target);
            });
        });
    }

    async fetchEvents(start, end) {
        try {
            const response = await fetch(`/api/events/?start=${start}&end=${end}`);
            if (!response.ok) throw new Error('Failed to fetch events');
            this.events = await response.json();
            this.render();
        } catch (error) {
            console.error('Error fetching events:', error);
        }
    }

    navigate(direction) {
        switch (this.currentView) {
            case 'month':
                this.currentDate.setMonth(this.currentDate.getMonth() + direction);
                break;
            case 'week':
                this.currentDate.setDate(this.currentDate.getDate() + (direction * 7));
                break;
            case 'day':
                this.currentDate.setDate(this.currentDate.getDate() + direction);
                break;
        }
        this.render();
    }

    changeView(view) {
        this.currentView = view;
        this.hideAllViews();
        this.render();
    }

    hideAllViews() {
        [this.monthView, this.weekView, this.dayView].forEach(view => {
            view.classList.add('hidden');
        });
    }

    updateViewButtons(activeButton) {
        this.viewButtons.forEach(button => {
            button.classList.remove('active');
        });
        activeButton.classList.add('active');
    }

    render() {
        this.updateTitle();
        
        switch (this.currentView) {
            case 'month':
                this.renderMonthView();
                break;
            case 'week':
                this.renderWeekView();
                break;
            case 'day':
                this.renderDayView();
                break;
        }
    }

    updateTitle() {
        const options = { year: 'numeric', month: 'long' };
        if (this.currentView === 'day') {
            options.day = 'numeric';
        }
        this.titleElement.textContent = this.currentDate.toLocaleDateString(undefined, options);
    }

    renderMonthView() {
        this.monthView.classList.remove('hidden');
        const daysContainer = this.monthView.querySelector('.calendar-days');
        daysContainer.innerHTML = '';

        const firstDay = new Date(this.currentDate.getFullYear(), this.currentDate.getMonth(), 1);
        const lastDay = new Date(this.currentDate.getFullYear(), this.currentDate.getMonth() + 1, 0);
        
        // Add days from previous month
        const startPadding = firstDay.getDay();
        const prevMonth = new Date(firstDay);
        prevMonth.setDate(0);
        
        for (let i = startPadding - 1; i >= 0; i--) {
            const dayElement = this.createDayElement(new Date(prevMonth.getFullYear(), prevMonth.getMonth(), prevMonth.getDate() - i));
            dayElement.classList.add('other-month');
            daysContainer.appendChild(dayElement);
        }

        // Add days of current month
        for (let day = 1; day <= lastDay.getDate(); day++) {
            const date = new Date(this.currentDate.getFullYear(), this.currentDate.getMonth(), day);
            const dayElement = this.createDayElement(date);
            daysContainer.appendChild(dayElement);
        }

        // Add days from next month
        const endPadding = 42 - (startPadding + lastDay.getDate()); // 42 = 6 rows × 7 days
        for (let i = 1; i <= endPadding; i++) {
            const date = new Date(lastDay.getFullYear(), lastDay.getMonth() + 1, i);
            const dayElement = this.createDayElement(date);
            dayElement.classList.add('other-month');
            daysContainer.appendChild(dayElement);
        }
    }

    createDayElement(date) {
        const dayElement = document.createElement('div');
        dayElement.className = 'calendar-day';
        
        if (this.isToday(date)) {
            dayElement.classList.add('today');
        }

        const dayNumber = document.createElement('div');
        dayNumber.className = 'calendar-day-number';
        dayNumber.textContent = date.getDate();
        dayElement.appendChild(dayNumber);

        // Add events for this day
        const dayEvents = this.getEventsForDate(date);
        dayEvents.forEach(event => {
            const eventElement = document.createElement('div');
            eventElement.className = `event ${event.type}`;
            eventElement.textContent = event.title;
            eventElement.title = event.title;
            eventElement.addEventListener('click', () => this.handleEventClick(event));
            dayElement.appendChild(eventElement);
        });

        return dayElement;
    }

    renderWeekView() {
        this.weekView.classList.remove('hidden');
        const timeline = this.weekView.querySelector('.timeline');
        timeline.innerHTML = '';

        // Create time slots
        for (let hour = 0; hour < 24; hour++) {
            const timeSlot = document.createElement('div');
            timeSlot.className = 'time-slot';
            
            const timeLabel = document.createElement('div');
            timeLabel.className = 'time-label';
            timeLabel.textContent = `${hour}:00`;
            
            const content = document.createElement('div');
            content.className = 'time-content';
            
            timeline.appendChild(timeLabel);
            timeline.appendChild(content);
        }
    }

    renderDayView() {
        this.dayView.classList.remove('hidden');
        const timeline = this.dayView.querySelector('.timeline');
        timeline.innerHTML = '';

        // Create time slots
        for (let hour = 0; hour < 24; hour++) {
            const timeSlot = document.createElement('div');
            timeSlot.className = 'time-slot';
            
            const timeLabel = document.createElement('div');
            timeLabel.className = 'time-label';
            timeLabel.textContent = `${hour}:00`;
            
            const content = document.createElement('div');
            content.className = 'time-content';
            
            timeline.appendChild(timeLabel);
            timeline.appendChild(content);
        }
    }

    isToday(date) {
        const today = new Date();
        return date.getDate() === today.getDate() &&
               date.getMonth() === today.getMonth() &&
               date.getFullYear() === today.getFullYear();
    }

    getEventsForDate(date) {
        // Filter events for the given date
        return this.events.filter(event => {
            const eventDate = new Date(event.date);
            return eventDate.getDate() === date.getDate() &&
                   eventDate.getMonth() === date.getMonth() &&
                   eventDate.getFullYear() === date.getFullYear();
        });
    }

    handleEventClick(event) {
        // Event click handler - can be customized based on requirements
        console.log('Event clicked:', event);
        // Implement modal or detail view
    }
}

// Initialize calendar when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    const calendar = new Calendar('calendarWidget');
    
    // Fetch initial events
    const start = new Date();
    const end = new Date(start);
    end.setMonth(end.getMonth() + 1);
    calendar.fetchEvents(start.toISOString(), end.toISOString());
});
