document.addEventListener('DOMContentLoaded', function() {
    
    const toggle = document.body.querySelector('.toggle-button')
    const navList = document.body.querySelector('.nav-list')
    
    toggle.addEventListener('click', function() {
        navList.classList.toggle('show-nav-list')
    })
})