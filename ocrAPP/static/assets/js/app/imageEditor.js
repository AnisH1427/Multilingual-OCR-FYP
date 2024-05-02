
const cloudName = "drvwg9jwn";
const uploadPreset = "arudwidn";
let imageId = "sample";
const uploadedImage = document.getElementById("uploadedimage");
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

        // Create an img element with the uploaded image URL
        var img = new Image();
        img.crossOrigin = "Anonymous";
        img.onload = function() {
            // Create a canvas element and set its size
            var canvas = document.createElement('canvas');
            canvas.width = 200; // Set the desired width
            canvas.height = 200; // Set the desired height

            // Draw the image onto the canvas
            var ctx = canvas.getContext('2d');
            ctx.drawImage(img, 0, 0, canvas.width, canvas.height);

            // Convert the canvas to a data URL
            var dataUrl = canvas.toDataURL('image/jpeg');

            // Set the src attribute of the img element to the data URL
            img.src = dataUrl;

            // Append the img element to the preview div
            var preview = document.getElementById('preview');
            preview.innerHTML = ''; // Clear the preview div
            preview.appendChild(img);
        };
        img.src = result.info.secure_url;
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
});
}
/* <script>
  var myWidget = cloudinary.createUploadWidget({
    cloudName: 'drvwg9jwn', 
    apiKey: '423176976473914',
    uploadPreset: 'arudwidn',
    cropping: 'client',
    showAdvancedOptions: true,
    croppingAspectRatio: null,
    sources: ['local', 'url', 'camera', 'image_search', 'dropbox', 'google_drive', 'shutterstock', 'adobe_stock'],
    googleApiKey: 'AIzaSyA1_8PjT6xGgxoOTaxWg-ATtmSOKLbWBNM',
    showCompletedButton: false,
    croppingShowDimensions: true,
    multiple: false,
    defaultSource: 'local',
    styles: {
      palette: {
        window: '#FFFFFF',
        sourceBg: '#FFFFFF',
        windowBorder: '#90A0B3',
        tabIcon: '#0094C7',
        inactiveTabIcon: '#69778A',
        menuIcons: '#0094C7',
        link: '#53ad9d',
        action: '#8F5DA5',
        inProgress: '#0194c7',
        complete: '#53ad9d',
        error: '#c43737',
        textDark: '#000000',
        textLight: '#FFFFFF'
      },
      fonts: {
        default: null,
        "'Space Mono', monospace": {
          url: 'https://fonts.googleapis.com/css?family=Space+Mono',
          active: true
        }
      },
      widgetWidth: '500px',
      widgetHeight: '500px'
    }
  }, (error, result) => { 
    if (!error && result && result.event === "success") { 
      console.log('Done! Here is the image info: ', result.info); 
    }
  })

  document.getElementById("upload_widget").addEventListener("click", function(){
      myWidget.open();
  }, false);
</script> */