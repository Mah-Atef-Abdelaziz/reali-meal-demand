'use client';

import React, { useState } from 'react';
import { 
  FileText, 
  Download, 
  Calendar, 
  Database, 
  ShieldCheck, 
  ExternalLink,
  ChevronRight
} from 'lucide-react';

const AUDIT_LOGS = [
  { id: 1, user: 'admin', action: 'EXPORT_REPORT', details: 'Exported consumption report for HQ-CAI', time: '10 mins ago', ip: '192.168.1.45' },
  { id: 2, user: 'admin', action: 'UPDATE_VISITOR_LOG', details: 'Added visitor log for EGPC (+45)', time: '2 hours ago', ip: '192.168.1.45' },
  { id: 3, user: 'system', action: 'DAILY_FORECAST_GENERATION', details: 'Generated forecasts for 15 locations', time: '4 hours ago', ip: '127.0.0.1' },
  { id: 4, user: 'admin', action: 'USER_LOGIN', details: 'Successful login from administrator account', time: '5 hours ago', ip: '192.168.1.45' },
];

export default function ReportsView() {
  const [startDate, setStartDate] = useState('2026-06-01');
  const [endDate, setEndDate] = useState('2026-06-29');
  const [reportType, setReportType] = useState('consumption');
  const [loading, setLoading] = useState(false);

  const handleExport = (format: 'csv' | 'xlsx') => {
    setLoading(true);
    setTimeout(() => {
      // Simulate download
      const content = `Date,Location,Period,Forecast,Actual,Waste\n2026-06-01,HQ-CAI,lunch,1680,1650,30`;
      const blob = new Blob([content], { type: 'text/csv' });
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.setAttribute('href', url);
      a.setAttribute('download', `reali_${reportType}_report_${startDate}_to_${endDate}.${format}`);
      a.click();
      setLoading(false);
    }, 1000);
  };

  return (
    <div className="p-8 space-y-8 bg-charcoal-950 min-h-screen flex-1 overflow-y-auto">
      {/* Header */}
      <div className="flex justify-between items-center border-b border-charcoal-800 pb-6">
        <div>
          <h2 className="text-2xl font-bold text-white tracking-wide">Reports & System Logs</h2>
          <p className="text-charcoal-400 text-xs mt-1">Export consumption analytics and view system audit trails for operational compliance.</p>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        {/* Export Parameters */}
        <div className="lg:col-span-2 space-y-6">
          <div className="glass-panel p-6 rounded-2xl space-y-5">
            <h3 className="text-sm font-bold text-white uppercase tracking-wider flex items-center gap-2">
              <FileText className="h-4.5 w-4.5 text-gold-500" />
              Generate Export Report
            </h3>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div className="space-y-1.5">
                <label className="text-[10px] text-charcoal-400 font-bold uppercase tracking-wider block">Start Date</label>
                <input 
                  type="date" 
                  value={startDate}
                  onChange={(e) => setStartDate(e.target.value)}
                  className="w-full bg-charcoal-900 border border-charcoal-800 rounded-xl px-4 py-3 text-xs text-white focus:outline-none focus:border-gold-500 font-semibold"
                />
              </div>
              <div className="space-y-1.5">
                <label className="text-[10px] text-charcoal-400 font-bold uppercase tracking-wider block">End Date</label>
                <input 
                  type="date" 
                  value={endDate}
                  onChange={(e) => setEndDate(e.target.value)}
                  className="w-full bg-charcoal-900 border border-charcoal-800 rounded-xl px-4 py-3 text-xs text-white focus:outline-none focus:border-gold-500 font-semibold"
                />
              </div>
            </div>

            <div className="space-y-1.5">
              <label className="text-[10px] text-charcoal-400 font-bold uppercase tracking-wider block">Report Type</label>
              <select 
                value={reportType}
                onChange={(e) => setReportType(e.target.value)}
                className="w-full bg-charcoal-900 border border-charcoal-800 rounded-xl px-4 py-3 text-xs text-white focus:outline-none focus:border-gold-500 font-semibold"
              >
                <option value="consumption">Meal Consumption Summary (Standard)</option>
                <option value="waste">Wastage Logs & Cost Analysis</option>
                <option value="accuracy">Forecast Performance & Accuracy Logs</option>
                <option value="visitors">External Visitor Impact Logs</option>
              </select>
            </div>

            <div className="flex gap-4 pt-4">
              <button
                onClick={() => handleExport('csv')}
                disabled={loading}
                className="flex-1 bg-charcoal-800 hover:bg-charcoal-700 border border-charcoal-700/60 text-white font-bold text-xs py-3 rounded-xl transition-all flex items-center justify-center gap-2 uppercase tracking-wider cursor-pointer"
              >
                <Download className="h-4 w-4 text-gold-500" />
                Export CSV
              </button>
              <button
                onClick={() => handleExport('xlsx')}
                disabled={loading}
                className="flex-1 bg-gradient-to-r from-gold-500 to-gold-600 hover:from-gold-600 hover:to-gold-700 text-charcoal-950 font-bold text-xs py-3 rounded-xl transition-all shadow-md shadow-gold-500/10 flex items-center justify-center gap-2 uppercase tracking-wider cursor-pointer"
              >
                <Download className="h-4 w-4" />
                Export Excel (XLSX)
              </button>
            </div>
          </div>

          {/* Database Info Cards */}
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div className="glass-panel p-5 rounded-2xl flex items-center gap-4">
              <div className="h-10 w-10 rounded-lg bg-gold-500/10 border border-gold-500/20 flex items-center justify-center">
                <Database className="h-5 w-5 text-gold-500" />
              </div>
              <div>
                <h4 className="text-xs font-bold text-white uppercase tracking-wider">Database Engine</h4>
                <p className="text-charcoal-300 text-xs mt-1 font-medium">SQLite (Local Serverless)</p>
                <span className="text-[9px] text-charcoal-400 font-semibold block mt-0.5">Size: 142.5 MB (Full logs)</span>
              </div>
            </div>
            <div className="glass-panel p-5 rounded-2xl flex items-center gap-4">
              <div className="h-10 w-10 rounded-lg bg-emerald-500/10 border border-emerald-500/20 flex items-center justify-center">
                <ShieldCheck className="h-5 w-5 text-emerald-400" />
              </div>
              <div>
                <h4 className="text-xs font-bold text-white uppercase tracking-wider">Security Protocol</h4>
                <p className="text-charcoal-300 text-xs mt-1 font-medium">JWT-Token Authentication</p>
                <span className="text-[9px] text-emerald-400 font-semibold block mt-0.5">RBAC Enabled (Admin Mode)</span>
              </div>
            </div>
          </div>
        </div>

        {/* System Audit Trail */}
        <div className="glass-panel p-6 rounded-2xl space-y-4">
          <div>
            <h3 className="text-sm font-bold text-white uppercase tracking-wider">Security Audit Trail</h3>
            <p className="text-charcoal-400 text-[11px] mt-0.5">Real-time system events and transaction records.</p>
          </div>
          <div className="space-y-4">
            {AUDIT_LOGS.map((log) => (
              <div key={log.id} className="space-y-2 pb-3.5 border-b border-charcoal-800/80 last:border-0 last:pb-0">
                <div className="flex justify-between text-[10px]">
                  <span className="font-bold text-gold-500 uppercase tracking-wider">{log.action}</span>
                  <span className="text-charcoal-400 font-semibold">{log.time}</span>
                </div>
                <p className="text-xs text-charcoal-200 leading-normal">{log.details}</p>
                <div className="flex gap-4 text-[9px] text-charcoal-400 font-semibold">
                  <span>User: <strong className="text-charcoal-300 font-bold">{log.user}</strong></span>
                  <span>IP: {log.ip}</span>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}
