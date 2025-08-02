// GreenObasket Service Worker for Offline Support
const CACHE_NAME = 'greenobasket-v1.0.0';
const urlsToCache = [
  '/',
  '/shop',
  '/static/manifest.json',
  '/static/images/logo.png',
  // Add other static assets as needed
];

// Install Service Worker
self.addEventListener('install', (event) => {
  event.waitUntil(
    caches.open(CACHE_NAME)
      .then((cache) => {
        console.log('GreenObasket: Service Worker cache opened');
        return cache.addAll(urlsToCache);
      })
  );
});

// Fetch events - serve from cache when offline
self.addEventListener('fetch', (event) => {
  event.respondWith(
    caches.match(event.request)
      .then((response) => {
        // Return cached version or fetch from network
        if (response) {
          return response;
        }
        return fetch(event.request);
      }
    )
  );
});

// Activate Service Worker
self.addEventListener('activate', (event) => {
  event.waitUntil(
    caches.keys().then((cacheNames) => {
      return Promise.all(
        cacheNames.map((cacheName) => {
          if (cacheName !== CACHE_NAME) {
            console.log('GreenObasket: Deleting old cache:', cacheName);
            return caches.delete(cacheName);
          }
        })
      );
    })
  );
});

// Handle background sync for orders when back online
self.addEventListener('sync', (event) => {
  if (event.tag === 'background-sync-orders') {
    event.waitUntil(doBackgroundSync());
  }
});

function doBackgroundSync() {
  // Sync pending orders when back online
  return new Promise((resolve) => {
    console.log('GreenObasket: Background sync for orders');
    resolve();
  });
}

// Push notifications for order updates
self.addEventListener('push', (event) => {
  const options = {
    body: event.data ? event.data.text() : 'Your organic groceries are on the way!',
    icon: '/static/images/icons/icon-192x192.png',
    badge: '/static/images/icons/icon-192x192.png',
    vibrate: [100, 50, 100],
    data: {
      dateOfArrival: Date.now(),
      primaryKey: '2'
    },
    actions: [
      {
        action: 'explore',
        title: 'Track Order',
        icon: '/static/images/icons/track-icon.png'
      },
      {
        action: 'close',
        title: 'Close',
        icon: '/static/images/icons/close-icon.png'
      }
    ]
  };

  event.waitUntil(
    self.registration.showNotification('GreenObasket Organic Groceries', options)
  );
});

// Handle notification clicks
self.addEventListener('notificationclick', (event) => {
  event.notification.close();

  if (event.action === 'explore') {
    // Open the app to track order
    event.waitUntil(
      clients.openWindow('/shop')
    );
  }
});