import { GoogleAuth }  from 'google-auth-library';
import { google } from 'googleapis';

import secrets from '../secrets/google-drive-key.json'

const shipRootFolder = '14P-wWqCy0qvoJulEEFm13wYDpKRcEl1m';
const targetRootFolder = '1AQUeaAGTFiwLtgyZif7Wfgj4mCU7v731';

const colorRegex = /-color(\d)\.\w{3,5}$/;
const shipNameRegex = /^(\w+_)?(.*)$/;

async function list(): Promise<void> {
  const focusResponse = await fetch('https://astrocraft.innovationlab.cx/focus/query-index.json');
  const focuses = await focusResponse.json();

  const auth = new GoogleAuth({credentials: secrets, scopes: ['https://www.googleapis.com/auth/drive']});
  const service = google.drive({version: 'v3', auth});

  const rootResponse = await service.files.list({
    pageSize: 1000,
    q: `mimeType='application/vnd.google-apps.folder' and '${shipRootFolder}' in parents and trashed=false`,
    spaces: 'drive',
    supportsAllDrives: true,
    includeItemsFromAllDrives: true,
  });
  let queryIndex = 'focus-path;stellar-silver;sunset-on-mars;ocean-blue;galaxy-teal;titan-grey;\n';
  for(let shipFolder of rootResponse.data.files || []) {
  // const shipFolder = (rootResponse.data.files || [])[2];
    const shipResponse = await service.files.list({
      pageSize: 1000,
      q: `name='03_final_screen' and mimeType='application/vnd.google-apps.folder' and '${shipFolder.id}' in parents and trashed=false`,
      spaces: 'drive',
      supportsAllDrives: true,
      includeItemsFromAllDrives: true,
    });
    if(shipResponse.data.files?.length === 1) {
      const filesResponse = await service.files.list({
        pageSize: 1000,
        q: `'${(shipResponse.data.files || [])[0].id}' in parents and trashed=false`,
        spaces: 'drive',
        supportsAllDrives: true,
        includeItemsFromAllDrives: true,
      });
      const files = filesResponse.data.files
        ?.map((file) => {
          const match = file.name?.match(colorRegex);
          if(!match) {
            return null;
          }
          return {
            color: parseInt(match[1]),
            ...file
          }
        })
        .filter((file) => file)
        .sort((a, b) => (a?.color || 0) - (b?.color || 0));
      if(files?.length !== 5) {
        console.log('invalid files:', filesResponse.data.files?.map((file) => file.name));
      } else {
        const shipName = (shipFolder.name?.match(shipNameRegex) || [,,])[2]?.trim();
        const focus = focuses.data.find((f: any) => f.name === shipName);
        if(!focus) {
          console.log('invalid ship:', shipFolder);
        } else {
          console.log('valid:', focus, files);
          const folderList = await service.files.list({
            q: `name = '${shipName}' and trashed != true and mimeType='application/vnd.google-apps.folder' and '${targetRootFolder}' in parents`,
            fields: 'nextPageToken, files(id, name)',
            spaces: 'drive',
            supportsAllDrives: true,
            includeItemsFromAllDrives: true,
          });
          if (folderList.data.files?.length !== 0) {
            await service.files.update({
              fileId: (folderList.data.files || [])[0].id || undefined,
              supportsAllDrives: true,
              requestBody : {
                trashed: true,
              },
            });
          }
          const shipFolder = await service.files.create({
            requestBody : {
              name: shipName,
              mimeType: 'application/vnd.google-apps.folder',
              parents: [targetRootFolder],
            },
            supportsAllDrives: true,
          });
          queryIndex += `${focus.path};`
          for(let file of files || []) {
            await service.files.copy({
            fileId: (file || {}).id || undefined,
            supportsAllDrives: true,
            requestBody: {
              parents: [shipFolder.data.id || '']
            }});
            console.log('preview', `/configurations/images/${shipName?.toLowerCase().replaceAll(' ', '-')}/${file?.name?.toLowerCase().replaceAll(' ', '-')}`)
            await fetch(`https://admin.hlx.page/preview/netcentric/edge-delivery-solari/main/configurations/images/${shipName?.toLowerCase().replaceAll(' ', '-')}/${file?.name?.toLowerCase().replaceAll(' ', '-')}`, 
              { method: 'POST' });
            console.log('publish')
            const publishResponse = await fetch(`https://admin.hlx.page/live/netcentric/edge-delivery-solari/main/configurations/images/${shipName?.toLowerCase().replaceAll(' ', '-')}/${file?.name?.toLowerCase().replaceAll(' ', '-')}`, 
              { method: 'POST' });
            const publishData = await publishResponse.json();
            const response = await fetch(publishData.live.url, {redirect: 'manual'});
            queryIndex += `https://astrocraft.innovationlab.cx${response.headers.get('location')};`;
          };
          queryIndex += '\n';
        }
      }
    }
  }
  console.log(queryIndex);
}

list();