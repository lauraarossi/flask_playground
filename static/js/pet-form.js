document.addEventListener('DOMContentLoaded', function() {
    const numPetsSelect = document.getElementById('numPets');
    const petButtonsSection = document.getElementById('petButtonsSection');
    const petButtons = document.getElementById('petButtons');
    const petInfoSection = document.getElementById('petInfoSection');
    const currentPetText = document.getElementById('currentPetText');
    const currentPetNumber = document.getElementById('currentPetNumber');
    const petForm = document.getElementById('petForm');
    let selectedPetNumber = null;
    
    // Get added pets from template (these will be passed from Flask)
    const addedPets = window.addedPets || [];
    const totalPets = window.totalPets || 0;
    
    // Handle dropdown change
    numPetsSelect.addEventListener('change', function() {
        const selectedValue = parseInt(this.value);
        
        if (selectedValue === 0) {
            // Hide both sections
            petButtonsSection.style.display = 'none';
            petInfoSection.style.display = 'none';
            petButtons.innerHTML = '';
            selectedPetNumber = null;
        } else {
            // Show pet buttons section
            petButtonsSection.style.display = 'block';
            petInfoSection.style.display = 'none';
            
            // Generate pet buttons
            petButtons.innerHTML = '';
            for (let i = 1; i <= selectedValue; i++) {
                const button = document.createElement('button');
                button.type = 'button';
                button.className = 'pet-button';
                button.textContent = `Pet ${i}`;
                button.dataset.petNumber = i;
                
                // Check if this pet has already been added
                if (addedPets.includes(i)) {
                    button.classList.add('added');
                    button.textContent = `Pet ${i} ✓`;
                    button.disabled = true;
                }
                
                button.addEventListener('click', function() {
                    // Don't allow clicking on already added pets
                    if (addedPets.includes(i)) {
                        return;
                    }
                    
                    // Remove selected class from all buttons
                    document.querySelectorAll('.pet-button').forEach(btn => {
                        btn.classList.remove('selected');
                    });
                    
                    // Add selected class to clicked button
                    this.classList.add('selected');
                    
                    // Show pet info section
                    petInfoSection.style.display = 'block';
                    
                    // Update current pet info
                    const petNumber = this.dataset.petNumber;
                    currentPetText.textContent = `Pet ${petNumber}`;
                    currentPetNumber.value = petNumber;
                    selectedPetNumber = parseInt(petNumber);
                });
                
                petButtons.appendChild(button);
            }
        }
    });
    
    // Form submission validation
    petForm.addEventListener('submit', function(e) {
        const selectedValue = parseInt(numPetsSelect.value);
        
        if (selectedValue === 0) {
            e.preventDefault();
            alert('Please select the number of pets first.');
            return false;
        }
        
        if (selectedPetNumber === null) {
            e.preventDefault();
            alert('Please select a pet to add information for.');
            return false;
        }
        
        // Check if this pet has already been added
        if (addedPets.includes(selectedPetNumber)) {
            e.preventDefault();
            alert('This pet has already been added. Please select a different pet.');
            return false;
        }
        
        // Check if pet information is filled
        const petType = document.querySelector('select[name="pet_type"]').value;
        const sex = document.querySelector('select[name="sex"]').value;
        const age = document.querySelector('input[name="age"]').value;
        const locationType = document.querySelector('select[name="location_type"]').value;
        
        if (!petType || !sex || age === '' || !locationType) {
            e.preventDefault();
            alert('Please complete all pet information fields before submitting.');
            return false;
        }
    });
    
    // Initialize on page load
    if (numPetsSelect.value === '0') {
        petButtonsSection.style.display = 'none';
        petInfoSection.style.display = 'none';
    } else {
        // Trigger change event to show buttons
        numPetsSelect.dispatchEvent(new Event('change'));
    }
});
