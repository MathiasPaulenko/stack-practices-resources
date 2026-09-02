async function* fetchPages(baseUrl, totalPages, pageSize = 100) {
  for (let offset = 0; offset < totalPages; offset += pageSize) {
    const url = `${baseUrl}?offset=${offset}&limit=${pageSize}`;
    const response = await fetch(url);
    const data = await response.json();
    if (data.length === 0) break;
    yield data;
  }
}

async function* fetchLines(filePath) {
  const fs = await import('fs/promises');
  const fileHandle = await fs.open(filePath, 'r');
  try {
    for await (const line of fileHandle.readLines()) {
      yield line.trim();
    }
  } finally {
    await fileHandle.close();
  }
}

async function processAll() {
  let total = 0;
  for await (const page of fetchPages("https://api.example.com/items", 10000)) {
    for (const item of page) {
      total += item.price;
    }
    console.log(`Processed page, running total: ${total}`);
  }
  console.log(`Final total: ${total}`);
}

async function processWithEarlyExit() {
  const gen = fetchPages("https://api.example.com/items", 10000);
  try {
    for await (const page of gen) {
      if (page.length === 0) break;
      console.log(`Got ${page.length} items`);
      break;
    }
  } finally {
    await gen.return();
  }
}

processAll();
