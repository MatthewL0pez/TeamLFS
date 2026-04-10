import React, { useState } from 'react';
import {
  View, Text, StyleSheet, ScrollView, TouchableOpacity,
  SafeAreaView,
} from 'react-native';
import { Ionicons } from '@expo/vector-icons';
import { useApp } from '../context/AppContext';
import { getRouteOrder, getRouteDistance, getClosestBusiness, haversine } from '../utils/distance';

export default function LogisticsScreen() {
  const { businesses } = useApp();

  const [closestFrom, setClosestFrom] = useState(null);
  const [closestResult, setClosestResult] = useState(null);

  const [routeFrom, setRouteFrom] = useState(null);
  const [routeResult, setRouteResult] = useState(null);

  function handleFindClosest(biz) {
    setClosestFrom(biz);
    const result = getClosestBusiness(businesses, biz.id);
    setClosestResult(result);
  }

  function handleShowRoute(biz) {
    setRouteFrom(biz);
    const route = getRouteOrder(businesses, biz.id);
    const totalDist = getRouteDistance(route);
    setRouteResult({ route, totalDist });
  }

  return (
    <SafeAreaView style={s.safe}>
      <ScrollView contentContainerStyle={s.scroll} showsVerticalScrollIndicator={false}>
        <Text style={s.title}>Logistics Tools</Text>
        <Text style={s.subtitle}>Haversine-based routing across all 10 hubs</Text>

        {/* ── Section 1: Find Closest ── */}
        <View style={s.section}>
          <View style={s.sectionHeader}>
            <Ionicons name="locate-outline" size={18} color="#1e3a5f" />
            <Text style={s.sectionTitle}>Find Closest Hub</Text>
          </View>
          <Text style={s.sectionHint}>Tap a hub to find its nearest neighbor</Text>

          <View style={s.hubGrid}>
            {businesses.map((biz) => (
              <TouchableOpacity
                key={biz.id}
                style={[s.hubChip, closestFrom?.id === biz.id && s.hubChipActive]}
                onPress={() => handleFindClosest(biz)}
              >
                <Text style={[s.hubChipText, closestFrom?.id === biz.id && s.hubChipTextActive]}>
                  {biz.city}
                </Text>
              </TouchableOpacity>
            ))}
          </View>

          {closestResult && closestFrom && (
            <View style={s.resultCard}>
              <View style={s.resultTop}>
                <View style={s.resultPin}>
                  <Ionicons name="location" size={18} color="#1e3a5f" />
                </View>
                <Text style={s.resultText}>
                  Closest to <Text style={s.resultBold}>{closestFrom.name}</Text>
                </Text>
              </View>
              <View style={s.resultArrow}>
                <Text style={s.resultCity}>{closestResult.business.name}</Text>
                <Text style={s.resultCity}>{closestResult.business.city}, {closestResult.business.country}</Text>
                <View style={s.distBadge}>
                  <Ionicons name="navigate-outline" size={13} color="#1e40af" />
                  <Text style={s.distText}>{closestResult.distance.toFixed(2)} km</Text>
                </View>
              </View>
            </View>
          )}
        </View>

        {/* ── Section 2: Optimal Route ── */}
        <View style={s.section}>
          <View style={s.sectionHeader}>
            <Ionicons name="git-merge-outline" size={18} color="#5b21b6" />
            <Text style={[s.sectionTitle, { color: '#5b21b6' }]}>Optimal Route</Text>
          </View>
          <Text style={s.sectionHint}>Nearest-neighbor algorithm starting from any hub</Text>

          <View style={s.hubGrid}>
            {businesses.map((biz) => (
              <TouchableOpacity
                key={biz.id}
                style={[s.hubChip, s.hubChipPurple, routeFrom?.id === biz.id && s.hubChipPurpleActive]}
                onPress={() => handleShowRoute(biz)}
              >
                <Text style={[s.hubChipText, routeFrom?.id === biz.id && s.hubChipTextActive]}>
                  {biz.city}
                </Text>
              </TouchableOpacity>
            ))}
          </View>

          {routeResult && routeFrom && (
            <View style={s.routeCard}>
              <View style={s.routeHeader}>
                <Text style={s.routeCardTitle}>Optimal Route from {routeFrom.city}</Text>
                <View style={s.totalDistBadge}>
                  <Text style={s.totalDistText}>{routeResult.totalDist.toFixed(2)} km total</Text>
                </View>
              </View>
              {routeResult.route.map((biz, idx) => (
                <View key={biz.id} style={s.routeStop}>
                  <View style={s.stopLine}>
                    <View style={[s.stopDot, idx === 0 && s.stopDotStart, idx === routeResult.route.length - 1 && s.stopDotEnd]} />
                    {idx < routeResult.route.length - 1 && <View style={s.stopConnector} />}
                  </View>
                  <View style={s.stopInfo}>
                    <Text style={s.stopNum}>{idx + 1}</Text>
                    <View>
                      <Text style={[s.stopName, idx === 0 && { color: '#1e3a5f', fontWeight: '900' }]}>{biz.name}</Text>
                      <Text style={s.stopCity}>{biz.city}, {biz.country}</Text>
                    </View>
                    {idx > 0 && (
                      <Text style={s.legDist}>
                        +{haversine(
                          routeResult.route[idx - 1].lat, routeResult.route[idx - 1].lon,
                          biz.lat, biz.lon
                        ).toFixed(0)} km
                      </Text>
                    )}
                  </View>
                </View>
              ))}
            </View>
          )}
        </View>
      </ScrollView>
    </SafeAreaView>
  );
}

