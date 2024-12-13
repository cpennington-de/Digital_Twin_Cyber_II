document.getElementById('readText').addEventListener('click', function() {
  chrome.tabs.query({ active: true, currentWindow: true }, function(tabs) {
    chrome.scripting.executeScript({
      target: { tabId: tabs[0].id },
      func: () => window.location.href  // Get page URL
    }, (results) => {
      if (results && results[0] && results[0].result) {
        const url = results[0].result;

        // Send the URL to the Python server
        fetch('http://127.0.0.1:5000/process_text', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({ url })
        })
        .then(response => response.json())
        .then(data => {
          if (data.is_phishing) {
            document.getElementById('content').innerText = 'Warning: This website might be a phishing attempt!';
          } else {
            document.getElementById('content').innerText = 'This website appears safe.';
          }
        })
        .catch(error => {
          console.error('Error:', error);
          document.getElementById('content').innerText = 'Error processing URL. Is the Python server running?';
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
        
        fetch('http://127.0.0.1:5000/extract-features', {
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