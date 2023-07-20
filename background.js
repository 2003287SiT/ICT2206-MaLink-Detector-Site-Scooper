// Listen for the click event on the browser action (extension icon)
chrome.action.onClicked.addListener((tab) => {
    
    // Execute content script in the active tab
    chrome.scripting.executeScript({
      target: { tabId: tab.id },
      function: () => {

        // Collect the links on the page
        const links = Array.from(document.querySelectorAll('a[href]'));

        // Extract the href values from the links
        const hrefs = links.map(link => link.href);

        // Send the links back to the extension
        chrome.runtime.sendMessage({ links: hrefs });
      },
    });
  });
  
  // Listen for incoming messages from the extension popup or content script
  chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
    if (message.generateHTML) {
      generateHtmlPage(message.links);
    }
  });
  
  function generateHtmlPage(links) {
    var htmlContent = '<html><head><title>MaLink Detector Links</title></head><body>';
    htmlContent += '<h1>MaLink Detector Links</h1>';
    htmlContent += '<ul>';
    links.forEach(function(link) {
      htmlContent += '<li><a href="' + link + '">' + link + '</a></li>';
    });
    htmlContent += '</ul>';
    htmlContent += '</body></html>';
  
    // Create a Blob with the HTML content
    var blob = new Blob([htmlContent], { type: 'text/html' });
  
    // Create a URL from the Blob
    var url = URL.createObjectURL(blob);
  
    // Open the URL in a new tab
    chrome.tabs.create({ url: url });
  
    // Revoke the URL after opening the tab to release resources
    URL.revokeObjectURL(url);
  }
  