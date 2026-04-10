import React, { useState } from 'react';
import {
  View, Text, StyleSheet, ScrollView, TouchableOpacity,
  SafeAreaView, Modal, TextInput, Alert,
} from 'react-native';
import { Ionicons } from '@expo/vector-icons';
import { useApp } from '../context/AppContext';

export default function BusinessScreen() {
  const { businesses, activeBusiness, selectBusiness, logoutBusiness } = useApp();
  const [manageTarget, setManageTarget] = useState(null); // business being managed
  const [newSection, setNewSection] = useState('');

  function handleSelect(biz) {
    selectBusiness(biz.id);
    Alert.alert('Business Selected', `${biz.name} is now active.`);
  }

  function handleLogout() {
    Alert.alert('Logout Business', 'Deselect the active business?', [
      { text: 'Cancel', style: 'cancel' },
      { text: 'Logout', style: 'destructive', onPress: logoutBusiness },
    ]);
  }

  function handleAddSection() {
    const name = newSection.trim();
    if (!name) return;
    if (manageTarget.sections[name] !== undefined) {
      Alert.alert('Already exists', `Section "${name}" already exists.`);
      return;
    }
    manageTarget.sections[name] = [];
    setNewSection('');
    setManageTarget({ ...manageTarget });
  }

  return (
    <SafeAreaView style={s.safe}>
      <ScrollView contentContainerStyle={s.scroll} showsVerticalScrollIndicator={false}>
        {/* Header */}
        <View style={s.header}>
          <Text style={s.title}>Business Management</Text>
          {activeBusiness ? (
            <View style={s.activeBadge}>
              <Ionicons name="checkmark-circle" size={14} color="#16a34a" />
              <Text style={s.activeBadgeText}>{activeBusiness.name}</Text>
              <TouchableOpacity onPress={handleLogout} style={s.logoutBtn}>
                <Text style={s.logoutText}>Logout</Text>
              </TouchableOpacity>
            </View>
          ) : (
            <Text style={s.hint}>Tap a hub to select it as active</Text>
          )}
        </View>

        {/* Business List */}
        {businesses.map((biz) => {
          const isActive = activeBusiness?.id === biz.id;
          return (
            <View key={biz.id} style={[s.card, isActive && s.cardActive]}>
              <View style={s.cardTop}>
                <View style={s.cardLeft}>
                  <View style={[s.idBadge, isActive && s.idBadgeActive]}>
                    <Text style={[s.idText, isActive && { color: '#fff' }]}>#{biz.id}</Text>
                  </View>
                  <View>
                    <Text style={s.bizName}>{biz.name}</Text>
                    <Text style={s.bizCity}>
                      <Ionicons name="location-outline" size={12} color="#64748b" /> {biz.city}, {biz.country}
                    </Text>
                  </View>
                </View>
                {isActive && <Ionicons name="checkmark-circle" size={20} color="#16a34a" />}
              </View>

              {/* Stats row */}
              <View style={s.statsRow}>
                <Stat icon="people-outline"  value={biz.employees.length}           label="Employees" />
                <Stat icon="layers-outline"  value={Object.keys(biz.sections).length} label="Sections" />
                <Stat icon="cube-outline"    value={biz.totalPackages}               label="Packages" />
              </View>

              {/* Actions */}
              <View style={s.actionsRow}>
                {!isActive && (
                  <TouchableOpacity style={[s.btn, s.btnPrimary]} onPress={() => handleSelect(biz)}>
                    <Ionicons name="log-in-outline" size={14} color="#fff" />
                    <Text style={s.btnPrimaryText}>Select</Text>
                  </TouchableOpacity>
                )}
                <TouchableOpacity style={[s.btn, s.btnSecondary]} onPress={() => setManageTarget(biz)}>
                  <Ionicons name="settings-outline" size={14} color="#1e3a5f" />
                  <Text style={s.btnSecondaryText}>Manage</Text>
                </TouchableOpacity>
              </View>
            </View>
          );
        })}
      </ScrollView>

      {/* Manage Modal */}
      <Modal visible={!!manageTarget} animationType="slide" presentationStyle="pageSheet">
        {manageTarget && (
          <SafeAreaView style={s.modal}>
            <View style={s.modalHeader}>
              <View>
                <Text style={s.modalTitle}>{manageTarget.name}</Text>
                <Text style={s.modalSubtitle}>{manageTarget.city}</Text>
              </View>
              <TouchableOpacity onPress={() => setManageTarget(null)}>
                <Ionicons name="close-circle" size={28} color="#64748b" />
              </TouchableOpacity>
            </View>

            <ScrollView style={s.modalScroll}>
              {/* Sections */}
              <Text style={s.sectionLabel}>SECTIONS</Text>
              {Object.keys(manageTarget.sections).length === 0 ? (
                <Text style={s.empty}>No sections yet.</Text>
              ) : (
                Object.entries(manageTarget.sections).map(([sec, pkgs]) => (
                  <View key={sec} style={s.sectionRow}>
                    <Ionicons name="layers-outline" size={16} color="#5b21b6" />
                    <Text style={s.sectionName}>{sec}</Text>
                    <Text style={s.sectionCount}>{pkgs.length} pkg{pkgs.length !== 1 ? 's' : ''}</Text>
                  </View>
                ))
              )}

              {/* Add Section */}
              <Text style={s.sectionLabel}>ADD SECTION</Text>
              <View style={s.inputRow}>
                <TextInput
                  style={s.input}
                  placeholder="Section name (e.g. Receiving)"
                  value={newSection}
                  onChangeText={setNewSection}
                  placeholderTextColor="#94a3b8"
                />
                <TouchableOpacity style={s.addBtn} onPress={handleAddSection}>
                  <Ionicons name="add" size={20} color="#fff" />
                </TouchableOpacity>
              </View>

              {/* Employees */}
              <Text style={s.sectionLabel}>EMPLOYEES</Text>
              {manageTarget.employees.length === 0 ? (
                <Text style={s.empty}>No employees assigned.</Text>
              ) : (
                manageTarget.employees.map((eid) => (
                  <View key={eid} style={s.sectionRow}>
                    <Ionicons name="person-outline" size={16} color="#0f5132" />
                    <Text style={s.sectionName}>User ID: {eid}</Text>
                  </View>
                ))
              )}
            </ScrollView>
          </SafeAreaView>
        )}
      </Modal>
    </SafeAreaView>
  );
}

