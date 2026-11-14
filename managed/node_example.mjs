// npm i apify-client
// APIFY_TOKEN=... node node_example.mjs
import { ApifyClient } from 'apify-client';

const client = new ApifyClient({ token: process.env.APIFY_TOKEN });
const run = await client.actor('goldfoot/ats-jobs-feed').call({
    companies: ['https://boards.greenhouse.io/stripe', 'ashby:linear', 'notion.so'],
    remoteOnly: true,
    includeDescription: false,
});
const { items } = await client.dataset(run.defaultDatasetId).listItems();
console.table(items.map((j) => ({ company: j.companyName, title: j.title, salary: j.salaryText })));
