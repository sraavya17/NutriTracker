// NutriTracker Frontend JavaScript

document.addEventListener('DOMContentLoaded', function() {
    // Initialize the application
    initializeApp();
});

function initializeApp() {
    // Add event listeners
    document.getElementById('add-food-item').addEventListener('click', addFoodItem);
    document.getElementById('nutrition-form').addEventListener('submit', handleFormSubmit);
    
    // Add remove functionality to existing food items
    updateRemoveButtons();
}

function addFoodItem() {
    const container = document.getElementById('food-items-container');
    const newItem = document.createElement('div');
    newItem.className = 'input-group mb-2';
    newItem.innerHTML = `
        <input type="text" class="form-control food-item" placeholder="Enter food item (e.g., apple, banana)" required>
        <button type="button" class="btn btn-outline-danger remove-food-item">
            <i class="fas fa-minus"></i>
        </button>
    `;
    
    container.appendChild(newItem);
    updateRemoveButtons();
}

function updateRemoveButtons() {
    const removeButtons = document.querySelectorAll('.remove-food-item');
    const foodItems = document.querySelectorAll('.food-item');
    
    removeButtons.forEach((button, index) => {
        // Enable/disable remove buttons based on number of items
        button.disabled = foodItems.length <= 1;
        
        // Remove existing listeners and add new ones
        button.replaceWith(button.cloneNode(true));
    });
    
    // Re-add event listeners to remove buttons
    document.querySelectorAll('.remove-food-item').forEach(button => {
        button.addEventListener('click', function() {
            if (document.querySelectorAll('.food-item').length > 1) {
                this.closest('.input-group').remove();
                updateRemoveButtons();
            }
        });
    });
}

async function handleFormSubmit(e) {
    e.preventDefault();
    
    // Show loading state
    showLoading();
    
    try {
        // Collect form data
        const formData = collectFormData();
        
        // Validate form data
        if (!validateFormData(formData)) {
            hideLoading();
            return;
        }
        
        // Make API call
        const response = await axios.post('/analyze', formData, {
            headers: {
                'Content-Type': 'application/json'
            }
        });
        
        // Display results
        displayResults(response.data);
        
    } catch (error) {
        console.error('Error:', error);
        showError(error.response?.data?.detail || 'An error occurred while analyzing your nutrition data.');
    } finally {
        hideLoading();
    }
}

function collectFormData() {
    // Collect food items
    const foodItems = Array.from(document.querySelectorAll('.food-item'))
        .map(input => input.value.trim())
        .filter(value => value !== '');
    
    // Collect user preferences
    const age = parseInt(document.getElementById('age').value);
    const gender = document.getElementById('gender').value;
    const goal = document.getElementById('goal').value || null;
    const dietPreference = document.getElementById('diet_preference').value || null;
    const calorieTarget = document.getElementById('calorie_target').value 
        ? parseInt(document.getElementById('calorie_target').value) 
        : null;
    
    const allergiesInput = document.getElementById('allergies').value.trim();
    const allergies = allergiesInput 
        ? allergiesInput.split(',').map(allergy => allergy.trim()).filter(allergy => allergy !== '')
        : [];
    
    return {
        food_items: foodItems,
        user_preferences: {
            age: age,
            gender: gender,
            goal: goal,
            diet_preference: dietPreference,
            allergies: allergies,
            calorie_target: calorieTarget
        }
    };
}

function validateFormData(formData) {
    if (formData.food_items.length === 0) {
        showError('Please enter at least one food item.');
        return false;
    }
    
    if (!formData.user_preferences.age || formData.user_preferences.age < 1) {
        showError('Please enter a valid age.');
        return false;
    }
    
    if (!formData.user_preferences.gender) {
        showError('Please select your gender.');
        return false;
    }
    
    return true;
}

function showLoading() {
    document.getElementById('loading').classList.remove('d-none');
    document.getElementById('results').classList.add('d-none');
    document.getElementById('no-results').classList.add('d-none');
    document.getElementById('error-message').classList.add('d-none');
}

function hideLoading() {
    document.getElementById('loading').classList.add('d-none');
}

function displayResults(data) {
    // Hide other sections
    document.getElementById('no-results').classList.add('d-none');
    document.getElementById('error-message').classList.add('d-none');
    
    // Show results section
    document.getElementById('results').classList.remove('d-none');
    
    // Display summary
    document.getElementById('summary-text').textContent = data.summary;
    
    // Display nutrient comparison
    displayNutrientComparison(data.comparison);
    
    // Display recommendations
    displayRecommendations(data.recommendations);
}

function displayNutrientComparison(comparison) {
    const container = document.getElementById('nutrient-comparison');
    container.innerHTML = '';
    
    comparison.forEach(nutrient => {
        const percentage = nutrient.required > 0 ? (nutrient.consumed / nutrient.required) * 100 : 0;
        const statusClass = nutrient.status.toLowerCase();
        
        const nutrientCard = document.createElement('div');
        nutrientCard.className = `nutrient-card ${statusClass}`;
        nutrientCard.innerHTML = `
            <div class="d-flex justify-content-between align-items-center mb-2">
                <h6 class="mb-0">${nutrient.nutrient}</h6>
                <span class="badge bg-${getStatusBadgeColor(nutrient.status)}">${nutrient.status.toUpperCase()}</span>
            </div>
            <div class="row">
                <div class="col-6">
                    <small class="text-muted">Consumed: ${nutrient.consumed.toFixed(1)}</small>
                </div>
                <div class="col-6">
                    <small class="text-muted">Required: ${nutrient.required.toFixed(1)}</small>
                </div>
            </div>
            <div class="progress mt-2" style="height: 8px;">
                <div class="progress-bar bg-${getStatusBadgeColor(nutrient.status)}" 
                     style="width: ${Math.min(percentage, 100)}%"></div>
            </div>
            <small class="text-muted">${percentage.toFixed(1)}% of requirement</small>
        `;
        
        container.appendChild(nutrientCard);
    });
}

function displayRecommendations(recommendations) {
    const container = document.getElementById('recommendations-list');
    container.innerHTML = '';
    
    recommendations.forEach(recommendation => {
        const listItem = document.createElement('li');
        listItem.className = 'recommendation-item';
        listItem.innerHTML = `
            <i class="fas fa-check-circle text-success me-2"></i>
            ${recommendation}
        `;
        container.appendChild(listItem);
    });
}

function getStatusBadgeColor(status) {
    switch(status.toLowerCase()) {
        case 'low': return 'danger';
        case 'high': return 'warning';
        case 'ok': return 'success';
        default: return 'secondary';
    }
}

function showError(message) {
    document.getElementById('error-text').textContent = message;
    document.getElementById('error-message').classList.remove('d-none');
    document.getElementById('results').classList.add('d-none');
    document.getElementById('no-results').classList.add('d-none');
}