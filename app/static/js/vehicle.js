// Vehicle management JavaScript
document.addEventListener('DOMContentLoaded', function() {
    // Vehicle form handling
    const vehicleForm = document.getElementById('vehicle-form');
    const modelSelect = document.getElementById('model');
    const customModelInput = document.getElementById('custom_model');
    const hourlyRateInput = document.getElementById('hourly_rate');
    const dailyRateInput = document.getElementById('daily_rate');
    const perKmRateInput = document.getElementById('per_km_rate');

    // Show/hide custom model input based on selection
    if (modelSelect && customModelInput) {
        modelSelect.addEventListener('change', function() {
            if (this.value === 'Other') {
                customModelInput.style.display = 'block';
                customModelInput.required = true;
            } else {
                customModelInput.style.display = 'none';
                customModelInput.required = false;
                customModelInput.value = '';
            }
        });
    }

    // Auto-calculate daily rate based on hourly rate
    if (hourlyRateInput && dailyRateInput) {
        hourlyRateInput.addEventListener('input', function() {
            const hourlyRate = parseFloat(this.value) || 0;
            const dailyRate = hourlyRate * 8; // 8 hours = 1 day
            dailyRateInput.value = dailyRate.toFixed(2);
        });
    }

    // Preset values for popular vehicle models
    const modelPresets = {
        'Ambassador': {
            hourly_rate: 150,
            per_km_rate: 12,
            has_ac: false,
            fuel_type: 'Petrol',
            transmission: 'Manual'
        },
        'Tata Sumo': {
            hourly_rate: 250,
            per_km_rate: 18,
            has_ac: true,
            fuel_type: 'Diesel',
            transmission: 'Manual'
        },
        'Maruti Omni': {
            hourly_rate: 180,
            per_km_rate: 15,
            has_ac: false,
            fuel_type: 'Petrol',
            transmission: 'Manual'
        },
        'Mahindra Bolero': {
            hourly_rate: 220,
            per_km_rate: 16,
            has_ac: true,
            fuel_type: 'Diesel',
            transmission: 'Manual'
        },
        'Toyota Innova': {
            hourly_rate: 350,
            per_km_rate: 22,
            has_ac: true,
            fuel_type: 'Diesel',
            transmission: 'Manual'
        }
    };

    // Apply preset values when model is selected
    if (modelSelect) {
        modelSelect.addEventListener('change', function() {
            const selectedModel = this.value;
            if (modelPresets[selectedModel]) {
                const preset = modelPresets[selectedModel];
                
                // Set hourly rate
                if (hourlyRateInput) {
                    hourlyRateInput.value = preset.hourly_rate;
                    // Trigger daily rate calculation
                    hourlyRateInput.dispatchEvent(new Event('input'));
                }
                
                // Set per km rate
                if (perKmRateInput) {
                    perKmRateInput.value = preset.per_km_rate;
                }
                
                // Set AC status
                const hasAcSelect = document.getElementById('has_ac');
                if (hasAcSelect) {
                    hasAcSelect.value = preset.has_ac.toString();
                }
                
                // Set fuel type
                const fuelTypeSelect = document.getElementById('fuel_type');
                if (fuelTypeSelect) {
                    fuelTypeSelect.value = preset.fuel_type;
                }
                
                // Set transmission
                const transmissionSelect = document.getElementById('transmission');
                if (transmissionSelect) {
                    transmissionSelect.value = preset.transmission;
                }
            }
        });
    }

    // Form validation
    if (vehicleForm) {
        vehicleForm.addEventListener('submit', function(e) {
            let isValid = true;
            let errorMessage = '';

            // Check required fields
            const requiredFields = [
                'registration_number',
                'vehicle_type', 
                'model',
                'year',
                'capacity',
                'hourly_rate',
                'per_km_rate',
                'has_ac',
                'fuel_type',
                'transmission'
            ];

            requiredFields.forEach(fieldName => {
                const field = document.getElementById(fieldName);
                if (field && !field.value.trim()) {
                    isValid = false;
                    errorMessage += `${fieldName.replace('_', ' ')} is required.\n`;
                }
            });

            // Validate positive numbers
            const numericFields = ['year', 'capacity', 'hourly_rate', 'per_km_rate', 'daily_rate'];
            numericFields.forEach(fieldName => {
                const field = document.getElementById(fieldName);
                if (field && field.value && parseFloat(field.value) <= 0) {
                    isValid = false;
                    errorMessage += `${fieldName.replace('_', ' ')} must be greater than 0.\n`;
                }
            });

            // Validate year
            const yearField = document.getElementById('year');
            if (yearField && yearField.value) {
                const year = parseInt(yearField.value);
                const currentYear = new Date().getFullYear();
                if (year < 1900 || year > currentYear + 1) {
                    isValid = false;
                    errorMessage += `Year must be between 1900 and ${currentYear + 1}.\n`;
                }
            }

            if (!isValid) {
                e.preventDefault();
                alert('Please fix the following errors:\n\n' + errorMessage);
            }
        });
    }

    // Enhanced vehicle list filtering
    const filterInput = document.getElementById('vehicle-filter');
    const acFilter = document.getElementById('ac-filter');
    const typeFilter = document.getElementById('type-filter');
    const statusFilter = document.getElementById('status-filter');

    function filterVehicles() {
        const filterText = filterInput ? filterInput.value.toLowerCase() : '';
        const acFilterValue = acFilter ? acFilter.value : '';
        const typeFilterValue = typeFilter ? typeFilter.value : '';
        const statusFilterValue = statusFilter ? statusFilter.value : '';
        
        const vehicleRows = document.querySelectorAll('.vehicle-row');
        
        vehicleRows.forEach(row => {
            const model = row.dataset.model ? row.dataset.model.toLowerCase() : '';
            const registration = row.dataset.registration ? row.dataset.registration.toLowerCase() : '';
            const hasAc = row.dataset.hasAc;
            const type = row.dataset.type;
            const status = row.dataset.status;
            
            const matchesText = !filterText || 
                               model.includes(filterText) || 
                               registration.includes(filterText);
            const matchesAc = !acFilterValue || hasAc === acFilterValue;
            const matchesType = !typeFilterValue || type === typeFilterValue;
            const matchesStatus = !statusFilterValue || status === statusFilterValue;
            
            if (matchesText && matchesAc && matchesType && matchesStatus) {
                row.style.display = '';
            } else {
                row.style.display = 'none';
            }
        });
    }

    // Add event listeners for filters
    if (filterInput) filterInput.addEventListener('input', filterVehicles);
    if (acFilter) acFilter.addEventListener('change', filterVehicles);
    if (typeFilter) typeFilter.addEventListener('change', filterVehicles);
    if (statusFilter) statusFilter.addEventListener('change', filterVehicles);

    // Rental cost calculator
    const calculateRentalCost = (hourlyRate, perKmRate, hours, km, isNightRental = false, nightMultiplier = 1.25, minHours = 4) => {
        const actualHours = Math.max(hours, minHours);
        const hourlyCost = actualHours * hourlyRate;
        const kmCost = km * perKmRate;
        let totalCost = hourlyCost + kmCost;
        
        if (isNightRental) {
            totalCost *= nightMultiplier;
        }
        
        return {
            hourlyCost: hourlyCost.toFixed(2),
            kmCost: kmCost.toFixed(2),
            nightCharge: isNightRental ? (totalCost - (hourlyCost + kmCost)).toFixed(2) : '0.00',
            totalCost: totalCost.toFixed(2)
        };
    };

    // Export calculator function for use in other pages
    window.calculateRentalCost = calculateRentalCost;
});
