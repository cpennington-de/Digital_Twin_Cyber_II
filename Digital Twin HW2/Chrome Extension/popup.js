document.getElementById('readText').addEventListener('click', function() {
  // Get the active tab
  chrome.tabs.query({ active: true, currentWindow: true }, function(tabs) {
    // Use the scripting API to execute a script in the active tab
    chrome.scripting.executeScript({
      target: { tabId: tabs[0].id },
      func: getPageURL
    }, (results) => {
      if (results && results[0] && results[0].result) {
        const url = results[0].result;

        // First extract URL features
        fetch('http://localhost:5000/extract-features', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'Accept': 'application/json'
          },
          body: JSON.stringify({ url })
        })
        .then(response => response.json())
        .then(features => {
          // Display the extracted features
          displayFeatures(features);

          // After features are extracted, send for phishing check
          return fetch('http://127.0.0.1:5000/process_text', {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json'
            },
            body: JSON.stringify({ text: url, features: features })
          });
        })
        .then(response => response.json())
        .then(data => {
          // Display True/False in the popup
          //Will change to reflect the outcome of the model instead of the url containing google
          if (data.contains_google) {
            document.getElementById('content').innerText = 'This website might be a Phishing attempt!';
          } else {
            document.getElementById('content').innerText = 'This website appears to be safe.';
          }
        })
        .catch(error => {
          console.error('Error:', error);
          document.getElementById('content').innerText = 'Error processing text. Is the Python Server running?';
        });
      } else {
        document.getElementById('content').innerText = 'No URL found.';
      }
    });
  });
});

// Test Features button for debugging feature extraction
document.getElementById('testFeatures').addEventListener('click', function() {
  chrome.tabs.query({ active: true, currentWindow: true }, function(tabs) {
    chrome.scripting.executeScript({
      target: { tabId: tabs[0].id },
      func: getPageURL
    }, (results) => {
      if (results && results[0] && results[0].result) {
        const url = results[0].result;
        
        fetch('http://localhost:5000/extract-features', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'Accept': 'application/json'
          },
          body: JSON.stringify({ url })
        })
        .then(response => response.json())
        .then(features => displayFeatures(features))
        .catch(error => {
          console.error('Error:', error);
          document.getElementById('results').innerText = 'Error extracting features';
        });
      }
    });
  });
});

// Helper function to display features in results div
function displayFeatures(features) {
  const resultsDiv = document.getElementById('results');
  resultsDiv.innerHTML = '';
  
  Object.entries(features).forEach(([key, value]) => {
    const featureDiv = document.createElement('div');
    featureDiv.className = 'feature';
    featureDiv.innerHTML = `
      <span>${key}:</span>
      <span>${value}</span>
    `;
    resultsDiv.appendChild(featureDiv);
  });
}

// Close button functionality
document.getElementById('closeButton').addEventListener('click', function() {
  window.close(); // This will close the popup
});

// This function will be executed in the context of the page to get its text content
function getPageText() {
  return document.body.innerText;
}

// This function returns the URL of the current page
function getPageURL() {
  return window.location.href;
}