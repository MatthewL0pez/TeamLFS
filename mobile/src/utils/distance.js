// Haversine distance formula — mirrors services/distance_service.py
const EARTH_RADIUS_KM = 6371;

function toRad(deg) {
  return (deg * Math.PI) / 180;
}

export function haversine(lat1, lon1, lat2, lon2) {
  const dLat = toRad(lat2 - lat1);
  const dLon = toRad(lon2 - lon1);
  const a =
    Math.sin(dLat / 2) ** 2 +
    Math.cos(toRad(lat1)) * Math.cos(toRad(lat2)) * Math.sin(dLon / 2) ** 2;
  const c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1 - a));
  return EARTH_RADIUS_KM * c;
}

// Mirrors PricingService.calculate_shipping_cost()
const BASE_FEE = 2.5;
const RATE_PER_KM = 0.01;
const RATE_PER_KG = 0.25;

export function calculateShippingCost(distanceKm, weightKg) {
  return Math.round((BASE_FEE + distanceKm * RATE_PER_KM + weightKg * RATE_PER_KG) * 100) / 100;
}

// Nearest-neighbor route order — mirrors get_route_order() in business_storage.py
export function getRouteOrder(businesses, startId) {
  const all = [...businesses];
  const visited = new Set([startId]);
  const route = [all.find((b) => b.id === startId)];

  while (visited.size < all.length) {
    const current = route[route.length - 1];
    let closest = null;
    let minDist = Infinity;

    for (const b of all) {
      if (visited.has(b.id)) continue;
      const d = haversine(current.lat, current.lon, b.lat, b.lon);
      if (d < minDist) {
        minDist = d;
        closest = b;
      }
    }
    if (!closest) break;
    route.push(closest);
    visited.add(closest.id);
  }
  return route;
}

export function getRouteDistance(route) {
  let total = 0;
  for (let i = 0; i < route.length - 1; i++) {
    total += haversine(route[i].lat, route[i].lon, route[i + 1].lat, route[i + 1].lon);
  }
  return total;
}

export function getClosestBusiness(businesses, fromId) {
  const base = businesses.find((b) => b.id === fromId);
  if (!base) return null;
  let closest = null;
  let minDist = Infinity;
  for (const b of businesses) {
    if (b.id === fromId) continue;
    const d = haversine(base.lat, base.lon, b.lat, b.lon);
    if (d < minDist) {
      minDist = d;
      closest = b;
    }
  }
  return { business: closest, distance: minDist };
}
