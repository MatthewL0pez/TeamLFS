import React, { useState } from 'react';
import {
  View, Text, StyleSheet, ScrollView, TouchableOpacity,
  SafeAreaView, TextInput, Alert,
} from 'react-native';
import { Ionicons } from '@expo/vector-icons';
import { useApp } from '../context/AppContext';
import { CITIES } from '../data/mockData';
import { haversine, calculateShippingCost } from '../utils/distance';
import { BUSINESSES } from '../data/mockData';

export default function RegisterPackageScreen({ navigation }) {
  const { activeBusiness, activeUser, addPackage } = useApp();

  const [destination, setDestination] = useState(null);
  const [description, setDescription] = useState('');
  const [weight, setWeight] = useState('');
  const [quote, setQuote] = useState(null);

  const sourceCity = activeBusiness?.city ?? '';

  // Cities exclude source
  const destinations = CITIES.filter((c) => c !== sourceCity);

  function getCityCoords(cityName) {
    // look up from BUSINESSES first, then fall back to locations
    const biz = BUSINESSES.find(
      (b) => b.city === cityName || b.name.includes(cityName)
    );
    if (biz) return { lat: biz.lat, lon: biz.lon };
    return null;
  }

  function handleCalculate() {
    if (!destination) { Alert.alert('Missing', 'Select a destination city.'); return; }
    if (!description.trim()) { Alert.alert('Missing', 'Enter a description.'); return; }
    const w = parseFloat(weight);
    if (isNaN(w) || w <= 0) { Alert.alert('Invalid', 'Enter a valid weight (e.g. 2.5).'); return; }

    const srcCoords = { lat: activeBusiness.lat, lon: activeBusiness.lon };
    const destBiz = BUSINESSES.find((b) => b.city === destination);
    if (!destBiz) { Alert.alert('Error', 'Could not find coordinates for that city.'); return; }

    const dist = haversine(srcCoords.lat, srcCoords.lon, destBiz.lat, destBiz.lon);
    const cost = calculateShippingCost(dist, w);
    setQuote({ dist, cost });
  }

  function handleConfirm() {
    const w = parseFloat(weight);
    const pkg = addPackage({
      businessId: activeBusiness.id,
      userId: activeUser.id,
      sourceCity,
      destinationCity: destination,
      weight: w,
      description: description.trim(),
      shippingCost: quote.cost,
    });
    Alert.alert(
      'Package Registered!',
      `Tracking ID: ${pkg.id}\nCost: $${quote.cost.toFixed(2)}`,
      [{ text: 'OK', onPress: () => navigation.goBack() }]
    );
  }

  return (
    <SafeAreaView style={s.safe}>
      {/* Top nav */}
      <View style={s.topNav}>
        <TouchableOpacity onPress={() => navigation.goBack()} style={s.backBtn}>
          <Ionicons name="arrow-back" size={20} color="#1e3a5f" />
          <Text style={s.backText}>Back</Text>
        </TouchableOpacity>
        <Text style={s.navTitle}>Register Package</Text>
        <View style={{ width: 70 }} />
      </View>

      <ScrollView contentContainerStyle={s.scroll} keyboardShouldPersistTaps="handled">
        {/* Context */}
        <View style={s.contextCard}>
          <Row icon="business-outline" label="Business" value={activeBusiness?.name} />
          <Row icon="person-outline"   label="User"     value={`${activeUser?.firstName} ${activeUser?.lastName}`} />
          <Row icon="location-outline" label="Origin"   value={sourceCity} />
        </View>

        {/* Step 1: Destination */}
        <Text style={s.stepLabel}>1. SELECT DESTINATION</Text>
        <ScrollView horizontal showsHorizontalScrollIndicator={false} style={s.cityScroll}>
          {destinations.map((city) => (
            <TouchableOpacity
              key={city}
              style={[s.cityChip, destination === city && s.cityChipActive]}
              onPress={() => { setDestination(city); setQuote(null); }}
            >
              <Text style={[s.cityChipText, destination === city && s.cityChipTextActive]}>{city}</Text>
            </TouchableOpacity>
          ))}
        </ScrollView>

        {/* Step 2: Details */}
        <Text style={s.stepLabel}>2. PACKAGE DETAILS</Text>
        <View style={s.fieldGroup}>
          <Text style={s.fieldLabel}>Description</Text>
          <TextInput
            style={s.input}
            placeholder="e.g. Electronics, Documents..."
            placeholderTextColor="#94a3b8"
            value={description}
            onChangeText={(v) => { setDescription(v); setQuote(null); }}
          />
        </View>
        <View style={s.fieldGroup}>
          <Text style={s.fieldLabel}>Weight (kg)</Text>
          <TextInput
            style={s.input}
            placeholder="e.g. 2.5"
            placeholderTextColor="#94a3b8"
            keyboardType="decimal-pad"
            value={weight}
            onChangeText={(v) => { setWeight(v); setQuote(null); }}
          />
        </View>

        {/* Step 3: Quote */}
        <Text style={s.stepLabel}>3. GET QUOTE</Text>
        <TouchableOpacity style={s.calcBtn} onPress={handleCalculate}>
          <Ionicons name="calculator-outline" size={16} color="#fff" />
          <Text style={s.calcBtnText}>Calculate Shipping Cost</Text>
        </TouchableOpacity>

        {quote && (
          <View style={s.quoteCard}>
            <Text style={s.quoteTitle}>Logistics Quote</Text>
            <QuoteLine label="Route"    value={`${sourceCity} → ${destination}`} />
            <QuoteLine label="Distance" value={`${quote.dist.toFixed(2)} km`} />
            <QuoteLine label="Weight"   value={`${parseFloat(weight).toFixed(2)} kg`} />
            <View style={s.quoteDivider} />
            <View style={s.quoteCostRow}>
              <Text style={s.quoteCostLabel}>Total Cost</Text>
              <Text style={s.quoteCostValue}>${quote.cost.toFixed(2)}</Text>
            </View>

            <TouchableOpacity style={s.confirmBtn} onPress={handleConfirm}>
              <Ionicons name="checkmark-circle-outline" size={18} color="#fff" />
              <Text style={s.confirmBtnText}>Confirm & Register</Text>
            </TouchableOpacity>
          </View>
        )}
      </ScrollView>
    </SafeAreaView>
  );
}

