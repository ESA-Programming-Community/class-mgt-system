document.addEventListener('DOMContentLoaded', function() {
    // Select the file links in the admin interface
    const fileLinks = document.querySelectorAll('a[href^="/media/submissions/"]');

    // Attach a click event listener to each file link
    fileLinks.forEach(function(link) {
        link.addEventListener('click', function(event) {
            event.preventDefault(); // Prevent default link behavior (opening in the browser)

            const fileUrl = this.getAttribute('href'); // Get the file URL
            const fileName = fileUrl.split('/').pop(); // Extract file name from URL

            // Create a temporary anchor element to trigger the download
            const downloadLink = document.createElement('a');
            downloadLink.setAttribute('href', fileUrl);
            downloadLink.setAttribute('download', fileName);
            downloadLink.style.display = 'none';

            document.body.appendChild(downloadLink); // Append the link to the document
            downloadLink.click(); // Simulate a click to trigger the download

            document.body.removeChild(downloadLink); // Remove the temporary link from the document
        });
    });
});