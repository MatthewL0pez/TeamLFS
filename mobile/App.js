import React from 'react';
import { NavigationContainer } from '@react-navigation/native';
import { createBottomTabNavigator } from '@react-navigation/bottom-tabs';
import { createNativeStackNavigator } from '@react-navigation/native-stack';
import { Ionicons } from '@expo/vector-icons';
import { StatusBar } from 'expo-status-bar';

import { AppProvider } from './src/context/AppContext';
import HomeScreen from './src/screens/HomeScreen';
import BusinessScreen from './src/screens/BusinessScreen';
import UserScreen from './src/screens/UserScreen';
import PackageScreen from './src/screens/PackageScreen';
import RegisterPackageScreen from './src/screens/RegisterPackageScreen';
import LogisticsScreen from './src/screens/LogisticsScreen';

const Tab = createBottomTabNavigator();
const BusinessStack = createNativeStackNavigator();
const PackageStack = createNativeStackNavigator();

function BusinessStackNav() {
  return (
    <BusinessStack.Navigator screenOptions={{ headerShown: false }}>
      <BusinessStack.Screen name="BusinessList" component={BusinessScreen} />
    </BusinessStack.Navigator>
  );   
}

function PackageStackNav() {
  return (
    <PackageStack.Navigator screenOptions={{ headerShown: false }}>
      <PackageStack.Screen name="PackageList" component={PackageScreen} />
      <PackageStack.Screen name="RegisterPackage" component={RegisterPackageScreen} />
    </PackageStack.Navigator>
  );
}

const THEME = {
  primary: '#1e3a5f',
  tabActive: '#2563eb',
  tabInactive: '#94a3b8',
  tabBar: '#ffffff',
};

export default function App() {
  return (
    <AppProvider>
      <NavigationContainer>
        <StatusBar style="light" />
        <Tab.Navigator
          screenOptions={({ route }) => ({
            headerShown: false,
            tabBarStyle: {
              backgroundColor: THEME.tabBar,
              borderTopColor: '#e2e8f0',
              paddingBottom: 6,
              paddingTop: 4,
              height: 62,
            },
            tabBarActiveTintColor: THEME.tabActive,
            tabBarInactiveTintColor: THEME.tabInactive,
            tabBarLabelStyle: { fontSize: 11, fontWeight: '600' },
            tabBarIcon: ({ focused, color, size }) => {
              const icons = {
                Home: focused ? 'home' : 'home-outline',
                Business: focused ? 'business' : 'business-outline',
                Users: focused ? 'people' : 'people-outline',
                Packages: focused ? 'cube' : 'cube-outline',
                Logistics: focused ? 'map' : 'map-outline',
              };
              return <Ionicons name={icons[route.name]} size={22} color={color} />;
            },
          })}
        >
          <Tab.Screen name="Home" component={HomeScreen} />
          <Tab.Screen name="Business" component={BusinessStackNav} />
          <Tab.Screen name="Users" component={UserScreen} />
          <Tab.Screen name="Packages" component={PackageStackNav} />
          <Tab.Screen name="Logistics" component={LogisticsScreen} />
        </Tab.Navigator>
      </NavigationContainer>
    </AppProvider>
  );
}
