import React from 'react';
import {
  View, Text, StyleSheet, ScrollView, TouchableOpacity, SafeAreaView,
} from 'react-native';
import { Ionicons } from '@expo/vector-icons';
import { useApp } from '../context/AppContext';

const NAV_CARDS = [
  { label: 'Business',  subtitle: 'Manage hubs & locations', icon: 'business',  color: '#1e3a5f', tab: 'Business' },
  { label: 'Users',     subtitle: 'Warehouse staff & agents', icon: 'people',    color: '#0f5132', tab: 'Users'    },
  { label: 'Packages',  subtitle: 'Track & register shipments',icon: 'cube',     color: '#5b21b6', tab: 'Packages' },
  { label: 'Logistics', subtitle: 'Routes & closest hubs',    icon: 'map',       color: '#92400e', tab: 'Logistics'},
];

export default function HomeScreen({ navigation }) {
  const { activeBusiness, activeUser } = useApp();

  return (
    <SafeAreaView style={s.safe}>
      <ScrollView contentContainerStyle={s.scroll} showsVerticalScrollIndicator={false}>
        {/* Header */}
        <View style={s.header}>
          <Text style={s.title}>LFS Tracker</Text>
          <Text style={s.subtitle}>Business Packaging Program — Team LFS</Text>
        </View>

        {/* Status Bar */}
        <View style={s.statusCard}>
          <StatusRow
            icon="business-outline"
            label="Active Business"
            value={activeBusiness ? `${activeBusiness.name}` : 'None selected'}
            color={activeBusiness ? '#16a34a' : '#94a3b8'}
          />
          <View style={s.divider} />
          <StatusRow
            icon="person-outline"
            label="Active User"
            value={activeUser ? `${activeUser.firstName} ${activeUser.lastName}` : 'None selected'}
            color={activeUser ? '#2563eb' : '#94a3b8'}
          />
        </View>

        {/* Nav Grid */}
        <Text style={s.sectionLabel}>NAVIGATION</Text>
        <View style={s.grid}>
          {NAV_CARDS.map((card) => (
            <TouchableOpacity
              key={card.label}
              style={[s.card, { borderLeftColor: card.color }]}
              onPress={() => navigation.navigate(card.tab)}
              activeOpacity={0.75}
            >
              <View style={[s.iconBox, { backgroundColor: card.color }]}>
                <Ionicons name={card.icon} size={22} color="#fff" />
              </View>
              <View style={s.cardText}>
                <Text style={s.cardTitle}>{card.label}</Text>
                <Text style={s.cardSub}>{card.subtitle}</Text>
              </View>
              <Ionicons name="chevron-forward" size={18} color="#cbd5e1" />
            </TouchableOpacity>
          ))}
        </View>

        {/* Footer */}
        <Text style={s.footer}>CPSC 362 — Team LFS</Text>
      </ScrollView>
    </SafeAreaView>
  );
}

function StatusRow({ icon, label, value, color }) {
  return (
    <View style={s.statusRow}>
      <Ionicons name={icon} size={16} color={color} style={{ marginRight: 8 }} />
      <Text style={s.statusLabel}>{label}: </Text>
      <Text style={[s.statusValue, { color }]}>{value}</Text>
    </View>
  );
}

const s = StyleSheet.create({
  safe:         { flex: 1, backgroundColor: '#f1f5f9' },
  scroll:       { padding: 20, paddingBottom: 40 },
  header:       { alignItems: 'center', paddingVertical: 28, marginBottom: 4 },
  title:        { fontSize: 30, fontWeight: '800', color: '#1e3a5f', letterSpacing: 0.5 },
  subtitle:     { fontSize: 13, color: '#64748b', marginTop: 4 },
  statusCard:   { backgroundColor: '#fff', borderRadius: 14, padding: 16, marginBottom: 24, shadowColor: '#000', shadowOpacity: 0.06, shadowRadius: 8, elevation: 3 },
  statusRow:    { flexDirection: 'row', alignItems: 'center', paddingVertical: 4 },
  statusLabel:  { fontSize: 13, color: '#64748b' },
  statusValue:  { fontSize: 13, fontWeight: '700', flexShrink: 1 },
  divider:      { height: 1, backgroundColor: '#f1f5f9', marginVertical: 8 },
  sectionLabel: { fontSize: 11, fontWeight: '700', color: '#94a3b8', letterSpacing: 1.2, marginBottom: 10 },
  grid:         { gap: 10 },
  card:         { backgroundColor: '#fff', borderRadius: 14, padding: 16, flexDirection: 'row', alignItems: 'center', borderLeftWidth: 4, shadowColor: '#000', shadowOpacity: 0.05, shadowRadius: 6, elevation: 2 },
  iconBox:      { width: 42, height: 42, borderRadius: 10, justifyContent: 'center', alignItems: 'center', marginRight: 14 },
  cardText:     { flex: 1 },
  cardTitle:    { fontSize: 15, fontWeight: '700', color: '#0f172a' },
  cardSub:      { fontSize: 12, color: '#64748b', marginTop: 2 },
  footer:       { textAlign: 'center', color: '#cbd5e1', fontSize: 11, marginTop: 32 },
});
