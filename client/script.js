// Retrieve the client's IP address
fetch('https://api.myip.com')
  .then(response => response.json())
  .then(data => {
    const ipAddress = data.ip;
    const ipAddressElement = document.getElementById('ip-address');
    ipAddressElement.textContent = ipAddress;
  })
  .catch(error => {
    console.error('Error:', error);
  });