function Stat({ icon, value, label }) {
  return (
    <View style={s.stat}>
      <Ionicons name={icon} size={13} color="#64748b" />
      <Text style={s.statValue}>{value}</Text>
      <Text style={s.statLabel}>{label}</Text>
    </View>
  );
}

const s = StyleSheet.create({
  safe:             { flex: 1, backgroundColor: '#f1f5f9' },
  scroll:           { padding: 16, paddingBottom: 40 },
  header:           { marginBottom: 16 },
  title:            { fontSize: 22, fontWeight: '800', color: '#1e3a5f' },
  hint:             { fontSize: 12, color: '#94a3b8', marginTop: 4 },
  activeBadge:      { flexDirection: 'row', alignItems: 'center', gap: 6, marginTop: 4 },
  activeBadgeText:  { fontSize: 12, color: '#16a34a', fontWeight: '600' },
  logoutBtn:        { backgroundColor: '#fee2e2', borderRadius: 6, paddingHorizontal: 8, paddingVertical: 2 },
  logoutText:       { fontSize: 11, color: '#dc2626', fontWeight: '700' },
  card:             { backgroundColor: '#fff', borderRadius: 14, padding: 14, marginBottom: 10, shadowColor: '#000', shadowOpacity: 0.05, shadowRadius: 6, elevation: 2 },
  cardActive:       { borderWidth: 2, borderColor: '#16a34a' },
  cardTop:          { flexDirection: 'row', alignItems: 'center', justifyContent: 'space-between', marginBottom: 10 },
  cardLeft:         { flexDirection: 'row', alignItems: 'center', gap: 10 },
  idBadge:          { width: 34, height: 34, borderRadius: 8, backgroundColor: '#f1f5f9', justifyContent: 'center', alignItems: 'center' },
  idBadgeActive:    { backgroundColor: '#1e3a5f' },
  idText:           { fontSize: 12, fontWeight: '700', color: '#475569' },
  bizName:          { fontSize: 15, fontWeight: '700', color: '#0f172a' },
  bizCity:          { fontSize: 12, color: '#64748b', marginTop: 1 },
  statsRow:         { flexDirection: 'row', gap: 16, marginBottom: 12 },
  stat:             { flexDirection: 'row', alignItems: 'center', gap: 4 },
  statValue:        { fontSize: 13, fontWeight: '700', color: '#0f172a' },
  statLabel:        { fontSize: 11, color: '#94a3b8' },
  actionsRow:       { flexDirection: 'row', gap: 8 },
  btn:              { flexDirection: 'row', alignItems: 'center', gap: 4, paddingHorizontal: 14, paddingVertical: 7, borderRadius: 8 },
  btnPrimary:       { backgroundColor: '#1e3a5f' },
  btnPrimaryText:   { color: '#fff', fontSize: 13, fontWeight: '700' },
  btnSecondary:     { backgroundColor: '#f1f5f9', borderWidth: 1, borderColor: '#e2e8f0' },
  btnSecondaryText: { color: '#1e3a5f', fontSize: 13, fontWeight: '700' },
  // Modal
  modal:            { flex: 1, backgroundColor: '#f1f5f9' },
  modalHeader:      { flexDirection: 'row', justifyContent: 'space-between', alignItems: 'flex-start', padding: 20, backgroundColor: '#fff', borderBottomWidth: 1, borderBottomColor: '#e2e8f0' },
  modalTitle:       { fontSize: 18, fontWeight: '800', color: '#1e3a5f' },
  modalSubtitle:    { fontSize: 13, color: '#64748b' },
  modalScroll:      { padding: 16 },
  sectionLabel:     { fontSize: 11, fontWeight: '700', color: '#94a3b8', letterSpacing: 1, marginTop: 16, marginBottom: 8 },
  sectionRow:       { flexDirection: 'row', alignItems: 'center', gap: 10, backgroundColor: '#fff', padding: 12, borderRadius: 10, marginBottom: 6 },
  sectionName:      { flex: 1, fontSize: 14, color: '#0f172a', fontWeight: '600' },
  sectionCount:     { fontSize: 12, color: '#94a3b8' },
  empty:            { fontSize: 13, color: '#94a3b8', fontStyle: 'italic', marginBottom: 8 },
  inputRow:         { flexDirection: 'row', gap: 8 },
  input:            { flex: 1, backgroundColor: '#fff', borderRadius: 10, borderWidth: 1, borderColor: '#e2e8f0', paddingHorizontal: 14, paddingVertical: 10, fontSize: 14, color: '#0f172a' },
  addBtn:           { backgroundColor: '#1e3a5f', borderRadius: 10, width: 44, justifyContent: 'center', alignItems: 'center' },
});
