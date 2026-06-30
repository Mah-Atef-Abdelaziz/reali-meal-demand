'use client';

import React, { useEffect, useState } from 'react';
import { 
  BarChart, Bar, LineChart, Line, PieChart, Pie, Cell,
  XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, Legend
} from 'recharts';
import { 
  Activity, 
  Trash2, 
  DollarSign, 
  CheckCircle2, 
  ArrowUpRight, 
  ArrowDownRight,
  MapPin,
  Clock
} from 'lucide-react';
import { api } from '../lib/api';

export default function DashboardView() {
  const [summary, setSummary] = useState<any>(null);
  const [locations, setLocations] = useState<any[]>([]);
  const [periods, setPeriods] = useState<any[]>([]);
  const [waste, setWaste] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function loadData() {
      const sumData = await api.dashboard.getSummary();
      const locData = await api.dashboard.getLocationCapacity();
      const perData = await api.dashboard.getPeriodShares();
      const wstData = await api.dashboard.getWeeklyWaste();
      
      setSummary(sumData);
      setLocations(locData);
      setPeriods(perData);
      setWaste(wstData);
      setLoading(false);
    }
    loadData();
  }, []);

  if (loading) {
    return (
      <div className="flex-1 flex items-center justify-center bg-charcoal-950 min-h-screen">
        <div className="flex flex-col items-center gap-3">
          <div className="h-10 w-10 border-4 border-gold-500 border-t-transparent rounded-full animate-spin" />
          <p className="text-charcoal-400 text-sm font-medium animate-pulse">Loading dashboard telemetry...</p>
        </div>
      </div>
    );
  }

  const statCards = [
    {
      title: 'Total Forecasts',
      value: summary?.total_predictions.toLocaleString(),
      change: '+12.4%',
      trend: 'up',
      icon: Activity,
      desc: 'Predictions generated this month'
    },
    {
      title: 'Waste Reduction',
      value: `${summary?.waste_reduction_percent}%`,
      change: '-4.8%',
      trend: 'down',
      icon: Trash2,
      desc: 'Average reduction in food waste'
    },
    {
      title: 'Cost Savings',
      value: `${summary?.saved_cost_egp.toLocaleString()} EGP`,
      change: '+18.2%',
      trend: 'up',
      icon: DollarSign,
      desc: 'Estimated operational savings'
    },
    {
      title: 'Model Accuracy',
      value: `${summary?.actual_vs_predicted_accuracy}%`,
      change: '+0.5%',
      trend: 'up',
      icon: CheckCircle2,
      desc: 'Actual vs predicted meal match'
    }
  ];

  return (
    <div className="p-8 space-y-8 bg-charcoal-950 min-h-screen flex-1 overflow-y-auto">
      {/* Header */}
      <div className="flex justify-between items-center border-b border-charcoal-800 pb-6">
        <div>
          <h2 className="text-2xl font-bold text-white tracking-wide">Operational Overview</h2>
          <p className="text-charcoal-400 text-xs mt-1">Real-time analytical insights and optimization metrics.</p>
        </div>
        <div className="text-right">
          <span className="text-[10px] text-charcoal-400 font-bold uppercase tracking-widest block">Active Model</span>
          <span className="text-xs bg-gold-500/10 border border-gold-500/30 text-gold-400 px-3 py-1 rounded-full font-semibold mt-1 inline-block">
            XGBoost-Regressor v1.0.0
          </span>
        </div>
      </div>

      {/* Stats Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        {statCards.map((card, idx) => {
          const Icon = card.icon;
          return (
            <div key={idx} className="glass-panel p-6 rounded-2xl flex flex-col justify-between hover:border-gold-500/30 transition-all duration-300 group">
              <div className="flex justify-between items-start">
                <div>
                  <span className="text-[11px] text-charcoal-400 font-semibold uppercase tracking-wider block">{card.title}</span>
                  <span className="text-2xl font-extrabold text-white mt-1.5 block tracking-tight group-hover:text-gold-400 transition-colors duration-200">{card.value}</span>
                </div>
                <div className="p-2.5 rounded-xl bg-charcoal-800/80 border border-charcoal-700/50">
                  <Icon className="h-5 w-5 text-gold-500" />
                </div>
              </div>
              <div className="flex items-center gap-2 mt-4 text-xs">
                <span className={`flex items-center font-bold ${card.trend === 'up' ? 'text-emerald-400' : 'text-rose-400'}`}>
                  {card.trend === 'up' ? <ArrowUpRight className="h-3.5 w-3.5" /> : <ArrowDownRight className="h-3.5 w-3.5" />}
                  {card.change}
                </span>
                <span className="text-charcoal-400 font-medium truncate">{card.desc}</span>
              </div>
            </div>
          );
        })}
      </div>

      {/* Charts Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        {/* Weekly Prepared vs Wasted */}
        <div className="glass-panel p-6 rounded-2xl lg:col-span-2 space-y-4">
          <div className="flex justify-between items-center">
            <div>
              <h3 className="text-base font-bold text-white">Daily Prepared vs Wasted Meals</h3>
              <p className="text-charcoal-400 text-xs mt-0.5">Historical meal preparation and waste metrics across active facilities.</p>
            </div>
            <div className="flex gap-4 text-xs font-semibold">
              <span className="flex items-center gap-1.5 text-gold-400">
                <span className="h-2 w-2 rounded-full bg-gold-500" />
                Prepared
              </span>
              <span className="flex items-center gap-1.5 text-charcoal-400">
                <span className="h-2 w-2 rounded-full bg-charcoal-600" />
                Wasted
              </span>
            </div>
          </div>
          <div className="h-80 w-full">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={waste} margin={{ top: 10, right: 10, left: -20, bottom: 0 }}>
                <CartesianGrid strokeDasharray="3 3" stroke="#2d2e35" vertical={false} />
                <XAxis dataKey="date" stroke="#838590" fontSize={11} tickLine={false} />
                <YAxis stroke="#838590" fontSize={11} tickLine={false} />
                <Tooltip 
                  contentStyle={{ backgroundColor: '#1b1c20', borderColor: 'rgba(197, 148, 36, 0.2)', color: '#fff' }}
                  cursor={{ fill: 'rgba(255, 255, 255, 0.03)' }}
                />
                <Bar dataKey="prepared" fill="#c59424" radius={[4, 4, 0, 0]} barSize={28} />
                <Bar dataKey="wasted" fill="#4e505b" radius={[4, 4, 0, 0]} barSize={28} />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>

        {/* Period Distribution */}
        <div className="glass-panel p-6 rounded-2xl flex flex-col justify-between">
          <div>
            <h3 className="text-base font-bold text-white">Meal Period Demand Share</h3>
            <p className="text-charcoal-400 text-xs mt-0.5">Breakfast, Lunch, and Dinner distribution metrics.</p>
          </div>
          <div className="h-60 w-full relative flex items-center justify-center my-4">
            <ResponsiveContainer width="100%" height="100%">
              <PieChart>
                <Pie
                  data={periods}
                  cx="50%"
                  cy="50%"
                  innerRadius={65}
                  outerRadius={90}
                  paddingAngle={5}
                  dataKey="count"
                >
                  {periods.map((entry, index) => (
                    <Cell key={`cell-${index}`} fill={entry.color || '#c59424'} />
                  ))}
                </Pie>
                <Tooltip contentStyle={{ backgroundColor: '#1b1c20', borderColor: 'rgba(197, 148, 36, 0.2)', color: '#fff' }} />
              </PieChart>
            </ResponsiveContainer>
            <div className="absolute flex flex-col items-center justify-center">
              <Clock className="h-6 w-6 text-gold-500/80 mb-1" />
              <span className="text-[10px] text-charcoal-400 uppercase font-bold tracking-wider">Total Volume</span>
              <span className="text-base font-extrabold text-white">
                {periods.reduce((acc, curr) => acc + curr.count, 0).toLocaleString()}
              </span>
            </div>
          </div>
          <div className="space-y-2 mt-2">
            {periods.map((item, idx) => (
              <div key={idx} className="flex items-center justify-between text-xs px-2 py-1.5 rounded-lg bg-charcoal-800/10 border border-charcoal-800/40">
                <div className="flex items-center gap-2">
                  <span className="h-2 w-2 rounded-full" style={{ backgroundColor: item.color }} />
                  <span className="text-charcoal-200 font-semibold">{item.period}</span>
                </div>
                <span className="text-white font-bold">{item.count.toLocaleString()}</span>
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* Facilities Demand Table */}
      <div className="glass-panel p-6 rounded-2xl space-y-4">
        <div>
          <h3 className="text-base font-bold text-white">Active Location Demand Capacity</h3>
          <p className="text-charcoal-400 text-xs mt-0.5">Comparing forecast daily demand against facility food preparation capacity.</p>
        </div>
        <div className="overflow-x-auto">
          <table className="w-full text-left text-xs border-collapse">
            <thead>
              <tr className="border-b border-charcoal-800 text-charcoal-400 uppercase font-bold tracking-wider">
                <th className="py-3 px-4">Location Code</th>
                <th className="py-3 px-4">Facility Capacity</th>
                <th className="py-3 px-4">Forecasted Demand</th>
                <th className="py-3 px-4">Utilisation Rate</th>
                <th className="py-3 px-4">Status</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-charcoal-800/60">
              {locations.map((loc, idx) => {
                const utilization = Math.round((loc.demand / loc.capacity) * 100);
                return (
                  <tr key={idx} className="hover:bg-charcoal-800/10 transition-colors">
                    <td className="py-3.5 px-4 font-bold text-white flex items-center gap-2">
                      <MapPin className="h-3.5 w-3.5 text-gold-500" />
                      {loc.location}
                    </td>
                    <td className="py-3.5 px-4 text-charcoal-300 font-medium">{loc.capacity.toLocaleString()}</td>
                    <td className="py-3.5 px-4 text-charcoal-300 font-medium">{loc.demand.toLocaleString()}</td>
                    <td className="py-3.5 px-4">
                      <div className="flex items-center gap-3">
                        <div className="w-24 bg-charcoal-800 h-2 rounded-full overflow-hidden">
                          <div 
                            className="bg-gold-500 h-full rounded-full" 
                            style={{ width: `${utilization}%` }} 
                          />
                        </div>
                        <span className="font-bold text-charcoal-200">{utilization}%</span>
                      </div>
                    </td>
                    <td className="py-3.5 px-4">
                      <span className={`px-2 py-0.5 rounded-md font-semibold text-[10px] ${
                        utilization > 85 
                          ? 'bg-rose-500/10 border border-rose-500/30 text-rose-400' 
                          : 'bg-emerald-500/10 border border-emerald-500/30 text-emerald-400'
                      }`}>
                        {utilization > 85 ? 'HIGH DEMAND' : 'OPTIMAL'}
                      </span>
                    </td>
                  </tr>
                );
              })}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}
