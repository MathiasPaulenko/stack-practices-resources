// AWS SDK v3 configuration for CDN invalidation
// Requires: npm install @aws-sdk/client-cloudfront
import { CloudFrontClient, CreateInvalidationCommand } from '@aws-sdk/client-cloudfront';

const cloudfront = new CloudFrontClient({ region: 'us-east-1' });

/**
 * Invalidate CDN cache for specific paths after deployment
 */
async function invalidateCache(distributionId, paths = ['/*']) {
  const command = new CreateInvalidationCommand({
    DistributionId: distributionId,
    InvalidationBatch: {
      CallerReference: Date.now().toString(),
      Paths: {
        Quantity: paths.length,
        Items: paths
      }
    }
  });

  const response = await cloudfront.send(command);
  console.log(`Invalidation created: ${response.Invalidation.Id}`);
  return response.Invalidation.Id;
}

// Usage: invalidate after static asset deployment
await invalidateCache('E1234567890ABC', ['/assets/*', '/index.html']);
