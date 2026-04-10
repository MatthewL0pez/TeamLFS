// Mock data mirroring the Python backend structures
// Replace with real API calls when backend integration is ready

export const BUSINESSES = [
  { id: 1,  name: 'Los Angeles Hub', city: 'Los Angeles',  country: 'USA',     lat: 34.0565,  lon: -118.2488, employees: [1, 2], sections: { Receiving: ['PKG-001', 'PKG-003'], Shipping: ['PKG-002'] }, totalPackages: 3 },
  { id: 2,  name: 'New York Hub',    city: 'New York City', country: 'USA',    lat: 40.7089,  lon: -74.0100,  employees: [3],    sections: { Sorting: ['PKG-004'] },                                   totalPackages: 1 },
  { id: 3,  name: 'Toronto Hub',     city: 'Toronto',       country: 'Canada', lat: 43.6506,  lon: -79.3858,  employees: [],     sections: {},                                                        totalPackages: 0 },
  { id: 4,  name: 'London Hub',      city: 'London',        country: 'UK',     lat: 51.5081,  lon: -0.1259,   employees: [4],    sections: { Inbound: [] },                                            totalPackages: 0 },
  { id: 5,  name: 'Paris Hub',       city: 'Paris',         country: 'France', lat: 48.8606,  lon:  2.3431,   employees: [],     sections: {},                                                        totalPackages: 0 },
  { id: 6,  name: 'Berlin Hub',      city: 'Berlin',        country: 'Germany',lat: 52.5160,  lon: 13.3967,   employees: [],     sections: {},                                                        totalPackages: 0 },
  { id: 7,  name: 'Rome Hub',        city: 'Rome',          country: 'Italy',  lat: 41.8878,  lon: 12.4842,   employees: [],     sections: {},                                                        totalPackages: 0 },
  { id: 8,  name: 'Dubai Hub',       city: 'Dubai',         country: 'UAE',    lat: 25.1924,  lon: 55.2778,   employees: [5],    sections: { Transit: ['PKG-005'] },                                  totalPackages: 1 },
  { id: 9,  name: 'Tokyo Hub',       city: 'Tokyo',         country: 'Japan',  lat: 35.6776,  lon: 139.7667,  employees: [6],    sections: {},                                                        totalPackages: 0 },
  { id: 10, name: 'Sydney Hub',      city: 'Sydney',        country: 'Australia', lat: -33.8622, lon: 151.2093, employees: [], sections: {},                                                         totalPackages: 0 },
];

export const USERS = [
  { id: 1, businessId: 1, firstName: 'Matt',    lastName: 'Lopez',    email: 'matt@lahub.com',    phone: '213-555-0101', billingInfo: 'VISA-4242', role: 'Warehouse Lead',  status: 'Active'   },
  { id: 2, businessId: 1, firstName: 'Sara',    lastName: 'Chen',     email: 'sara@lahub.com',    phone: '213-555-0102', billingInfo: 'VISA-8888', role: 'Shipping Agent',  status: 'Active'   },
  { id: 3, businessId: 2, firstName: 'James',   lastName: 'Parker',   email: 'james@nyhub.com',   phone: '212-555-0201', billingInfo: 'MC-1234',   role: 'Manager',         status: 'Active'   },
  { id: 4, businessId: 4, firstName: 'Olivia',  lastName: 'Smith',    email: 'olivia@lonhub.com', phone: '020-555-0401', billingInfo: 'VISA-3333', role: 'Logistics Lead',  status: 'Active'   },
  { id: 5, businessId: 8, firstName: 'Khalid',  lastName: 'Al-Farsi', email: 'khalid@dubaihub.ae',phone: '04-555-0801',  billingInfo: 'AMEX-9999', role: 'Operations Lead', status: 'Active'   },
  { id: 6, businessId: 9, firstName: 'Yuki',    lastName: 'Tanaka',   email: 'yuki@tokyohub.jp',  phone: '03-555-0901',  billingInfo: 'VISA-7777', role: 'Warehouse Agent', status: 'Active'   },
];

export const PACKAGES = [
  { id: 'PKG-001', businessId: 1, userId: 1, sourceCity: 'Los Angeles', destinationCity: 'Tokyo',        weight: 2.5,  description: 'Electronics',       shippingCost: 91.22,  status: 'Processing' },
  { id: 'PKG-002', businessId: 1, userId: 2, sourceCity: 'Los Angeles', destinationCity: 'London',       weight: 1.2,  description: 'Apparel',           shippingCost: 93.90,  status: 'Shipped'    },
  { id: 'PKG-003', businessId: 1, userId: 1, sourceCity: 'Los Angeles', destinationCity: 'Dubai',        weight: 3.0,  description: 'Auto Parts',        shippingCost: 142.34, status: 'Processing' },
  { id: 'PKG-004', businessId: 2, userId: 3, sourceCity: 'New York City','destinationCity': 'Paris',      weight: 0.8,  description: 'Documents',         shippingCost: 60.10,  status: 'In Transit' },
  { id: 'PKG-005', businessId: 8, userId: 5, sourceCity: 'Dubai',        destinationCity: 'Sydney',       weight: 5.0,  description: 'Industrial Goods',  shippingCost: 124.62, status: 'Processing' },
];

export const CITIES = [
  'Los Angeles', 'New York City', 'Toronto', 'London',
  'Paris', 'Berlin', 'Rome', 'Dubai', 'Tokyo', 'Sydney',
];
