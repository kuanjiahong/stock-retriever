# stock-retriever
Use Google APIs to retrieve stock prices and update it onto Google Sheet


## Set up
1. Follow the instructions to enable Google API, install Google API library and generate `credentials.json` file

   [Python quickstart for Google API](https://developers.google.com/docs/api/quickstart/python)

2. Go to the website to get your API key

   [Financial Modelling Prep](https://site.financialmodelingprep.com/)

3. Create a Google Sheet document and note down the spreadsheet ID (you can obtained it from the spreadsheet URL)

   [Google Sheets API Overview](https://developers.google.com/sheets/api/guides/concepts)


4. Authentication with Google Service Account

   [Google OAuth2 with service account](https://developers.google.com/identity/protocols/oauth2/service-account#python)


6. Schedule Cloud Functions

   Topic name: `stocks`
   
   [Schedule a Cloud Function using Pub/Sub](https://cloud.google.com/scheduler/docs/tut-pub-sub)
