'use client';

import React, { useState } from 'react';
import { 
  MenuSquare, 
  Plus, 
  MapPin, 
  Calendar, 
  Users, 
  FileText,
  Egg,
  Coffee,
  CheckCircle
} from 'lucide-react';

const INITIAL_VISITORS = [
  { id: 1, date: '2026-06-30', location: 'HQ-CAI', count: 45, company: 'EGPC', purpose: 'Q2 Audit', meals: 'Lunch' },
  { id: 2, date: '2026-07-02', location: 'IND-AST', count: 120, company: 'Orascom', purpose: 'Safety Seminar', meals: 'Breakfast, Lunch' },
];

const SAMPLE_MENU_ITEMS = [
  { name: 'Grilled Chicken', category: 'Chicken', temp: 'Hot', period: 'Lunch', cost: 15.00, calories: 420 },
  { name: 'Chicken Biryani', category: 'Chicken', temp: 'Hot', period: 'Lunch', cost: 12.00, calories: 650 },
  { name: 'Beef Kebab', category: 'Beef', temp: 'Hot', period: 'Lunch', cost: 18.00, calories: 510 },
  { name: 'Ful Medames', category: 'Vegetarian', temp: 'Hot', period: 'Breakfast', cost: 6.00, calories: 280 },
  { name: 'Shakshuka', category: 'Egg', temp: 'Hot', period: 'Breakfast', cost: 8.00, calories: 310 },
  { name: 'Salad Bowl', category: 'Vegetarian', temp: 'Cold', period: 'Lunch', cost: 7.00, calories: 150 },
  { name: 'Mixed Grill', category: 'Beef', temp: 'Hot', period: 'Dinner', cost: 25.00, calories: 720 },
];

