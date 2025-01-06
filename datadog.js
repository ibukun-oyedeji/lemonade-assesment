// This js code snippet will imports the necessary modules (datadogLogs and datadogRum) from the Datadog React Native SDK. 

import { datadogLogs, datadogRum } from '@datadog/mobile-react-native';

datadogLogs.initialize({
    clientToken: 'YOUR_DATADOG_CLIENT_TOKEN',
    env: 'production', 
});

datadogRum.initialize({
    applicationId: 'YOUR_DATADOG_APPLICATION_ID',
    clientToken: 'YOUR_DATADOG_CLIENT_TOKEN',
    env: 'production',
});
