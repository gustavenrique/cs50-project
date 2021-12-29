const imgDiv = document.querySelector('.image-div')
const inpfile = document.querySelector('#inpFile')
const image = document.querySelector('.preview-img')

inpFile.addEventListener('change', function() {
    // Get the files from the input
    const file = this.files[0]
    
    // If there is a file
    if (file) {
        let reader =  new FileReader()
        
        reader.addEventListener('load', function() {
            image.setAttribute('src', this.result)
        })
        
        // Display the image div
        imgDiv.style.display = 'flex'
        
        // And display the image to the user after reading it
        reader.readAsDataURL(file)
    }
})