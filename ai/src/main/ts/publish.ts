const apiBaseUrl = 'https://admin.hlx.page/'
const organisation = 'netcentric';
const repository = 'eds-solari';
const branch = 'main';

async function post(getEndpoint: (path: string) => string, path: string): Promise<void> {
  const endpoint = getEndpoint(path);
  const response = await fetch(endpoint, {
    method: "POST",
  });
  if (!response.ok) {
    throw new Error(`Error while calling ${endpoint}, status = ${response.status}`);
  }
  console.log(`${endpoint}: `, await response.json());
}

const getPreviewEndpoint = (path: string) => `${apiBaseUrl}preview/${organisation}/${repository}/${branch}/${path}`;
const getPublishEndpoint = (path: string) => `${apiBaseUrl}live/${organisation}/${repository}/${branch}/${path}`;


post(getPreviewEndpoint, 'test');
post(getPublishEndpoint, 'test');

export { post };