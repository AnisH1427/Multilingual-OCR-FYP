
const cloudName = "drvwg9jwn";
const uploadPreset = "arudwidn";
let imageId = "sample";
const uploadedImage = document.getElementById("uploadedimage");
var image_url;

const myWidget = cloudinary.createUploadWidget(
    {
        cloudName:cloudName,
        uploadPreset:uploadPreset
    },
    (error,result)=>{
      if(!error && result && result.event === "success"){
        console.log("Done! Here is the image info: ",result.info);

        imageId = result.info.public_id;
        uploadedImage.setAttribute("src",result.info.secure_url);
        uploadedImage.style.width = "200%";
        uploadedImage.style.height = "100%";
        uploadedImage.style.objectFit = "contain";
        createPreviewImage(result.info.secure_url);
    }
    }
)
document.getElementById("upload_widget").addEventListener("click",()=>{
    myWidget.open();
},false);

document.getElementById("edit_widget").addEventListener("click",editImage);

let myEditor;
function editImage(){
    if(myEditor){
        myEditor.hide();
        myEditor.destroy();
        myEditor = null;
    }
    myEditor = cloudinary.mediaEditor();
    myEditor.update({
        publicIds: [imageId],
        cloudName: cloudName,
        image: {
            steps:[
                "resizeAndCrop",
                "export",
            ],
            resizeAndCrop: {
              cropMode: "fixed", // Fixed aspect ratio cropping
              croppingShowDimensions: true, // Show crop dimensions
              cropping: true,
              croppingAspectRatio: 1, // Set your desired aspect ratio here
          },
            export: {  
                "formats":[
                    "auto",
                    "png",
                    "jpg",
                    "webp"
                ],
                "quality":[
                    "auto",
                    55,
                    75,
                    "low"
                ],
                "download":true,
                "share":true
            }
        }
});
myEditor.show();
myEditor.on("export", function(data){
  console.log("Exported", data);

  // Get the URL of the edited image
  const url = data.assets[0].secureUrl;

  // Update the 'src' attribute of the 'uploadedimage' element with the URL of the edited image
  document.getElementById("uploadedimage").setAttribute("src", url);
  createPreviewImage(url);
  image_url=url;
});
}

//function for previewing image inorder to prevent redundant code
function createPreviewImage(url) {
  // Create an img element with the uploaded image URL
  var img = new Image();
  img.crossOrigin = "Anonymous";
  img.onload = function() {

    var preview = document.getElementById('preview');
    
    // Create a canvas element and set its size
    var canvas = document.createElement('canvas');
    
    var ctx = canvas.getContext('2d');

    let rect = preview.getBoundingClientRect();

    let MAX_WIDTH = rect.width;
    let MAX_HEIGHT = rect.height;

    let width = img.width;
    let height = img.height;

  

    canvas.width = width;
    canvas.height = height;

    // Draw the image onto the canvas
    ctx.drawImage(img, 0, 0, width, height);

    // Convert the canvas to a data URL
    var dataUrl = canvas.toDataURL('image/jpeg');

    // Create a new img element for the preview
    var previewImg = new Image();

    previewImg.src = dataUrl;

    // Append the img element to the preview div
    preview.innerHTML = ''; // Clear the preview div
    preview.appendChild(previewImg);
  };
  img.src = url;
  image_url = url;
}

var globalImageBlob;

