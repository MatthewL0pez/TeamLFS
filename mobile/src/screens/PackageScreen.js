import React from 'react';
import {
  View, Text, StyleSheet, ScrollView, TouchableOpacity, SafeAreaView,
} from 'react-native';
import { Ionicons } from '@expo/vector-icons';
import { useApp } from '../context/AppContext';

const STATUS_COLORS = {
  Processing: { bg: '#fef9c3', text: '#854d0e', icon: 'hourglass-outline' },
  Shipped:    { bg: '#dbeafe', text: '#1e40af', icon: 'airplane-outline'  },
  'In Transit':{ bg: '#f0fdf4', text: '#166534', icon: 'navigate-outline' },
  Delivered:  { bg: '#dcfce7', text: '#15803d', icon: 'checkmark-circle-outline' },
};

export default function PackageScreen({ navigation }) {
  const { activeBusiness, activeUser, packages } = useApp();

  const bizPkgs = activeBusiness
    ? packages.filter((p) => p.businessId === activeBusiness.id)
    : [];

  const userPkgs = activeUser
    ? packages.filter((p) => p.userId === activeUser.id)
    : [];

  const canRegister = activeBusiness && activeUser;

  return (
    <SafeAreaView style={s.safe}>
      <ScrollView contentContainerStyle={s.scroll} showsVerticalScrollIndicator={false}>
        {/* Header */}
        <View style={s.header}>
          <Text style={s.title}>Package Management</Text>
          <View style={s.statusRow}>
            <Pill label={activeBusiness ? activeBusiness.name : 'No business'} active={!!activeBusiness} icon="business-outline" />
            <Pill label={activeUser ? `${activeUser.firstName} ${activeUser.lastName}` : 'No user'} active={!!activeUser} icon="person-outline" />
          </View>
        </View>

        {/* Register button */}
        {canRegister ? (
          <TouchableOpacity style={s.registerBtn} onPress={() => navigation.navigate('RegisterPackage')}>
            <Ionicons name="add-circle-outline" size={18} color="#fff" />
            <Text style={s.registerBtnText}>Register New Package</Text>
          </TouchableOpacity>
        ) : (
          <View style={s.warningBox}>
            <Ionicons name="warning-outline" size={16} color="#92400e" />
            <Text style={s.warningText}>Select both a Business and a User to register packages.</Text>
          </View>
        )}

        {/* My Packages */}
        {activeUser && (
          <>
            <Text style={s.sectionLabel}>MY PACKAGES  ({userPkgs.length})</Text>
            {userPkgs.length === 0 ? (
              <Text style={s.empty}>No packages for this user.</Text>
            ) : (
              userPkgs.map((p) => <PackageCard key={p.id} pkg={p} />)
            )}
          </>
        )}

        {/* Business Packages */}
        {activeBusiness && (
          <>
            <Text style={s.sectionLabel}>ALL BUSINESS PACKAGES  ({bizPkgs.length})</Text>
            {bizPkgs.length === 0 ? (
              <Text style={s.empty}>No packages for this business.</Text>
            ) : (
              bizPkgs.map((p) => <PackageCard key={p.id} pkg={p} highlight={activeUser?.id === p.userId} />)
            )}
          </>
        )}

        {!activeBusiness && (
          <View style={s.emptyFull}>
            <Ionicons name="cube-outline" size={52} color="#cbd5e1" />
            <Text style={s.emptyText}>Select a business to view packages</Text>
          </View>
        )}
      </ScrollView>
    </SafeAreaView>
  );
}

function PackageCard({ pkg, highlight }) {
  const status = STATUS_COLORS[pkg.status] ?? STATUS_COLORS.Processing;
  return (
    <View style={[s.card, highlight && s.cardHighlight]}>
      <View style={s.cardTop}>
        <Text style={s.pkgId}>{pkg.id}</Text>
        <View style={[s.statusPill, { backgroundColor: status.bg }]}>
          <Ionicons name={status.icon} size={11} color={status.text} />
          <Text style={[s.statusText, { color: status.text }]}>{pkg.status}</Text>
        </View>
      </View>
      <Text style={s.description}>{pkg.description}</Text>
      <View style={s.routeRow}>
        <Ionicons name="location-outline" size={13} color="#64748b" />
        <Text style={s.routeText}>{pkg.sourceCity}</Text>
        <Ionicons name="arrow-forward" size={13} color="#94a3b8" />
        <Text style={s.routeText}>{pkg.destinationCity}</Text>
      </View>
      <View style={s.metaRow}>
        <MetaChip icon="scale-outline"  value={`${pkg.weight} kg`} />
        <MetaChip icon="card-outline"   value={`$${pkg.shippingCost.toFixed(2)}`} highlight />
      </View>
    </View>
  );
}

