import { Client } from '@elastic/elasticsearch';

const client = new Client({ node: 'http://localhost:9200' });

async function getCategoryFacets(query) {
  const response = await client.search({
    index: 'products',
    size: 0,
    query: { match: { name: query } },
    aggs: {
      categories: {
        terms: { field: 'category.keyword', size: 20 },
      },
      brands: {
        terms: { field: 'brand.keyword', size: 20 },
      },
    },
  });

  return {
    categories: response.aggregations.categories.buckets,
    brands: response.aggregations.brands.buckets,
  };
}

async function getRevenueHistogram() {
  const response = await client.search({
    index: 'orders',
    size: 0,
    aggs: {
      sales_over_time: {
        date_histogram: {
          field: 'created_at',
          calendar_interval: 'month',
        },
        aggs: {
          revenue: { sum: { field: 'total_amount' } },
          avg_order_value: { avg: { field: 'total_amount' } },
        },
      },
    },
  });

  return response.aggregations.sales_over_time.buckets;
}

async function paginateComposite(afterKey = null) {
  const response = await client.search({
    index: 'events',
    size: 0,
    aggs: {
      events_by_region: {
        composite: {
          size: 100,
          sources: [
            { region: { terms: { field: 'region.keyword' } } },
            { day: { date_histogram: { field: 'timestamp', calendar_interval: 'day' } } },
          ],
          ...(afterKey && { after: afterKey }),
        },
      },
    },
  });

  const { buckets, after_key } = response.aggregations.events_by_region;

  if (after_key) {
    console.log(`Got ${buckets.length} buckets, fetching next page...`);
    return [...buckets, ...await paginateComposite(after_key)];
  }

  return buckets;
}

const query = process.argv[2] || 'laptop';
const facets = await getCategoryFacets(query);
console.log('Facets:', facets);
