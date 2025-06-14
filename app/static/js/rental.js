// Rental management functionality

// Rental Manager object for handling rental-related operations
const RentalManager = {
    // Calculate total rental cost based on start and end dates
    calculateRentalCost: function(startDate, endDate, dailyRate) {
        const days = Math.ceil((endDate.getTime() - startDate.getTime()) / (24 * 60 * 60 * 1000));
        return days * dailyRate;
    },

    // Validate rental form inputs
    validateRentalForm: function() {
        const vehicleSelect = document.getElementById('vehicle_id');
        const customerSelect = document.getElementById('customer_id');
        const startDateInput = document.getElementById('start_date');
        const endDateInput = document.getElementById('end_date');

        let isValid = true;
        let errorMessage = '';

        if (vehicleSelect.value === '') {
            isValid = false;
            errorMessage += 'Please select a vehicle.\n';
        }

        if (customerSelect.value === '') {
            isValid = false;
            errorMessage += 'Please select a customer.\n';
        }

        if (startDateInput.value === '') {
            isValid = false;
            errorMessage += 'Please enter a start date.\n';
        }

        if (endDateInput.value === '') {
            isValid = false;
            errorMessage += 'Please enter an end date.\n';
        }

        const startDate = new Date(startDateInput.value);
        const endDate = new Date(endDateInput.value);

        if (startDate > endDate) {
            isValid = false;
            errorMessage += 'End date must be after start date.\n';
        }

        if (!isValid) {
            alert('Please fix the following errors:\n' + errorMessage);
        }

        return isValid;
    },

    // Update rental cost in real time as dates change
    updateRentalCostPreview: function() {
        const startDateInput = document.getElementById('start_date');
        const endDateInput = document.getElementById('end_date');
        const vehicleSelect = document.getElementById('vehicle_id');
        const costPreview = document.getElementById('rental_cost_preview');
        
        if (startDateInput && endDateInput && vehicleSelect && costPreview) {
            if (startDateInput.value && endDateInput.value && vehicleSelect.value) {
                const startDate = new Date(startDateInput.value);
                const endDate = new Date(endDateInput.value);
                
                // Get the daily rate from the selected vehicle option
                const selectedOption = vehicleSelect.options[vehicleSelect.selectedIndex];
                const dailyRate = parseFloat(selectedOption.getAttribute('data-daily-rate') || '0');
                
                if (startDate <= endDate) {
                    const cost = this.calculateRentalCost(startDate, endDate, dailyRate);
                    costPreview.textContent = `Estimated Cost: $${cost.toFixed(2)}`;
                } else {
                    costPreview.textContent = 'Please select valid dates';
                }
            }
        }
    },
    
    // Initialize rental form event listeners
    initRentalForm: function() {
        const rentalForm = document.getElementById('rental-form');
        const startDateInput = document.getElementById('start_date');
        const endDateInput = document.getElementById('end_date');
        const vehicleSelect = document.getElementById('vehicle_id');
        
        if (rentalForm) {
            rentalForm.addEventListener('submit', (e) => {
                if (!this.validateRentalForm()) {
                    e.preventDefault();
                }
            });
            
            // Update cost preview when inputs change
            if (startDateInput && endDateInput && vehicleSelect) {
                startDateInput.addEventListener('change', () => this.updateRentalCostPreview());
                endDateInput.addEventListener('change', () => this.updateRentalCostPreview());
                vehicleSelect.addEventListener('change', () => this.updateRentalCostPreview());
            }
        }
    }
};

// Initialize rental functionality when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    // Check if we're on a rental-related page
    if (window.location.pathname.includes('/rentals')) {
        RentalManager.initRentalForm();
    }
});