export default function MenusView() {
  const [visitors, setVisitors] = useState(INITIAL_VISITORS);
  const [selectedLocation, setSelectedLocation] = useState('HQ-CAI');
  const [selectedDate, setSelectedDate] = useState('2026-06-30');
  
  // Visitor Form State
  const [vCount, setVCount] = useState(10);
  const [vCompany, setVCompany] = useState('');
  const [vPurpose, setVPurpose] = useState('');
  const [vPeriod, setVPeriod] = useState('Lunch');

  const handleAddVisitor = (e: React.FormEvent) => {
    e.preventDefault();
    if (!vCompany) return;

    const newVisitor = {
      id: Date.now(),
      date: selectedDate,
      location: selectedLocation,
      count: Number(vCount),
      company: vCompany,
      purpose: vPurpose || 'Internal Visit',
      meals: vPeriod
    };

    setVisitors([newVisitor, ...visitors]);
    setVCompany('');
    setVPurpose('');
  };

  return (
    <div className="p-8 space-y-8 bg-charcoal-950 min-h-screen flex-1 overflow-y-auto">
      {/* Header */}
      <div className="flex justify-between items-center border-b border-charcoal-800 pb-6">
        <div>
          <h2 className="text-2xl font-bold text-white tracking-wide">Menu & Visitor Planning</h2>
          <p className="text-charcoal-400 text-xs mt-1">Configure daily kitchen menus and log expected external visitors to adjust raw material metrics.</p>
        </div>
      </div>

      {/* Main Grid split */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        {/* Menu Items Catalog */}
        <div className="lg:col-span-2 space-y-6">
          <div className="glass-panel p-6 rounded-2xl space-y-4">
            <div className="flex justify-between items-center border-b border-charcoal-800 pb-4">
              <div>
                <h3 className="text-sm font-bold text-white uppercase tracking-wider">Scheduled Daily Menu</h3>
                <p className="text-charcoal-400 text-[11px] mt-0.5">Active kitchen preparation items for Cairo HQ.</p>
              </div>
              <div className="flex gap-3">
                <select className="bg-charcoal-900 border border-charcoal-800 rounded-lg px-3 py-1.5 text-[11px] text-white focus:outline-none focus:border-gold-500 font-semibold">
                  <option value="HQ-CAI">HQ-CAI</option>
                  <option value="IND-AST">IND-AST</option>
                </select>
                <input 
                  type="date" 
                  value={selectedDate}
                  onChange={(e) => setSelectedDate(e.target.value)}
                  className="bg-charcoal-900 border border-charcoal-800 rounded-lg px-3 py-1.5 text-[11px] text-white focus:outline-none focus:border-gold-500 font-semibold"
                />
              </div>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              {SAMPLE_MENU_ITEMS.map((item, idx) => (
                <div key={idx} className="p-4 rounded-xl bg-charcoal-900 border border-charcoal-800/80 hover:border-gold-500/20 transition-all duration-200 flex justify-between items-center">
                  <div className="flex gap-3 items-center">
                    <div className="h-8 w-8 rounded-lg bg-charcoal-800 flex items-center justify-center font-bold text-xs text-gold-500">
                      {item.period === 'Breakfast' ? <Egg className="h-4 w-4" /> : <Coffee className="h-4 w-4" />}
                    </div>
                    <div>
                      <h4 className="text-xs font-bold text-white">{item.name}</h4>
                      <p className="text-[10px] text-charcoal-400 font-medium mt-0.5">{item.category} • {item.calories} kcal</p>
                    </div>
                  </div>
                  <div className="text-right">
                    <span className="text-xs font-bold text-gold-500">{item.cost.toFixed(2)} EGP</span>
                    <span className="text-[9px] text-charcoal-400 block mt-0.5 uppercase tracking-wider font-bold">{item.period}</span>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>

        {/* Visitor Logs / Form */}
        <div className="space-y-8">
          {/* Add Visitor Form */}
          <div className="glass-panel p-6 rounded-2xl space-y-4">
            <h3 className="text-sm font-bold text-white uppercase tracking-wider">Log External Visitors</h3>
            <form onSubmit={handleAddVisitor} className="space-y-4">
              <div className="space-y-1.5">
                <label className="text-[10px] text-charcoal-400 font-bold uppercase tracking-wider block">Visiting Organization</label>
                <input 
                  type="text" 
                  value={vCompany}
                  onChange={(e) => setVCompany(e.target.value)}
                  placeholder="e.g. Orascom Construction"
                  className="w-full bg-charcoal-900 border border-charcoal-800 rounded-xl px-4 py-3 text-xs text-white placeholder-charcoal-500 focus:outline-none focus:border-gold-500 font-semibold"
                />
              </div>

              <div className="grid grid-cols-2 gap-4">
                <div className="space-y-1.5">
                  <label className="text-[10px] text-charcoal-400 font-bold uppercase tracking-wider block">Visitor Count</label>
                  <input 
                    type="number" 
                    value={vCount}
                    onChange={(e) => setVCount(Number(e.target.value))}
                    min={1}
                    className="w-full bg-charcoal-900 border border-charcoal-800 rounded-xl px-4 py-3 text-xs text-white focus:outline-none focus:border-gold-500 font-semibold"
                  />
                </div>
                <div className="space-y-1.5">
                  <label className="text-[10px] text-charcoal-400 font-bold uppercase tracking-wider block">Meal Period</label>
                  <select 
                    value={vPeriod}
                    onChange={(e) => setVPeriod(e.target.value)}
                    className="w-full bg-charcoal-900 border border-charcoal-800 rounded-xl px-4 py-3 text-xs text-white focus:outline-none focus:border-gold-500 font-semibold"
                  >
                    <option value="Breakfast">Breakfast</option>
                    <option value="Lunch">Lunch</option>
                    <option value="Dinner">Dinner</option>
                    <option value="All Periods">All Periods</option>
                  </select>
                </div>
              </div>

              <div className="space-y-1.5">
                <label className="text-[10px] text-charcoal-400 font-bold uppercase tracking-wider block">Purpose of Visit</label>
                <input 
                  type="text" 
                  value={vPurpose}
                  onChange={(e) => setVPurpose(e.target.value)}
                  placeholder="e.g. Technical Audit"
                  className="w-full bg-charcoal-900 border border-charcoal-800 rounded-xl px-4 py-3 text-xs text-white placeholder-charcoal-500 focus:outline-none focus:border-gold-500 font-semibold"
                />
              </div>

              <button 
                type="submit"
                className="w-full bg-gradient-to-r from-gold-500 to-gold-600 hover:from-gold-600 hover:to-gold-700 text-charcoal-950 font-bold text-xs py-3 rounded-xl transition-all shadow-md shadow-gold-500/10 flex items-center justify-center gap-2 uppercase tracking-wider cursor-pointer"
              >
                <Plus className="h-4 w-4" />
                Add Visitor Log
              </button>
            </form>
          </div>

          {/* Active Visitors List */}
          <div className="glass-panel p-6 rounded-2xl space-y-4">
            <h3 className="text-sm font-bold text-white uppercase tracking-wider flex items-center gap-2">
              <Users className="h-4.5 w-4.5 text-gold-500" />
              Registered Visitors
            </h3>
            <div className="space-y-3.5">
              {visitors.map((visitor) => (
                <div key={visitor.id} className="p-3.5 rounded-xl bg-charcoal-900 border border-charcoal-800/80 flex justify-between items-start">
                  <div>
                    <h4 className="text-xs font-bold text-white">{visitor.company}</h4>
                    <p className="text-[10px] text-charcoal-400 mt-1">{visitor.purpose} • {visitor.location}</p>
                    <span className="text-[9px] bg-gold-500/10 text-gold-400 px-2 py-0.5 rounded border border-gold-500/20 inline-block mt-2 font-semibold">
                      {visitor.meals}
                    </span>
                  </div>
                  <div className="text-right">
                    <span className="text-sm font-extrabold text-white block">+{visitor.count}</span>
                    <span className="text-[9px] text-charcoal-400 font-medium block mt-0.5">{visitor.date}</span>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
