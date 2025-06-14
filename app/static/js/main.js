// Main JavaScript file for Transport Company Vehicle Rental Management System

// Initialize the application when the DOM is fully loaded
document.addEventListener('DOMContentLoaded', () => {
    console.log('Transport Company Vehicle Rental Management System initialized');
    
    // Initialize Bootstrap tooltips
    const tooltips = document.querySelectorAll('[data-bs-toggle="tooltip"]');
    if (tooltips.length) {
        Array.from(tooltips).forEach(tooltip => {
            new bootstrap.Tooltip(tooltip);
        });
    }
    
    // Initialize Bootstrap popovers
    const popovers = document.querySelectorAll('[data-bs-toggle="popover"]');
    if (popovers.length) {
        Array.from(popovers).forEach(popover => {
            new bootstrap.Popover(popover);
        });
    }
    
    // Setup event listeners for sidebar toggler if it exists
    const sidebarToggler = document.getElementById('sidebarToggle');
    if (sidebarToggler) {
        sidebarToggler.addEventListener('click', (e) => {
            e.preventDefault();
            document.body.classList.toggle('sidebar-toggled');
            document.querySelector('.sidebar')?.classList.toggle('toggled');
        });
    }
    
    // Close sidebar when window is less than 768px (mobile view)
    const handleResize = () => {
        if (window.innerWidth < 768) {
            document.querySelector('.sidebar')?.classList.add('toggled');
        } else {
            document.querySelector('.sidebar')?.classList.remove('toggled');
        }
    };
    
    window.addEventListener('resize', handleResize);
    handleResize(); // Call once on load
    
    // Handle flash message dismissal
    const flashMessages = document.querySelectorAll('.alert');
    if (flashMessages.length) {
        setTimeout(() => {
            flashMessages.forEach(message => {
                message.classList.add('fade');
                setTimeout(() => {
                    message.remove();
                }, 500);
            });
        }, 5000);
    }

    // Dark Mode Toggle Functionality
    const themeToggleBtn = document.getElementById('theme-toggle');
    
    // Function to set the theme
    const setTheme = (theme) => {
        document.documentElement.setAttribute('data-bs-theme', theme);
        localStorage.setItem('theme', theme);
        
        // Update button icons
        const darkIcon = themeToggleBtn.querySelector('.dark-icon');
        const lightIcon = themeToggleBtn.querySelector('.light-icon');
        
        if (theme === 'dark') {
            darkIcon.classList.add('d-none');
            lightIcon.classList.remove('d-none');
        } else {
            darkIcon.classList.remove('d-none');
            lightIcon.classList.add('d-none');
        }
    };
    
    // Check for saved theme preference or use system preference
    if (themeToggleBtn) {
        const savedTheme = localStorage.getItem('theme');
        
        if (savedTheme) {
            setTheme(savedTheme);
        } else {
            // Check if user prefers dark mode at the OS level
            const prefersDarkMode = window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches;
            setTheme(prefersDarkMode ? 'dark' : 'light');
        }
        
        // Add event listener for theme toggle
        themeToggleBtn.addEventListener('click', () => {
            const currentTheme = document.documentElement.getAttribute('data-bs-theme');
            const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
            setTheme(newTheme);
        });
        
        // Listen for system theme changes
        window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', e => {
            if (!localStorage.getItem('theme')) {
                setTheme(e.matches ? 'dark' : 'light');
            }
        });
    }
});