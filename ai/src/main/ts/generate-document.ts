import OpenAI from 'openai';
import { writeFileSync } from 'fs';

import secrets from '../secrets/chatgpt-key.json';

const openai = new OpenAI({
  apiKey: secrets.key
});

async function main(input: string) {
  const chatCompletion = await openai.chat.completions.create({
    messages: [
      { role: 'system', content: `You are a markdown generator. The documents your are generating are used as content for websites. The Content Management system which will use the markdown as content for websites is called Adobe Experience Manager, more specifically a feature within it called Edge Delivery Services. 

      The markdown documents can use headlines, ordered lists, unordered lists. Tables have a special semantic therefore they should not be used for typical content structuring but are reserved for layouting of the content.

      Contend layouted with with tables is called a block. Each block has a name which is the first cell of the table and spans all columns forming a header row. The rest of the stucture of the blocks' table is defined for each block individually. There are the following blocks you can use to layout the content:
      - "Hero": typically used at the very top of the page consisting of a background image, a headline and short teaser text to start the content presentation. Additional instances of this block might be used to introduce important sections of the document but should be used scarce. The structure of the block below the header row is one cell containing an image, a headline and a short description all to tease the following content.
      - "Column": the column block can be used to show text beside an image or to show two options beside each other. Below the header row the column block has two columns each containing the content shown beside each other.
      - "Cards": the cards block can be used to show 3 or more options in a gallery give the reader a good overview of the choices or attributes. Below the header row the cards block has a row with one column for each card. The content structure should be similar for each card.
      ` },
      { role: 'user', content: input },
    ],
    model: 'gpt-3.5-turbo',
  });
  chatCompletion.choices.forEach((choice) => {
    console.log(choice);
    writeFileSync('out/eds-doc.md', choice.message.content || '');
  });
}

main('Generate a markdown document for a space ship.');