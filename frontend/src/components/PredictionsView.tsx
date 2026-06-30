'use client';

import React, { useState } from 'react';
import { 
  TrendingUp, 
  MapPin, 
  Calendar, 
  Clock, 
  Play, 
  ShieldAlert, 
  Sparkles,
  ArrowUp,
  ArrowDown,
  Info
} from 'lucide-react';
import { api } from '../lib/api';

const LOCATIONS = [
  { id: 1, name: 'Headquarters (HQ-CAI) — Cairo', capacity: 2000 },
  { id: 2, name: 'Alexandria Office (OFF-ALX) — Alexandria', capacity: 800 },
  { id: 5, name: 'Ain Sokhna Industrial (IND-ASK) — Ain Sokhna', capacity: 1500 },
  { id: 6, name: 'Borg El-Arab Plant (IND-BRG) — Borg El-Arab', capacity: 1200 },
  { id: 9, name: 'Ras Gharib Field (FLD-RSG) — Ras Gharib', capacity: 600 },
];

export default function PredictionsView() {
  const [locationId, setLocationId] = useState(1);
  const [dateStr, setDateStr] = useState(new Date(Date.now() + 86400000).toISOString().split('T')[0]); // Default to tomorrow
  const [period, setPeriod] = useState('lunch');
  const [forecast, setForecast] = useState<any>(null);
  const [loading, setLoading] = useState(false);

  const handleGenerate = async () => {
    setLoading(true);
    // Add small artificial delay for premium feels
    setTimeout(async () => {
      const data = await api.predictions.getForecast(locationId, dateStr, period);
      setForecast(data);
      setLoading(false);
    }, 800);
  };

  return (
    <div className="p-8 space-y-8 bg-charcoal-950 min-h-screen flex-1 overflow-y-auto">
      {/* Header */}
      <div className="flex justify-between items-center border-b border-charcoal-800 pb-6">
        <div>
          <h2 className="text-2xl font-bold text-white tracking-wide">Predictive Forecasting</h2>
          <p className="text-charcoal-400 text-xs mt-1">Generate meal demand predictions with weather integration and SHAP explainability.</p>
        </div>
      </div>

      {/* Control Panel Panel */}
      <div className="glass-panel p-6 rounded-2xl">
        <h3 className="text-sm font-bold text-white mb-4 uppercase tracking-wider">Forecast Parameters</h3>
        <div className="grid grid-cols-1 md:grid-cols-4 gap-6 items-end">
          {/* Location */}
          <div className="space-y-2">
            <label className="text-[11px] text-charcoal-400 font-bold uppercase tracking-wider flex items-center gap-1.5">
              <MapPin className="h-3.5 w-3.5 text-gold-500" />
              Work Location
            </label>
            <select 
              value={locationId}
              onChange={(e) => setLocationId(Number(e.target.value))}
              className="w-full bg-charcoal-900 border border-charcoal-800 rounded-xl px-4 py-3 text-xs text-white focus:outline-none focus:border-gold-500 font-semibold"
            >
              {LOCATIONS.map(loc => (
                <option key={loc.id} value={loc.id}>{loc.name}</option>
              ))}
            </select>
          </div>

          {/* Date */}
          <div className="space-y-2">
            <label className="text-[11px] text-charcoal-400 font-bold uppercase tracking-wider flex items-center gap-1.5">
              <Calendar className="h-3.5 w-3.5 text-gold-500" />
              Target Date
            </label>
            <input 
              type="date"
              value={dateStr}
              onChange={(e) => setDateStr(e.target.value)}
              className="w-full bg-charcoal-900 border border-charcoal-800 rounded-xl px-4 py-3 text-xs text-white focus:outline-none focus:border-gold-500 font-semibold"
            />
          </div>

          {/* Meal Period */}
          <div className="space-y-2">
            <label className="text-[11px] text-charcoal-400 font-bold uppercase tracking-wider flex items-center gap-1.5">
              <Clock className="h-3.5 w-3.5 text-gold-500" />
              Meal Period
            </label>
            <select 
              value={period}
              onChange={(e) => setPeriod(e.target.value)}
              className="w-full bg-charcoal-900 border border-charcoal-800 rounded-xl px-4 py-3 text-xs text-white focus:outline-none focus:border-gold-500 font-semibold"
            >
              <option value="breakfast">Breakfast</option>
              <option value="lunch">Lunch</option>
              <option value="dinner">Dinner</option>
            </select>
          </div>

          {/* Run Button */}
          <button
            onClick={handleGenerate}
            disabled={loading}
            className="w-full bg-gradient-to-r from-gold-500 to-gold-600 hover:from-gold-600 hover:to-gold-700 text-charcoal-950 font-bold text-xs py-3 rounded-xl transition-all shadow-lg shadow-gold-500/10 flex items-center justify-center gap-2 uppercase tracking-wider disabled:opacity-50 cursor-pointer"
          >
            {loading ? (
              <>
                <div className="h-3.5 w-3.5 border-2 border-charcoal-950 border-t-transparent rounded-full animate-spin" />
                Processing...
              </>
            ) : (
              <>
                <Play className="h-3.5 w-3.5 fill-charcoal-950 stroke-0" />
                Generate Forecast
              </>
            )}
          </button>
        </div>
      </div>

      {/* Results View */}
      {forecast ? (
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8 animate-fade-in">
          {/* Main KPI Cards */}
          <div className="lg:col-span-2 space-y-6">
            {/* Forecast Panel */}
            <div className="glass-panel p-8 rounded-2xl relative overflow-hidden">
              <div className="absolute top-0 right-0 h-32 w-32 bg-gold-500/5 rounded-full blur-3xl" />
              <div className="flex justify-between items-start">
                <div>
                  <span className="text-[10px] bg-gold-500/10 border border-gold-500/30 text-gold-400 px-2.5 py-1 rounded-md font-bold uppercase tracking-wider">
                    Model: {forecast.model_version}
                  </span>
                  <h3 className="text-xl font-bold text-white mt-4">Forecast Output Summary</h3>
                </div>
                <div className="text-right">
                  <span className="text-[10px] text-charcoal-400 font-bold uppercase tracking-widest block">Confidence Score</span>
                  <span className="text-xl font-extrabold text-emerald-400">
                    {(forecast.confidence_score * 100).toFixed(1)}%
                  </span>
                </div>
              </div>

              <div className="grid grid-cols-2 md:grid-cols-4 gap-6 mt-8 pt-8 border-t border-charcoal-800/80">
                <div>
                  <span className="text-[10px] text-charcoal-400 font-bold uppercase tracking-wider block">Predicted Demand</span>
                  <span className="text-3xl font-extrabold text-white mt-1 block">{forecast.predicted_count}</span>
                  <span className="text-[10px] text-charcoal-400 mt-1 block">Expected headcount</span>
                </div>
                <div>
                  <span className="text-[10px] text-charcoal-400 font-bold uppercase tracking-wider block">Recommended Prep</span>
                  <span className="text-3xl font-extrabold text-gold-500 mt-1 block">{forecast.recommended_quantity}</span>
                  <span className="text-[10px] text-gold-500/80 mt-1 block">+5% safety buffer</span>
                </div>
                <div>
                  <span className="text-[10px] text-charcoal-400 font-bold uppercase tracking-wider block">Expected Waste</span>
                  <span className="text-3xl font-extrabold text-charcoal-400 mt-1 block">{forecast.predicted_waste}</span>
                  <span className="text-[10px] text-charcoal-400 mt-1 block">Meals margins</span>
                </div>
                <div>
                  <span className="text-[10px] text-charcoal-400 font-bold uppercase tracking-wider block">Capacity Status</span>
                  <span className="text-3xl font-extrabold text-white mt-1 block">
                    {LOCATIONS.find(l => l.id === locationId)?.capacity}
                  </span>
                  <span className="text-[10px] text-charcoal-400 mt-1 block">Max facility capacity</span>
                </div>
              </div>
            </div>

            {/* Waste Alert Mitigation */}
            <div className="glass-panel p-6 rounded-2xl flex gap-4 border-l-4 border-l-amber-500 bg-amber-500/5">
              <ShieldAlert className="h-6 w-6 text-amber-500 shrink-0 mt-0.5" />
              <div>
                <h4 className="text-sm font-bold text-amber-400">Smart Waste Mitigation Recommendation</h4>
                <p className="text-charcoal-300 text-xs mt-1.5 leading-relaxed">
                  Based on historical consumption variance for {period} on similar days, we recommend setting a strict cap of **{forecast.recommended_quantity} prepared meals** with kitchen staff. Additionally, preparing lighter portions and cold items could save an estimated **{Math.round(forecast.predicted_waste * 12)} EGP** in material wastage.
                </p>
              </div>
            </div>

            {/* Natural Language Explanation */}
            <div className="glass-panel p-6 rounded-2xl space-y-3">
              <h4 className="text-xs font-bold text-white uppercase tracking-wider flex items-center gap-2">
                <Sparkles className="h-4 w-4 text-gold-500" />
                Natural Language Explanation
              </h4>
              <p className="text-charcoal-200 text-xs leading-relaxed font-medium">
                {forecast.shap_explanation.natural_language}
              </p>
            </div>
          </div>

          {/* SHAP Explanation Card */}
          <div className="glass-panel p-6 rounded-2xl flex flex-col justify-between">
            <div className="space-y-4">
              <div>
                <h4 className="text-sm font-bold text-white flex items-center gap-2">
                  SHAP Feature Contributions
                  <span title="SHAP values show the relative contribution of each feature to the final prediction.">
                    <Info className="h-3.5 w-3.5 text-charcoal-400 cursor-help" />
                  </span>
                </h4>
                <p className="text-charcoal-400 text-[11px] mt-0.5">Top model decision drivers for this prediction.</p>
              </div>
              <div className="space-y-3 mt-4">
                {forecast.shap_explanation.factors.map((factor: any, idx: number) => {
                  const isPositive = factor.contribution > 0;
                  return (
                    <div key={idx} className="space-y-1.5">
                      <div className="flex justify-between text-[11px]">
                        <span className="font-semibold text-charcoal-300 font-mono">{factor.factor}</span>
                        <span className={`font-bold ${isPositive ? 'text-emerald-400' : 'text-rose-400'}`}>
                          {isPositive ? '+' : ''}{factor.contribution}%
                        </span>
                      </div>
                      <div className="w-full bg-charcoal-800 h-1.5 rounded-full overflow-hidden">
                        <div 
                          className={`h-full rounded-full ${isPositive ? 'bg-emerald-500' : 'bg-rose-500'}`}
                          style={{ width: `${Math.min(Math.abs(factor.contribution) * 2, 100)}%` }}
                        />
                      </div>
                    </div>
                  );
                })}
              </div>
            </div>
            <div className="pt-6 border-t border-charcoal-800/80 text-[10px] text-charcoal-400 font-semibold leading-relaxed mt-6">
              * Positive values represent factors increasing forecasted demand, negative values show factors decreasing demand.
            </div>
          </div>
        </div>
      ) : (
        <div className="glass-panel p-16 rounded-2xl flex flex-col items-center justify-center text-center space-y-4">
          <div className="h-14 w-14 rounded-full bg-charcoal-900 border border-charcoal-800 flex items-center justify-center">
            <TrendingUp className="h-6 w-6 text-charcoal-400" />
          </div>
          <div>
            <h3 className="text-base font-bold text-white">No Forecast Generated</h3>
            <p className="text-charcoal-400 text-xs mt-1 max-w-sm">Select work location, date, and meal period parameters above to compute predictions.</p>
          </div>
        </div>
      )}
    </div>
  );
}
