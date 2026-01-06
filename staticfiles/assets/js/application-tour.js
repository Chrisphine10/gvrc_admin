/**
 * Application Tour System
 * Provides guided tour functionality for new users
 */

(function() {
    'use strict';

    // Tour configuration - only include elements that exist on current page
    function getTourSteps() {
        const steps = [];
        
        // Step 1: Welcome (always available)
        if (document.querySelector('.navbar-brand')) {
            steps.push({
                element: '.navbar-brand',
                title: 'Welcome to Hodi Admin!',
                intro: 'This is your application logo and branding area. Click here to return to the dashboard.',
                position: 'bottom'
            });
        }
        
        // Step 2: Navigation Menu (check if exists)
        const sidenav = document.querySelector('#sidenav-main');
        if (sidenav) {
            steps.push({
                element: '#sidenav-main',
                title: 'Navigation Menu',
                intro: 'Use the sidebar menu to navigate through different sections of the application. Each section contains related features and tools.',
                position: 'right'
            });
        }
        
        // Step 3: Dashboard link (only if exists)
        const dashboardLink = document.querySelector('.nav-link[href*="index"], .nav-link[href*="dashboard"]');
        if (dashboardLink) {
            steps.push({
                element: '.nav-link[href*="index"], .nav-link[href*="dashboard"]',
                title: 'Dashboard',
                intro: 'The dashboard provides an overview of key metrics, recent activities, and quick access to important features.',
                position: 'right'
            });
        }
        
        // Step 4: Facilities link (only if exists)
        const facilitiesLink = document.querySelector('.nav-link[href*="facilities"]');
        if (facilitiesLink) {
            steps.push({
                element: '.nav-link[href*="facilities"]',
                title: 'Facility Management',
                intro: 'Manage community facilities, view facility maps, and organize services and programs.',
                position: 'right'
            });
        }
        
        // Step 5: HR link (only if exists)
        const hrLink = document.querySelector('.nav-link[href*="humanresources"], .nav-link[href*="hr"]');
        if (hrLink) {
            steps.push({
                element: '.nav-link[href*="humanresources"], .nav-link[href*="hr"]',
                title: 'Human Resources',
                intro: 'Manage staff, contacts, and human resource information for facilities.',
                position: 'right'
            });
        }
        
        // Step 6: Chat link (only if exists)
        const chatLink = document.querySelector('.nav-link[href*="chat"]');
        if (chatLink) {
            steps.push({
                element: '.nav-link[href*="chat"]',
                title: 'Emergency Chat',
                intro: 'Monitor and manage emergency chat conversations and analytics.',
                position: 'right'
            });
        }
        
        // Step 7: Documents link (only if exists)
        const docsLink = document.querySelector('.nav-link[href*="documents"]');
        if (docsLink) {
            steps.push({
                element: '.nav-link[href*="documents"]',
                title: 'Documents',
                intro: 'Upload, manage, and organize documents and files.',
                position: 'right'
            });
        }
        
        // Step 8: Users link (only if exists)
        const usersLink = document.querySelector('.nav-link[href*="users"]');
        if (usersLink) {
            steps.push({
                element: '.nav-link[href*="users"]',
                title: 'User Management',
                intro: 'Manage user accounts, roles, and permissions.',
                position: 'right'
            });
        }
        
        // Step 9: Settings link (only if exists)
        const settingsLink = document.querySelector('.nav-link[href*="settings"]');
        if (settingsLink) {
            steps.push({
                element: '.nav-link[href*="settings"]',
                title: 'Application Settings',
                intro: 'Configure application settings, upload logos, customize themes, and manage essential settings.',
                position: 'right'
            });
        }
        
        // Step 10: Top Navigation (check if exists)
        const navbar = document.querySelector('#navbar-main');
        if (navbar) {
            steps.push({
                element: '#navbar-main',
                title: 'Top Navigation',
                intro: 'Access notifications, user profile, and quick actions from the top navigation bar.',
                position: 'bottom'
            });
        }
        
        return steps;
    }

    // Initialize tour
    function initTour() {
        // Check if intro.js is loaded
        if (typeof introJs === 'undefined') {
            console.warn('Intro.js not loaded. Loading from CDN...');
            loadIntroJS();
            return;
        }

        // Get steps that exist on current page
        const steps = getTourSteps();
        
        if (steps.length === 0) {
            console.warn('No tour steps available on this page');
            if (window.toastManager) {
                window.toastManager.info('Tour is not available on this page. Please navigate to the main dashboard.');
            }
            return null;
        }

        const tour = introJs();
        tour.setOptions({
            steps: steps,
            showProgress: true,
            showBullets: true,
            exitOnOverlayClick: true,
            exitOnEsc: true,
            nextLabel: 'Next →',
            prevLabel: '← Previous',
            skipLabel: 'Skip Tour',
            doneLabel: 'Got it!',
            tooltipClass: 'customTooltip',
            highlightClass: 'customHighlight',
            buttonClass: 'btn btn-sm btn-primary',
            disableInteraction: false,
            // Better element detection
            scrollToElement: true,
            scrollPadding: 20
        });

        // Store tour completion in localStorage
        tour.oncomplete(function() {
            localStorage.setItem('hodi_tour_completed', 'true');
            localStorage.setItem('hodi_tour_completed_date', new Date().toISOString());
            if (window.toastManager) {
                window.toastManager.success('Tour completed! You can restart it anytime from the Help menu.');
            }
        });

        tour.onexit(function() {
            // Don't mark as completed if user exits early
        });

        return tour;
    }

    // Load Intro.js from CDN
    function loadIntroJS() {
        // Load CSS
        const link = document.createElement('link');
        link.rel = 'stylesheet';
        link.href = 'https://cdn.jsdelivr.net/npm/intro.js@7.2.0/minified/introjs.min.css';
        document.head.appendChild(link);

        // Load JS
        const script = document.createElement('script');
        script.src = 'https://cdn.jsdelivr.net/npm/intro.js@7.2.0/minified/intro.min.js';
        script.onload = function() {
            console.log('Intro.js loaded successfully');
            // Retry initialization after a short delay
            setTimeout(function() {
                const tour = initTour();
                if (tour) {
                    tour.start();
                }
            }, 100);
        };
        document.head.appendChild(script);
    }

    // Start tour function
    window.startApplicationTour = function() {
        const tour = initTour();
        if (tour) {
            tour.start();
        } else {
            loadIntroJS();
        }
    };

    // Check if tour should auto-start
    function checkAutoStartTour() {
        // Check if tour is enabled and should show on first login
        const tourCompleted = localStorage.getItem('hodi_tour_completed');
        const shouldAutoStart = !tourCompleted; // Auto-start if not completed

        // Check if settings allow auto-start (this would come from backend)
        // For now, we'll use localStorage flag
        if (shouldAutoStart) {
            // Wait for page to fully load
            if (document.readyState === 'complete') {
                setTimeout(function() {
                    window.startApplicationTour();
                }, 2000); // Wait 2 seconds after page load
            } else {
                window.addEventListener('load', function() {
                    setTimeout(function() {
                        window.startApplicationTour();
                    }, 2000);
                });
            }
        }
    }

    // Add tour button to navigation
    function addTourButton() {
        // Check if button already exists
        if (document.getElementById('start-tour-btn')) {
            return;
        }

        // Try to find a good place to add the button (e.g., in the navbar)
        const navbar = document.querySelector('#navbar-main .navbar-nav');
        if (navbar) {
            const tourButton = document.createElement('li');
            tourButton.className = 'nav-item';
            tourButton.innerHTML = `
                <a class="nav-link" href="javascript:void(0);" id="start-tour-btn" onclick="window.startApplicationTour()">
                    <i class="ni ni-compass-04 text-info"></i>
                    <span class="nav-link-text">Take Tour</span>
                </a>
            `;
            navbar.appendChild(tourButton);
        }

        // Also add to sidenav if available
        const sidenav = document.querySelector('#sidenav-main .navbar-nav');
        if (sidenav) {
            const tourItem = document.createElement('li');
            tourItem.className = 'nav-item';
            tourItem.innerHTML = `
                <a class="nav-link" href="javascript:void(0);" id="start-tour-btn-sidebar" onclick="window.startApplicationTour()">
                    <i class="ni ni-compass-04 text-info"></i>
                    <span class="nav-link-text">Application Tour</span>
                </a>
            `;
            // Insert before logout or at the end
            const logoutItem = sidenav.querySelector('.nav-link[href*="logout"]');
            if (logoutItem && logoutItem.closest('li')) {
                sidenav.insertBefore(tourItem, logoutItem.closest('li'));
            } else {
                sidenav.appendChild(tourItem);
            }
        }
    }

    // Initialize when DOM is ready
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', function() {
            addTourButton();
            // Auto-start is controlled by backend settings, so we'll check via API or template variable
        });
    } else {
        addTourButton();
    }

    // Export for global access
    window.ApplicationTour = {
        start: window.startApplicationTour,
        init: initTour,
        addButton: addTourButton
    };

})();

