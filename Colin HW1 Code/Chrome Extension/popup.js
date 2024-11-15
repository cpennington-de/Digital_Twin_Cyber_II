document.getElementById('readText').addEventListener('click', function() {
  // Get the active tab
  chrome.tabs.query({ active: true, currentWindow: true }, function(tabs) {
    // Use the scripting API to execute a script in the active tab
    chrome.scripting.executeScript({
      target: { tabId: tabs[0].id },
      func: getPageText
    }, (results) => {
      if (results && results[0] && results[0].result) {
        const text = results[0].result;

        // Send the text to the Python server
        fetch('http://127.0.0.1:5000/process_text', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({ text: text })
        })
        .then(response => response.json())
        .then(data => {
          // Display the processed text in the popup, using innerHTML to allow HTML rendering
          document.getElementById('content').innerHTML = data.processed_text;
        })
        .catch(error => {
          console.error('Error:', error);
          document.getElementById('content').innerText = 'Error processing text. Is the Python Server running?';
        });
      } else {
        document.getElementById('content').innerText = 'No text found.';
      }
    });
  });
});

// Close button functionality
document.getElementById('closeButton').addEventListener('click', function() {
  window.close(); // This will close the popup
});

// This function will be executed in the context of the page to get its text content
function getPageText() {
  return document.body.innerText;
}

document.getElementById("readText").addEventListener("click", () => {
  const color = document.getElementById("colorPicker").value;
  chrome.tabs.query({ active: true, currentWindow: true }, (tabs) => {
    chrome.scripting.executeScript({
      target: { tabId: tabs[0].id },
      func: (color) => {
        document.body.style.backgroundColor = color;
      },
      args: [color]
    });
  });
});