document.getElementById('detectCharactersButton').addEventListener('click', function(event) {
  event.preventDefault();
  console.log('Detecting characters');

    // Check if an image has been uploaded
    var previewDiv = document.getElementById('preview');
    if (!previewDiv || !previewDiv.innerHTML.includes('<img')) {
      Swal.fire({
        icon: 'error',
        title: 'Oops...',
        text: 'Please upload an image before detecting characters.',
      });
      return;
    }

  // Fetch the image data
  fetch(image_url)
      .then(response => response.blob())
      .then(imageBlob => {

            // Store the image blob in the global variable
          globalImageBlob = imageBlob;

          // Create a FormData object
          var formData = new FormData();

          // Append the image data
          formData.append('document', imageBlob, 'image.jpg');

          // Get the selected edge detection method
          var selectElement = document.getElementById('edge-detection');
          var selectedOption = selectElement.value;

          // Append the selected edge detection method
          formData.append('edge_detection_method', selectedOption);

          console.log(selectedOption);

          // Send the POST request
          return fetch('/app/api/document/', {
              method: 'POST',
              headers: {
                  'X-CSRFToken': '{{ csrf_token }}'
              },
              body: formData
          });
      })
      .then(response => response.blob())
      .then(blob => {
          let preview = document.getElementById('preview');
          let objectURL = URL.createObjectURL(blob);
          preview.innerHTML = '<img src="' + objectURL + '">';
          document.getElementById('predict-button').style.display = 'block';
          document.querySelector('.card').style.display = 'block';
          document.getElementById('predicted-text').innerHTML='<h3 style="color:green">Predicted Text Will Appear Here</h3>';
      })
      .catch(error => {
          console.error('Error:', error);
      });
});

var swiper = new Swiper('.swiper', {
        direction: 'horizontal',
        loop: true,
        navigation: {
            nextEl: '.swiper-button-next',
            prevEl: '.swiper-button-prev',
        },
        pagination: {
            el: '.swiper-pagination',
            clickable: true,
        },
    });

    document.getElementById('nextButton').addEventListener('click', function() {
        swiper.slideNext();
    });

    document.getElementById('prevButton').addEventListener('click', function() {
      swiper.slidePrev();
    });

    /*document.getElementById('prevButton').addEventListener('click', function() {
        swiper.slidePrev();
    });*/

    let language = '';
    let outputFormat = '';
  
      function setLanguage(lang) {
          language = lang;
          console.log(language);
          document.getElementById('languageButton').textContent = language;
      }
  
      function setOutputFormat(format) {
          outputFormat = format;
          console.log(outputFormat);
          document.getElementById('outputFormatButton').textContent = outputFormat;
      }

    
    document.getElementById('predict-button').addEventListener('click', function(event) {
      event.preventDefault();
      if(!language || !outputFormat){
        if(language && !outputFormat){
          text = 'Please select the output format first!';
        } else if(!language && outputFormat){
          text = 'Please select the language first!';
        } else {
          text = 'Please select the language and output format first!';
        }
        // Inject style tag into head
        var style = document.createElement('style');
        style.innerHTML = `
        .swal2-popup {
            font-size: 1.1em !important; /* Change font size */
            width: 25em !important; /* Change width */
        }`;
        document.head.appendChild(style);

        Swal.fire({
          position: 'bottom-end',
          icon: 'error',
          title: 'Oops...',
          text: text,
          timer: 2000
        });
        return;
      }
      console.log('Predicting');
      var file = globalImageBlob; // Get the original file
      var formData = new FormData();
      formData.append('document', file);
      formData.append('language', language);

      // Get the selected edge detection method
      var selectElement = document.getElementById('edge-detection');
      var selectedOption = selectElement.value;

      // Append the selected edge detection method
      formData.append('edge_detection_method', selectedOption);
      
      fetch('/app/api/predict/', {
          method: 'POST',
          headers: {
          'X-CSRFToken': '{{ csrf_token }}'
      },
      body: formData }).then(response => response.text())
      .then(data => {
        console.log(data);
// Handle the final_predictions here
var final_predictions = JSON.parse(data);  // Parse the data as JSON

var predictedElement = document.getElementById('predicted-text');
predictedElement.innerHTML = '';
 // Add the style dynamically
 predictedElement.style.whiteSpace = 'pre';
 predictedElement.style.width = '750px';
 predictedElement.style.height = '150px';
 predictedElement.style.overflow = 'auto';
 predictedElement.style.fontStyle = 'regular';

 if(selectedOption=="chain_word"){
  predictedElement.innerHTML += final_predictions;
  }
  else{
    var i = 0;
    function typeWriter() {
    
    if (i < final_predictions.length) {
        predictedElement.innerHTML += final_predictions[i] + '<br>';
        i++;
        setTimeout(typeWriter, 200);  // Adjust the speed of the typing effect here
    }
}
typeWriter();
  }

})
.catch(error => console.error('Error:', error.message));
  });
