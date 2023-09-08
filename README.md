# stock-retriever
Use Google APIs to retrieve stock prices and update it onto Google Sheet

Visit the website: https://kuanjiahong.github.io/stock-retriever/

## Set up
1. Follow the instructions to enable Google API, install Google API library and generate `credentials.json` file

   [Python quickstart for Google API](https://developers.google.com/docs/api/quickstart/python)

   Authentication with Google Service Account

   [Google OAuth2 with service account](https://developers.google.com/identity/protocols/oauth2/service-account#python)

   After creating a service account, remember to add the service account email into the Google Spreadsheet

3. Go to the Financial Modeling Prep to get your API key

   [Financial Modeling Prep](https://site.financialmodelingprep.com/developer/docs/)

4. Create a Google Sheet document and note down the spreadsheet ID (you can obtained it from the spreadsheet URL)

   [Google Sheets API Overview](https://developers.google.com/sheets/api/guides/concepts)


5. Schedule Cloud Functions

   Topic name: `stocks`
   
   [Schedule a Cloud Function using Pub/Sub](https://cloud.google.com/scheduler/docs/tut-pub-sub)
