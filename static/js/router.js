class DashboardRouter {
    constructor() {
        this.currentPath = window.location.pathname;
        window.addEventListener('popstate', () => {
            this.currentPath = window.location.pathname;
        });
    }

    navigate(path) {
        if (path !== this.currentPath) {
            window.history.pushState({}, '', path);
            this.currentPath = path;
        }
    }
}
