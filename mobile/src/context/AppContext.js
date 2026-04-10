import React, { createContext, useContext, useState } from 'react';
import { BUSINESSES, USERS, PACKAGES } from '../data/mockData';

const AppContext = createContext(null);

export function AppProvider({ children }) {
  const [businesses] = useState(BUSINESSES);
  const [users, setUsers] = useState(USERS);
  const [packages, setPackages] = useState(PACKAGES);
  const [activeBusinessId, setActiveBusinessId] = useState(null);
  const [activeUserId, setActiveUserId] = useState(null);

  const activeBusiness = businesses.find((b) => b.id === activeBusinessId) ?? null;
  const activeUser = users.find((u) => u.id === activeUserId) ?? null;

  function selectBusiness(id) {
    setActiveBusinessId(id);
    setActiveUserId(null); // reset user when business changes
  }

  function logoutBusiness() {
    setActiveBusinessId(null);
    setActiveUserId(null);
  }

  function selectUser(id) {
    setActiveUserId(id);
  }

  function clearUser() {
    setActiveUserId(null);
  }

  function addUser(userData) {
    const newId = Math.max(...users.map((u) => u.id)) + 1;
    const newUser = { id: newId, ...userData };
    setUsers((prev) => [...prev, newUser]);
    return newUser;
  }

  function addPackage(pkgData) {
    const newId = `PKG-${String(packages.length + 1).padStart(3, '0')}`;
    const newPkg = { id: newId, status: 'Processing', ...pkgData };
    setPackages((prev) => [...prev, newPkg]);
    return newPkg;
  }

  return (
    <AppContext.Provider
      value={{
        businesses,
        users,
        packages,
        activeBusiness,
        activeUser,
        selectBusiness,
        logoutBusiness,
        selectUser,
        clearUser,
        addUser,
        addPackage,
      }}
    >
      {children}
    </AppContext.Provider>
  );
}

export function useApp() {
  return useContext(AppContext);
}
