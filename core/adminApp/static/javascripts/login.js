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