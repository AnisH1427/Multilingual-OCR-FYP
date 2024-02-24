// document.querySelector('.drop').addEventListener('dragover', function(e) {
//     //prevent the default behavior of the event to allow dropping
//   e.preventDefault();

//   //adding dragging class to the dropzone for visual feedback
//   this.classList.add('dragging');
// });

// //add the dragleave event listener to the dropzone for removing the dragging class
// document.querySelector('.drop').addEventListener('dragleave', function(e) {
//     //remove the dragging class from the dropzone
//   this.classList.remove('dragging');
// });

// document.querySelector('.drop').addEventListener('drop', function(e) {
//     //prevent the default behavior of the event to allow dropping
//     e.preventDefault();

//     //remove the dragging class from the dropzone
//     this.classList.remove('dragging');

//     //get the files from the DataTransfer object
//     var file = e.dataTransfer.files[0];

//     var formData= new FormData();
//     formData.append('file',file);
     
//     fetch('/', {
//         method: 'POST',
//         body: formData
//     }).then(response => {
//         if(response.ok){
//             console.log('File uploaded successfully');
//         } else{
//             console.log('File not uploaded');
//         }
//     }).catch(error => {
//         console.log('Error:', error);
//     })
// });

// document.querySelector('.browse').addEventListener('click',function(){
//     document.querySelector('#files').click();
// });

// document.querySelector('#files').addEventListener('change',function(){
//     var file = this.files[0];
//     var formData= new FormData();
//     formData.append('file',file);
     
//     fetch('/', {
//         method: 'POST',
//         body: formData
//     }).then(response => {
//         if(response.ok){
//             console.log('File uploaded successfully');
//         } else{
//             console.log('File not uploaded');
//         }
//     }).catch(error => {
//         console.log('Error:', error);
//     })
// });