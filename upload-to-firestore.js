const admin = require('firebase-admin');
const fs = require('fs');
const path = require('path');
const csv = require('csv-parser');

// ใช้ Firebase Admin SDK
const serviceAccount = require('./firebase-key.json');

// เริ่มต้น Firebase
admin.initializeApp({
  credential: admin.credential.cert(serviceAccount),
});

const db = admin.firestore();

// อ่านทุกไฟล์ .csv ใน current directory
fs.readdirSync('.')
  .filter(file => file.endsWith('.csv'))  // เลือกเฉพาะไฟล์ .csv
  .forEach(file => {
    const filePath = path.join('.', file);
    console.log(`Uploading data from: ${filePath}`);
    
    // อ่านไฟล์ CSV
    fs.createReadStream(filePath)
      .pipe(csv())
      .on('data', async (row) => {
        try {
          // อัปโหลดแต่ละแถวเข้า Firestore
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