function MetaChip({ icon, value, highlight }) {
  return (
    <View style={[mc.chip, highlight && mc.chipHighlight]}>
      <Ionicons name={icon} size={12} color={highlight ? '#1e40af' : '#64748b'} />
      <Text style={[mc.text, highlight && mc.textHighlight]}>{value}</Text>
    </View>
  );
}

function Pill({ label, active, icon }) {
  return (
    <View style={[pl.pill, active && pl.active]}>
      <Ionicons name={icon} size={11} color={active ? '#fff' : '#94a3b8'} />
      <Text style={[pl.text, active && pl.textActive]}>{label}</Text>
    </View>
  );
}

const pl = StyleSheet.create({
  pill:       { flexDirection: 'row', alignItems: 'center', gap: 4, backgroundColor: '#f1f5f9', borderRadius: 20, paddingHorizontal: 10, paddingVertical: 5 },
  active:     { backgroundColor: '#1e3a5f' },
  text:       { fontSize: 11, color: '#94a3b8' },
  textActive: { color: '#fff', fontWeight: '600' },
});

const mc = StyleSheet.create({
  chip:          { flexDirection: 'row', alignItems: 'center', gap: 4, backgroundColor: '#f8fafc', borderRadius: 6, paddingHorizontal: 8, paddingVertical: 4 },
  chipHighlight: { backgroundColor: '#dbeafe' },
  text:          { fontSize: 12, color: '#64748b', fontWeight: '600' },
  textHighlight: { color: '#1e40af', fontWeight: '700' },
});

const s = StyleSheet.create({
  safe:          { flex: 1, backgroundColor: '#f1f5f9' },
  scroll:        { padding: 16, paddingBottom: 40 },
  header:        { marginBottom: 14 },
  title:         { fontSize: 22, fontWeight: '800', color: '#1e3a5f', marginBottom: 8 },
  statusRow:     { flexDirection: 'row', gap: 8, flexWrap: 'wrap' },
  registerBtn:   { flexDirection: 'row', alignItems: 'center', gap: 8, backgroundColor: '#5b21b6', borderRadius: 12, padding: 13, justifyContent: 'center', marginBottom: 16 },
  registerBtnText:{ color: '#fff', fontWeight: '800', fontSize: 14 },
  warningBox:    { flexDirection: 'row', alignItems: 'center', gap: 8, backgroundColor: '#fef3c7', borderRadius: 10, padding: 12, marginBottom: 16 },
  warningText:   { fontSize: 12, color: '#92400e', flex: 1 },
  sectionLabel:  { fontSize: 11, fontWeight: '700', color: '#94a3b8', letterSpacing: 1, marginBottom: 8, marginTop: 6 },
  empty:         { fontSize: 13, color: '#94a3b8', fontStyle: 'italic', marginBottom: 12 },
  emptyFull:     { alignItems: 'center', paddingTop: 60 },
  emptyText:     { fontSize: 15, color: '#94a3b8', marginTop: 12 },
  card:          { backgroundColor: '#fff', borderRadius: 12, padding: 14, marginBottom: 8, shadowColor: '#000', shadowOpacity: 0.04, shadowRadius: 5, elevation: 2 },
  cardHighlight: { borderLeftWidth: 3, borderLeftColor: '#2563eb' },
  cardTop:       { flexDirection: 'row', justifyContent: 'space-between', alignItems: 'center', marginBottom: 4 },
  pkgId:         { fontSize: 13, fontWeight: '700', color: '#475569', fontFamily: 'monospace' },
  statusPill:    { flexDirection: 'row', alignItems: 'center', gap: 3, paddingHorizontal: 8, paddingVertical: 3, borderRadius: 20 },
  statusText:    { fontSize: 11, fontWeight: '700' },
  description:   { fontSize: 15, fontWeight: '700', color: '#0f172a', marginBottom: 6 },
  routeRow:      { flexDirection: 'row', alignItems: 'center', gap: 5, marginBottom: 8 },
  routeText:     { fontSize: 12, color: '#475569', fontWeight: '600' },
  metaRow:       { flexDirection: 'row', gap: 8 },
});