const s = StyleSheet.create({
  safe:               { flex: 1, backgroundColor: '#f1f5f9' },
  scroll:             { padding: 16, paddingBottom: 48 },
  title:              { fontSize: 22, fontWeight: '800', color: '#1e3a5f' },
  subtitle:           { fontSize: 12, color: '#94a3b8', marginTop: 2, marginBottom: 20 },
  section:            { backgroundColor: '#fff', borderRadius: 16, padding: 16, marginBottom: 16, shadowColor: '#000', shadowOpacity: 0.04, shadowRadius: 6, elevation: 2 },
  sectionHeader:      { flexDirection: 'row', alignItems: 'center', gap: 8, marginBottom: 4 },
  sectionTitle:       { fontSize: 16, fontWeight: '800', color: '#1e3a5f' },
  sectionHint:        { fontSize: 12, color: '#94a3b8', marginBottom: 12 },
  hubGrid:            { flexDirection: 'row', flexWrap: 'wrap', gap: 8, marginBottom: 12 },
  hubChip:            { borderWidth: 1.5, borderColor: '#bfdbfe', borderRadius: 20, paddingHorizontal: 12, paddingVertical: 6, backgroundColor: '#eff6ff' },
  hubChipActive:      { backgroundColor: '#1e3a5f', borderColor: '#1e3a5f' },
  hubChipPurple:      { borderColor: '#ddd6fe', backgroundColor: '#f5f3ff' },
  hubChipPurpleActive:{ backgroundColor: '#5b21b6', borderColor: '#5b21b6' },
  hubChipText:        { fontSize: 12, color: '#1e40af', fontWeight: '600' },
  hubChipTextActive:  { color: '#fff' },
  resultCard:         { backgroundColor: '#f0f9ff', borderRadius: 12, padding: 14, borderWidth: 1, borderColor: '#bae6fd' },
  resultTop:          { flexDirection: 'row', alignItems: 'center', gap: 8, marginBottom: 8 },
  resultPin:          { width: 30, height: 30, borderRadius: 15, backgroundColor: '#dbeafe', justifyContent: 'center', alignItems: 'center' },
  resultText:         { fontSize: 13, color: '#64748b' },
  resultBold:         { fontWeight: '800', color: '#1e3a5f' },
  resultArrow:        { paddingLeft: 8, gap: 2 },
  resultCity:         { fontSize: 15, fontWeight: '700', color: '#0f172a' },
  distBadge:          { flexDirection: 'row', alignItems: 'center', gap: 4, marginTop: 4, backgroundColor: '#dbeafe', alignSelf: 'flex-start', paddingHorizontal: 10, paddingVertical: 4, borderRadius: 20 },
  distText:           { fontSize: 12, color: '#1e40af', fontWeight: '700' },
  routeCard:          { backgroundColor: '#faf5ff', borderRadius: 12, padding: 14, borderWidth: 1, borderColor: '#ddd6fe' },
  routeHeader:        { flexDirection: 'row', justifyContent: 'space-between', alignItems: 'center', marginBottom: 12 },
  routeCardTitle:     { fontSize: 13, fontWeight: '700', color: '#5b21b6', flex: 1 },
  totalDistBadge:     { backgroundColor: '#5b21b6', borderRadius: 20, paddingHorizontal: 10, paddingVertical: 4 },
  totalDistText:      { color: '#fff', fontSize: 11, fontWeight: '700' },
  routeStop:          { flexDirection: 'row', marginBottom: 2 },
  stopLine:           { width: 24, alignItems: 'center', paddingTop: 4 },
  stopDot:            { width: 10, height: 10, borderRadius: 5, backgroundColor: '#a78bfa' },
  stopDotStart:       { backgroundColor: '#5b21b6', width: 12, height: 12, borderRadius: 6 },
  stopDotEnd:         { backgroundColor: '#dc2626' },
  stopConnector:      { width: 2, flex: 1, backgroundColor: '#ddd6fe', marginVertical: 2 },
  stopInfo:           { flex: 1, flexDirection: 'row', alignItems: 'center', gap: 8, paddingVertical: 6, paddingLeft: 4 },
  stopNum:            { fontSize: 11, fontWeight: '800', color: '#94a3b8', width: 18 },
  stopName:           { fontSize: 13, fontWeight: '700', color: '#0f172a' },
  stopCity:           { fontSize: 11, color: '#94a3b8' },
  legDist:            { marginLeft: 'auto', fontSize: 11, color: '#7c3aed', fontWeight: '600' },
});
