import React, { useState } from 'react';
import {
  View, Text, StyleSheet, ScrollView, TouchableOpacity,
  SafeAreaView, Modal, TextInput, Alert,
} from 'react-native';
import { Ionicons } from '@expo/vector-icons';
import { useApp } from '../context/AppContext';

export default function UserScreen() {
  const { users, activeBusiness, activeUser, selectUser, clearUser, addUser } = useApp();
  const [showCreate, setShowCreate] = useState(false);
  const [form, setForm] = useState({ firstName: '', lastName: '', email: '', phone: '', billingInfo: '' });

  const bizUsers = activeBusiness
    ? users.filter((u) => u.businessId === activeBusiness.id)
    : [];

  function handleCreate() {
    const { firstName, lastName, email, phone, billingInfo } = form;
    if (!firstName || !lastName || !email || !phone || !billingInfo) {
      Alert.alert('Missing Fields', 'All fields are required.');
      return;
    }
    const newUser = addUser({ ...form, businessId: activeBusiness.id, role: 'Staff', status: 'Active' });
    Alert.alert('User Created', `${newUser.firstName} ${newUser.lastName} (ID ${newUser.id})`);
    setForm({ firstName: '', lastName: '', email: '', phone: '', billingInfo: '' });
    setShowCreate(false);
  }

  return (
    <SafeAreaView style={s.safe}>
      <ScrollView contentContainerStyle={s.scroll} showsVerticalScrollIndicator={false}>
        {/* Header */}
        <View style={s.header}>
          <Text style={s.title}>User Management</Text>
          <View style={s.statusBanner}>
            <StatusPill
              icon="business-outline"
              label={activeBusiness ? activeBusiness.name : 'No business selected'}
              active={!!activeBusiness}
            />
            <StatusPill
              icon="person-outline"
              label={activeUser ? `${activeUser.firstName} ${activeUser.lastName}` : 'No user selected'}
              active={!!activeUser}
            />
          </View>
        </View>

        {!activeBusiness ? (
          <View style={s.empty}>
            <Ionicons name="business-outline" size={48} color="#cbd5e1" />
            <Text style={s.emptyText}>Select a business first</Text>
            <Text style={s.emptyHint}>Go to the Business tab to select a hub</Text>
          </View>
        ) : (
          <>
            {/* Active user actions */}
            {activeUser && (
              <View style={s.activeUserCard}>
                <View style={s.activeUserLeft}>
                  <Ionicons name="person-circle" size={38} color="#2563eb" />
                  <View>
                    <Text style={s.activeUserName}>{activeUser.firstName} {activeUser.lastName}</Text>
                    <Text style={s.activeUserEmail}>{activeUser.email}</Text>
                  </View>
                </View>
                <TouchableOpacity style={s.clearBtn} onPress={clearUser}>
                  <Text style={s.clearText}>Clear</Text>
                </TouchableOpacity>
              </View>
            )}

            {/* Create button */}
            <TouchableOpacity style={s.createBtn} onPress={() => setShowCreate(true)}>
              <Ionicons name="person-add-outline" size={16} color="#fff" />
              <Text style={s.createBtnText}>Create User for {activeBusiness.name}</Text>
            </TouchableOpacity>

            {/* User list */}
            <Text style={s.sectionLabel}>USERS FOR {activeBusiness.name.toUpperCase()}</Text>

            {bizUsers.length === 0 ? (
              <View style={s.emptyInline}>
                <Text style={s.emptyText}>No users found for this business.</Text>
              </View>
            ) : (
              bizUsers.map((u) => {
                const isActive = activeUser?.id === u.id;
                return (
                  <View key={u.id} style={[s.card, isActive && s.cardActive]}>
                    <View style={s.cardLeft}>
                      <View style={[s.avatar, isActive && s.avatarActive]}>
                        <Text style={[s.avatarText, isActive && { color: '#fff' }]}>
                          {u.firstName[0]}{u.lastName[0]}
                        </Text>
                      </View>
                      <View>
                        <View style={s.nameRow}>
                          <Text style={s.name}>{u.firstName} {u.lastName}</Text>
                          <Text style={s.idTag}>#{u.id}</Text>
                        </View>
                        <Text style={s.email}>{u.email}</Text>
                        <Text style={s.role}>{u.role}  ·  {u.status}</Text>
                      </View>
                    </View>
                    <View style={s.cardActions}>
                      {isActive ? (
                        <View style={s.activePill}>
                          <Ionicons name="checkmark-circle" size={12} color="#16a34a" />
                          <Text style={s.activePillText}>Active</Text>
                        </View>
                      ) : (
                        <TouchableOpacity style={s.selectBtn} onPress={() => selectUser(u.id)}>
                          <Text style={s.selectBtnText}>Select</Text>
                        </TouchableOpacity>
                      )}
                    </View>
                  </View>
                );
              })
            )}
          </>
        )}
      </ScrollView>

      {/* Create User Modal */}
      <Modal visible={showCreate} animationType="slide" presentationStyle="pageSheet">
        <SafeAreaView style={s.modal}>
          <View style={s.modalHeader}>
            <Text style={s.modalTitle}>Create User</Text>
            <TouchableOpacity onPress={() => setShowCreate(false)}>
              <Ionicons name="close-circle" size={28} color="#64748b" />
            </TouchableOpacity>
          </View>
          <ScrollView style={s.modalScroll} keyboardShouldPersistTaps="handled">
            <Text style={s.modalBizLabel}>For: {activeBusiness?.name}</Text>
            {[
              { key: 'firstName',   label: 'First Name',           placeholder: 'e.g. Matt' },
              { key: 'lastName',    label: 'Last Name',            placeholder: 'e.g. Lopez' },
              { key: 'email',       label: 'Email',                placeholder: 'e.g. matt@hub.com' },
              { key: 'phone',       label: 'Phone',                placeholder: 'e.g. 213-555-0101' },
              { key: 'billingInfo', label: 'Billing Info',         placeholder: 'e.g. VISA-4242' },
            ].map(({ key, label, placeholder }) => (
              <View key={key} style={s.fieldGroup}>
                <Text style={s.fieldLabel}>{label}</Text>
                <TextInput
                  style={s.input}
                  placeholder={placeholder}
                  placeholderTextColor="#94a3b8"
                  value={form[key]}
                  onChangeText={(val) => setForm((prev) => ({ ...prev, [key]: val }))}
                  autoCapitalize={key === 'email' ? 'none' : 'words'}
                  keyboardType={key === 'email' ? 'email-address' : key === 'phone' ? 'phone-pad' : 'default'}
                />
              </View>
            ))}
            <TouchableOpacity style={s.submitBtn} onPress={handleCreate}>
              <Ionicons name="person-add" size={16} color="#fff" />
              <Text style={s.submitBtnText}>Create User</Text>
            </TouchableOpacity>
          </ScrollView>
        </SafeAreaView>
      </Modal>
    </SafeAreaView>
  );
}