function Row({ icon, label, value }) {
  return (
    <View style={s.ctxRow}>
      <Ionicons name={icon} size={14} color="#64748b" />
      <Text style={s.ctxLabel}>{label}: </Text>
      <Text style={s.ctxValue}>{value}</Text>
    </View>
  );
}

function QuoteLine({ label, value }) {
  return (
    <View style={s.quoteLine}>
      <Text style={s.quoteLineLabel}>{label}</Text>
      <Text style={s.quoteLineValue}>{value}</Text>
    </View>
  );
}

const s = StyleSheet.create({
  safe:              { flex: 1, backgroundColor: '#f1f5f9' },
  topNav:            { flexDirection: 'row', alignItems: 'center', justifyContent: 'space-between', backgroundColor: '#fff', paddingHorizontal: 16, paddingVertical: 12, borderBottomWidth: 1, borderBottomColor: '#e2e8f0' },
  backBtn:           { flexDirection: 'row', alignItems: 'center', gap: 4 },
  backText:          { fontSize: 14, color: '#1e3a5f', fontWeight: '600' },
  navTitle:          { fontSize: 16, fontWeight: '800', color: '#0f172a' },
  scroll:            { padding: 16, paddingBottom: 60 },
  contextCard:       { backgroundColor: '#fff', borderRadius: 12, padding: 14, marginBottom: 20, gap: 6 },
  ctxRow:            { flexDirection: 'row', alignItems: 'center', gap: 6 },
  ctxLabel:          { fontSize: 13, color: '#64748b' },
  ctxValue:          { fontSize: 13, color: '#0f172a', fontWeight: '700' },
  stepLabel:         { fontSize: 11, fontWeight: '700', color: '#94a3b8', letterSpacing: 1, marginBottom: 10 },
  cityScroll:        { marginBottom: 20 },
  cityChip:          { borderWidth: 1.5, borderColor: '#e2e8f0', borderRadius: 20, paddingHorizontal: 14, paddingVertical: 7, marginRight: 8, backgroundColor: '#fff' },
  cityChipActive:    { backgroundColor: '#1e3a5f', borderColor: '#1e3a5f' },
  cityChipText:      { fontSize: 13, color: '#475569', fontWeight: '600' },
  cityChipTextActive:{ color: '#fff' },
  fieldGroup:        { marginBottom: 14 },
  fieldLabel:        { fontSize: 12, fontWeight: '700', color: '#475569', marginBottom: 5, textTransform: 'uppercase', letterSpacing: 0.5 },
  input:             { backgroundColor: '#fff', borderRadius: 10, borderWidth: 1, borderColor: '#e2e8f0', paddingHorizontal: 14, paddingVertical: 11, fontSize: 14, color: '#0f172a' },
  calcBtn:           { flexDirection: 'row', alignItems: 'center', gap: 8, justifyContent: 'center', backgroundColor: '#2563eb', borderRadius: 12, padding: 13, marginBottom: 16 },
  calcBtnText:       { color: '#fff', fontWeight: '800', fontSize: 14 },
  quoteCard:         { backgroundColor: '#fff', borderRadius: 14, padding: 18, shadowColor: '#000', shadowOpacity: 0.06, shadowRadius: 8, elevation: 3 },
  quoteTitle:        { fontSize: 16, fontWeight: '800', color: '#1e3a5f', marginBottom: 12 },
  quoteLine:         { flexDirection: 'row', justifyContent: 'space-between', paddingVertical: 5 },
  quoteLineLabel:    { fontSize: 13, color: '#64748b' },
  quoteLineValue:    { fontSize: 13, color: '#0f172a', fontWeight: '600' },
  quoteDivider:      { height: 1, backgroundColor: '#f1f5f9', marginVertical: 10 },
  quoteCostRow:      { flexDirection: 'row', justifyContent: 'space-between', alignItems: 'center', marginBottom: 16 },
  quoteCostLabel:    { fontSize: 15, fontWeight: '700', color: '#0f172a' },
  quoteCostValue:    { fontSize: 22, fontWeight: '900', color: '#1e3a5f' },
  confirmBtn:        { flexDirection: 'row', alignItems: 'center', justifyContent: 'center', gap: 8, backgroundColor: '#16a34a', borderRadius: 12, padding: 13 },
  confirmBtnText:    { color: '#fff', fontWeight: '800', fontSize: 15 },
});
