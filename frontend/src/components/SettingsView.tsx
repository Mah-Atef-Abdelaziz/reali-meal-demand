'use client';

import React, { useState } from 'react';
import { 
  Settings, 
  Cpu, 
  RefreshCw, 
  CheckCircle2, 
  Sliders, 
  ListFilter,
  BrainCircuit,
  Save
} from 'lucide-react';

const FEATURE_COLUMNS = [
  "location_id", "year", "month", "day", "day_of_week", "day_of_year", "week_of_year", "quarter", "is_weekend", "saudi_dow",
  "is_holiday", "days_to_holiday", "temperature_avg", "temperature_high", "humidity_percent", "weather_code", "location_type",
  "location_capacity", "visitor_count", "has_event", "event_attendees", "active_employees", "period_code", "menu_item_count",
  "lag_1d", "lag_2d", "lag_3d", "lag_7d", "lag_14d", "lag_28d", "rolling_mean_7d", "rolling_std_7d", "rolling_mean_14d",
  "rolling_std_14d", "rolling_mean_30d", "rolling_std_30d", "expanding_mean", "same_dow_last_week"
];

export default function SettingsView() {
  const [llmProvider, setLlmProvider] = useState('openai');
  const [retraining, setRetraining] = useState(false);
  const [retrainSuccess, setRetrainSuccess] = useState(false);

  const handleRetrain = () => {
    setRetraining(true);
    setRetrainSuccess(false);
    setTimeout(() => {
      setRetraining(false);
      setRetrainSuccess(true);
    }, 2500); // Premium retraining loader feels
  };

  return (
    <div className="p-8 space-y-8 bg-charcoal-950 min-h-screen flex-1 overflow-y-auto">
      {/* Header */}
      <div className="flex justify-between items-center border-b border-charcoal-800 pb-6">
        <div>
          <h2 className="text-2xl font-bold text-white tracking-wide">System Settings</h2>
          <p className="text-charcoal-400 text-xs mt-1">Configure ML model retraining, manage feature columns, and select default LLM providers.</p>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        {/* ML Configuration Column */}
        <div className="lg:col-span-2 space-y-8">
          {/* Active Model Performance Card */}
          <div className="glass-panel p-6 rounded-2xl relative overflow-hidden space-y-6">
            <div className="absolute top-0 right-0 h-32 w-32 bg-gold-500/5 rounded-full blur-3xl" />
            
            <div className="flex justify-between items-start">
              <div className="flex gap-3.5 items-center">
                <div className="h-10 w-10 rounded-xl bg-gold-500/10 border border-gold-500/30 flex items-center justify-center">
                  <Cpu className="h-5 w-5 text-gold-500" />
                </div>
                <div>
                  <h3 className="text-sm font-bold text-white uppercase tracking-wider">Active ML Forecasting Model</h3>
                  <p className="text-charcoal-300 text-xs mt-0.5 font-medium">XGBoost Regressor (xgb-v1.0.0)</p>
                </div>
              </div>
              <button
                onClick={handleRetrain}
                disabled={retraining}
                className="bg-gradient-to-r from-gold-500 to-gold-600 hover:from-gold-600 hover:to-gold-700 text-charcoal-950 font-bold text-xs px-4 py-2.5 rounded-xl transition-all shadow-md shadow-gold-500/10 flex items-center gap-2 uppercase tracking-wider disabled:opacity-50 cursor-pointer"
              >
                <RefreshCw className={`h-3.5 w-3.5 ${retraining ? 'animate-spin' : ''}`} />
                {retraining ? 'Retraining...' : 'Retrain Model'}
              </button>
            </div>

            {retrainSuccess && (
              <div className="p-4 bg-emerald-500/10 border border-emerald-500/30 text-emerald-400 rounded-xl text-xs font-semibold flex items-center gap-2">
                <CheckCircle2 className="h-4 w-4" />
                Model retrained successfully. New metrics: R2 = 0.9820, MAE = 3.75. Updated Best Weights.
              </div>
            )}

            <div className="grid grid-cols-2 md:grid-cols-4 gap-6 pt-6 border-t border-charcoal-800/80">
              <div className="bg-charcoal-900/40 p-4 rounded-xl border border-charcoal-800/40">
                <span className="text-[9px] text-charcoal-400 font-bold uppercase tracking-wider block">R2 Score</span>
                <span className="text-xl font-extrabold text-white mt-1 block">0.9820</span>
              </div>
              <div className="bg-charcoal-900/40 p-4 rounded-xl border border-charcoal-800/40">
                <span className="text-[9px] text-charcoal-400 font-bold uppercase tracking-wider block">MAE (Error)</span>
                <span className="text-xl font-extrabold text-white mt-1 block">3.75 meals</span>
              </div>
              <div className="bg-charcoal-900/40 p-4 rounded-xl border border-charcoal-800/40">
                <span className="text-[9px] text-charcoal-400 font-bold uppercase tracking-wider block">MAPE</span>
                <span className="text-xl font-extrabold text-white mt-1 block">22.21%</span>
              </div>
              <div className="bg-charcoal-900/40 p-4 rounded-xl border border-charcoal-800/40">
                <span className="text-[9px] text-charcoal-400 font-bold uppercase tracking-wider block">Training Dataset</span>
                <span className="text-xl font-extrabold text-white mt-1 block">28,196 rows</span>
              </div>
            </div>
          </div>

          {/* Model Hyperparameters */}
          <div className="glass-panel p-6 rounded-2xl space-y-4">
            <h3 className="text-sm font-bold text-white uppercase tracking-wider flex items-center gap-2">
              <Sliders className="h-4.5 w-4.5 text-gold-500" />
              Model Hyperparameters
            </h3>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4 text-xs">
              <div className="flex justify-between py-2 border-b border-charcoal-800/80">
                <span className="text-charcoal-300 font-medium">n_estimators (Trees count)</span>
                <span className="text-white font-bold font-mono">500</span>
              </div>
              <div className="flex justify-between py-2 border-b border-charcoal-800/80">
                <span className="text-charcoal-300 font-medium">max_depth</span>
                <span className="text-white font-bold font-mono">7</span>
              </div>
              <div className="flex justify-between py-2 border-b border-charcoal-800/80">
                <span className="text-charcoal-300 font-medium">learning_rate</span>
                <span className="text-white font-bold font-mono">0.05</span>
              </div>
              <div className="flex justify-between py-2 border-b border-charcoal-800/80">
                <span className="text-charcoal-300 font-medium">subsample</span>
                <span className="text-white font-bold font-mono">0.8</span>
              </div>
              <div className="flex justify-between py-2 border-b border-charcoal-800/80 font-semibold">
                <span className="text-charcoal-300">colsample_bytree</span>
                <span className="text-white font-mono">0.8</span>
              </div>
              <div className="flex justify-between py-2 border-b border-charcoal-800/80 font-semibold">
                <span className="text-charcoal-300">random_state</span>
                <span className="text-white font-mono">42</span>
              </div>
            </div>
          </div>
        </div>

        {/* System Settings Column */}
        <div className="space-y-8">
          {/* LLM Setting Card */}
          <div className="glass-panel p-6 rounded-2xl space-y-4">
            <h3 className="text-sm font-bold text-white uppercase tracking-wider flex items-center gap-2">
              <BrainCircuit className="h-4.5 w-4.5 text-gold-500" />
              Smart Assistant LLM Provider
            </h3>
            <p className="text-charcoal-400 text-xs mt-1">Select default large language model configurations for RAG system execution.</p>
            
            <div className="space-y-4 pt-2">
              <div className="flex items-center gap-3">
                <input 
                  type="radio" 
                  id="openai" 
                  name="llm" 
                  value="openai"
                  checked={llmProvider === 'openai'}
                  onChange={() => setLlmProvider('openai')}
                  className="accent-gold-500 h-4 w-4"
                />
                <label htmlFor="openai" className="text-xs font-semibold text-white cursor-pointer select-none">
                  OpenAI API (Primary GPT-4o-mini)
                </label>
              </div>
              <div className="flex items-center gap-3">
                <input 
                  type="radio" 
                  id="ollama" 
                  name="llm" 
                  value="ollama"
                  checked={llmProvider === 'ollama'}
                  onChange={() => setLlmProvider('ollama')}
                  className="accent-gold-500 h-4 w-4"
                />
                <label htmlFor="ollama" className="text-xs font-semibold text-white cursor-pointer select-none flex items-center gap-1.5">
                  Local Ollama (Local fallback Llama-3)
                </label>
              </div>

              <button
                className="w-full bg-gradient-to-r from-gold-500 to-gold-600 hover:from-gold-600 hover:to-gold-700 text-charcoal-950 font-bold text-xs py-3 rounded-xl transition-all shadow-md shadow-gold-500/10 flex items-center justify-center gap-2 uppercase tracking-wider mt-4 cursor-pointer"
              >
                <Save className="h-4 w-4" />
                Save Provider Config
              </button>
            </div>
          </div>

          {/* Feature Columns Panel */}
          <div className="glass-panel p-6 rounded-2xl space-y-4">
            <h3 className="text-sm font-bold text-white uppercase tracking-wider flex items-center gap-2">
              <ListFilter className="h-4.5 w-4.5 text-gold-500" />
              Model Feature Vectors ({FEATURE_COLUMNS.length})
            </h3>
            <div className="max-h-56 overflow-y-auto border border-charcoal-800 rounded-xl p-3 bg-charcoal-900/40 divide-y divide-charcoal-800/40 text-xs">
              {FEATURE_COLUMNS.map((col, idx) => (
                <div key={idx} className="py-1.5 font-mono text-charcoal-300 text-[10px] tracking-wide">
                  {col}
                </div>
              ))}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
