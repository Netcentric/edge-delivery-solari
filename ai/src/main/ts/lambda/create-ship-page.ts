import { post } from '../publish';

const handler = (): LambdaResponse => {
  console.log(post);
  return {
    statusCode: 200,
    headers: {},
    body: 'Hello World',
  };
};

export { handler };