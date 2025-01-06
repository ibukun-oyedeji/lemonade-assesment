// This js snippet imports the Rum module for Real User Monitoring, also contains a standard fetch call to the API endpoint.

import { Rum } from '@datadog/mobile-react-native';

fetch('YOUR_API_ENDPOINT')
  .then(response => {
    if (!response.ok) {
      Rum.addCurrentNetworkError(response.status, response.statusText);
    }
    return response.json();
  })
  .then(data => {
    // Process data
  })
  .catch(error => {
    Rum.addError(error); 
  });
