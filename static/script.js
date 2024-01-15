document.getElementById('fileToUpload').addEventListener('change', function(e) {
    var file = e.target.files[0];
    if (!file) return;

    var formData = new FormData();
    formData.append('fileToUpload', file);

    var xhr = new XMLHttpRequest();
    xhr.open('POST', '/upload', true);

    // Show the loading bar
    var loadingBar = document.getElementById('loadingBar');
    var loadingProgress = document.getElementById('loadingProgress');
    loadingBar.style.display = 'block';

    xhr.upload.onprogress = function(e) {
        if (e.lengthComputable) {
            var percentComplete = (e.loaded / e.total) * 100;
            loadingProgress.style.width = percentComplete + '%';
        }
    };

    xhr.onload = function() {
        if (xhr.status === 200) {
            loadingBar.style.display = 'block';
            var response = JSON.parse(xhr.responseText);
            alert('Upload complete! Your code is: ' + response.code);
        } else {
            alert('Upload failed.');
        }
    };

    xhr.send(formData);
});