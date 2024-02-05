import { GoogleAuth }  from 'google-auth-library';
import { google } from 'googleapis';
import { createReadStream } from 'fs';

import secrets from '../secrets/google-drive-key.json'

const driveShare = '0AJjRhcTZbIKsUk9PVA';
const driveFolder = '1OME3hUxm5zYtBsVlUfKal2O5qmdW3ehE';

async function upload(filePath: string): Promise<void> {
  const auth = new GoogleAuth({credentials: secrets, scopes: ['https://www.googleapis.com/auth/drive']});
  const service = google.drive({version: 'v3', auth});
  const requestBody = {
    name: 'photo.jpg',
    parents: [driveFolder],
    driveId: driveShare,
    supportsAllDrives: true,
  };
  const media = {
    mimeType: 'image/jpeg',
    body: createReadStream(filePath),
  };
  const driveFile = await service.files.create({
    requestBody,
    media: media,
    supportsAllDrives: true,
  });
  console.log('File Id:', driveFile.data.id);
  console.log(driveFile.data.id);
}

upload('/Users/andreashaller/Pictures/samples/munich-1220908_1280.jpg');