function StatusPill({ icon, label, active }) {
  return (
    <View style={[sp.pill, active && sp.pillActive]}>
      <Ionicons name={icon} size={12} color={active ? '#fff' : '#94a3b8'} />
      <Text style={[sp.text, active && sp.textActive]}>{label}</Text>
    </View>
  );
}

const sp = StyleSheet.create({
  pill:       { flexDirection: 'row', alignItems: 'center', gap: 4, backgroundColor: '#f1f5f9', borderRadius: 20, paddingHorizontal: 10, paddingVertical: 5 },
  pillActive: { backgroundColor: '#1e3a5f' },
  text:       { fontSize: 12, color: '#94a3b8' },
  textActive: { color: '#fff', fontWeight: '600' },
});

const s = StyleSheet.create({
  safe:            { flex: 1, backgroundColor: '#f1f5f9' },
  scroll:          { padding: 16, paddingBottom: 40 },
  header:          { marginBottom: 16 },
  title:           { fontSize: 22, fontWeight: '800', color: '#1e3a5f', marginBottom: 8 },
  statusBanner:    { flexDirection: 'row', gap: 8, flexWrap: 'wrap' },
  empty:           { alignItems: 'center', paddingTop: 60 },
  emptyInline:     { paddingVertical: 20, alignItems: 'center' },
  emptyText:       { fontSize: 16, color: '#94a3b8', marginTop: 10, fontWeight: '600' },
  emptyHint:       { fontSize: 12, color: '#cbd5e1', marginTop: 4 },
  activeUserCard:  { backgroundColor: '#eff6ff', borderRadius: 12, padding: 14, flexDirection: 'row', alignItems: 'center', justifyContent: 'space-between', marginBottom: 12, borderWidth: 1, borderColor: '#bfdbfe' },
  activeUserLeft:  { flexDirection: 'row', alignItems: 'center', gap: 10 },
  activeUserName:  { fontSize: 15, fontWeight: '700', color: '#1e40af' },
  activeUserEmail: { fontSize: 12, color: '#3b82f6' },
  clearBtn:        { backgroundColor: '#dbeafe', borderRadius: 8, paddingHorizontal: 12, paddingVertical: 5 },
  clearText:       { color: '#2563eb', fontSize: 12, fontWeight: '700' },
  createBtn:       { flexDirection: 'row', alignItems: 'center', gap: 6, backgroundColor: '#0f5132', borderRadius: 10, padding: 12, justifyContent: 'center', marginBottom: 16 },
  createBtnText:   { color: '#fff', fontWeight: '700', fontSize: 14 },
  sectionLabel:    { fontSize: 11, fontWeight: '700', color: '#94a3b8', letterSpacing: 1, marginBottom: 8 },
  card:            { backgroundColor: '#fff', borderRadius: 12, padding: 14, marginBottom: 8, flexDirection: 'row', alignItems: 'center', justifyContent: 'space-between', shadowColor: '#000', shadowOpacity: 0.04, shadowRadius: 4, elevation: 1 },
  cardActive:      { borderWidth: 2, borderColor: '#2563eb' },
  cardLeft:        { flexDirection: 'row', alignItems: 'center', gap: 12, flex: 1 },
  cardActions:     { marginLeft: 8 },
  avatar:          { width: 42, height: 42, borderRadius: 21, backgroundColor: '#f1f5f9', justifyContent: 'center', alignItems: 'center' },
  avatarActive:    { backgroundColor: '#2563eb' },
  avatarText:      { fontSize: 14, fontWeight: '800', color: '#475569' },
  nameRow:         { flexDirection: 'row', alignItems: 'center', gap: 6 },
  name:            { fontSize: 14, fontWeight: '700', color: '#0f172a' },
  idTag:           { fontSize: 11, color: '#94a3b8', backgroundColor: '#f8fafc', paddingHorizontal: 5, paddingVertical: 1, borderRadius: 4 },
  email:           { fontSize: 12, color: '#64748b' },
  role:            { fontSize: 11, color: '#94a3b8', marginTop: 1 },
  activePill:      { flexDirection: 'row', alignItems: 'center', gap: 3, backgroundColor: '#dcfce7', paddingHorizontal: 8, paddingVertical: 4, borderRadius: 20 },
  activePillText:  { fontSize: 11, color: '#16a34a', fontWeight: '700' },
  selectBtn:       { backgroundColor: '#1e3a5f', borderRadius: 8, paddingHorizontal: 12, paddingVertical: 6 },
  selectBtnText:   { color: '#fff', fontSize: 12, fontWeight: '700' },
  // Modal
  modal:           { flex: 1, backgroundColor: '#f1f5f9' },
  modalHeader:     { flexDirection: 'row', justifyContent: 'space-between', alignItems: 'center', padding: 20, backgroundColor: '#fff', borderBottomWidth: 1, borderBottomColor: '#e2e8f0' },
  modalTitle:      { fontSize: 18, fontWeight: '800', color: '#1e3a5f' },
  modalScroll:     { padding: 16 },
  modalBizLabel:   { fontSize: 13, color: '#64748b', marginBottom: 16 },
  fieldGroup:      { marginBottom: 14 },
  fieldLabel:      { fontSize: 12, fontWeight: '700', color: '#475569', marginBottom: 5, textTransform: 'uppercase', letterSpacing: 0.5 },
  input:           { backgroundColor: '#fff', borderRadius: 10, borderWidth: 1, borderColor: '#e2e8f0', paddingHorizontal: 14, paddingVertical: 11, fontSize: 14, color: '#0f172a' },
  submitBtn:       { flexDirection: 'row', alignItems: 'center', justifyContent: 'center', gap: 8, backgroundColor: '#0f5132', borderRadius: 12, padding: 14, marginTop: 8 },
  submitBtnText:   { color: '#fff', fontWeight: '800', fontSize: 15 },
});
