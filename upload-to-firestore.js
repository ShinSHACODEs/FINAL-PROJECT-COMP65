const admin = require('firebase-admin');
const fs = require('fs');
const path = require('path');
const csv = require('csv-parser');

const serviceAccount = require('./firebase-key.json');

admin.initializeApp({
  credential: admin.credential.cert(serviceAccount),
});

const db = admin.firestore();

// อ่านทุกไฟล์ .csv ใน current directory
fs.readdirSync('.')
  .filter(file => file.endsWith('.csv'))
  .forEach(file => {
    console.log(`Uploading data from: ${file}`);
    fs.createReadStream(file)
      .pipe(csv())
      .on('data', async (row) => {
        try {
          await db.collection('weather_data').add(row);
          console.log('Uploaded row:', row);
        } catch (error) {
          console.error('Error uploading:', error);
        }
      })
      .on('end', () => {
        console.log(`Finished uploading ${file}`);
      });
  });
