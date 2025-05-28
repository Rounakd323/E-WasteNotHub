// Set max date for DOB (18+ years)
document.getElementById('dob').max = new Date(new Date().setFullYear(new Date().getFullYear() - 18)).toISOString().split('T')[0];

// Role Selection Cards
const roleCards = document.querySelectorAll('.role-card');
roleCards.forEach(card => {
    card.addEventListener('click', function() {
        roleCards.forEach(c => c.classList.remove('active'));
        this.classList.add('active');
        // 🔥 THIS is where the magic happens:
        document.getElementById('role').value = this.dataset.role;
        
        // Show/hide role-specific fields
        document.querySelectorAll('.role-fields').forEach(field => field.style.display = 'none');
        if (this.dataset.role === 'seller') {
            document.getElementById('seller-fields').style.display = 'block';
        } else if (this.dataset.role === 'volunteer') {
            document.getElementById('volunteer-fields').style.display = 'block';
        }
    });
});

// Toggle Password Visibility
document.getElementById('toggle-password').addEventListener('click', function() {
    const passwordField = document.getElementById('password');
    const icon = this.querySelector('i');
    passwordField.type = passwordField.type === 'password' ? 'text' : 'password';
    icon.className = passwordField.type === 'password' ? 'bi bi-eye' : 'bi bi-eye-slash';
});

// Password Strength Meter
document.getElementById('password').addEventListener('input', function(e) {
    const strengthIndicator = document.querySelector('.strength-indicator');
    const strengthText = document.querySelector('.strength-text');
    const strength = calculatePasswordStrength(e.target.value);
    
    strengthIndicator.className = 'strength-indicator flex-grow-1';
    
    if (strength < 30) {
        strengthIndicator.classList.add('bg-danger');
        strengthText.textContent = 'Weak';
    } else if (strength < 70) {
        strengthIndicator.classList.add('bg-warning');
        strengthText.textContent = 'Medium';
    } else {
        strengthIndicator.classList.add('bg-success');
        strengthText.textContent = 'Strong';
    }
    
    strengthIndicator.style.width = `${strength}%`;
});

function calculatePasswordStrength(password) {
    let strength = 0;
    if (password.length > 0) strength += Math.min(password.length * 5, 50);
    if (/[A-Z]/.test(password)) strength += 10;
    if (/[0-9]/.test(password)) strength += 15;
    if (/[^A-Za-z0-9]/.test(password)) strength += 25;
    return Math.min(strength, 100);
}

// Animate form on load
document.addEventListener('DOMContentLoaded', () => {
    const form = document.querySelector('form');
    form.style.opacity = 0;
    form.style.transform = 'translateY(20px)';
    
    setTimeout(() => {
        form.style.transition = 'opacity 0.6s, transform 0.6s';
        form.style.opacity = 1;
        form.style.transform = 'translateY(0)';
    }, 300);
});

// Message after the form submisison
document.addEventListener('DOMContentLoaded', function () {
    const alerts = document.querySelectorAll('.alert');

    alerts.forEach(function (alert) {
        setTimeout(function () {
            // Add the Bootstrap 'fade' and 'show' classes to animate the disappearance
            alert.classList.remove('show');
            alert.classList.add('hide');

            // Optional: completely remove the alert from the DOM after fade out
            setTimeout(() => {
                alert.remove();
            }, 500); // wait for fade transition to complete before removing
        }, 5000); // 5 seconds
    });
});

// Form Submission
document.querySelector('form').addEventListener('submit', function(e) {
    const submitBtn = this.querySelector('button[type="submit"]');
    const submitText = submitBtn.querySelector('.submit-text');
    
    submitBtn.disabled = true;
    submitText.textContent = 'Processing...';
    submitBtn.classList.add('btn-loading');

    // Let the form submit as usual (no preventDefault)
});

// for the comany interactivity
document.querySelectorAll('.role-card').forEach(card => {
    card.addEventListener('click', () => {
        document.querySelectorAll('.role-card').forEach(c => c.classList.remove('active'));
        card.classList.add('active');
        const selectedRole = card.getAttribute('data-role');
        document.getElementById('role').value = selectedRole;

        // 👇 Show/hide company fields based on selected role
        const companyFields = document.getElementById('company-fields');
        if (selectedRole === 'company') {
            companyFields.style.display = 'block';
        } else {
            companyFields.style.display = 'none';
        }

        // (Optional) Hide DOB, Gender, etc., if company is selected
        // Example:
        // document.getElementById('dob').closest('.mb-3').style.display = (selectedRole === 'company') ? 'none' : 'block';
    });
});