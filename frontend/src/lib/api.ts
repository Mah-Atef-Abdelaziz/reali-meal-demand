/**
 * API Client — Integrates with FastAPI backend or falls back to mock data.
 */

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api/v1';

// Helper to get auth headers
const getHeaders = () => {
  const token = typeof window !== 'undefined' ? localStorage.getItem('token') : null;
  return {
    'Content-Type': 'application/json',
    ...(token ? { Authorization: `Bearer ${token}` } : {}),
  };
};

// Check if backend is alive
export async function pingBackend(): Promise<boolean> {
  try {
    const res = await fetch(`${API_BASE_URL.replace('/api/v1', '')}/health`, { method: 'GET', signal: AbortSignal.timeout(2000) });
    return res.ok;
  } catch {
    return false;
  }
}

// Simulated data generator for offline fallback
export const mockData = {
  dashboard: {
    getSummary: () => ({
      total_predictions: 1450,
      average_confidence: 0.942,
      saved_cost_sar: 148500.0,
      waste_reduction_percent: 24.5,
      actual_vs_predicted_accuracy: 96.8,
    }),
    getLocationCapacity: () => [
      { location: 'HQ-RYD', capacity: 2000, demand: 1680 },
      { location: 'OFF-JED', capacity: 800, demand: 620 },
      { location: 'ONS-JBL', capacity: 1500, demand: 1320 },
      { location: 'OFS-SHB', capacity: 600, demand: 540 },
      { location: 'ONS-YNB', capacity: 1200, demand: 980 },
    ],
    getPeriodShares: () => [
      { period: 'Breakfast', count: 32540, color: '#dec15c' },
      { period: 'Lunch', count: 98450, color: '#c59424' },
      { period: 'Dinner', count: 42100, color: '#4e505b' },
    ],
    getWeeklyWasteTrend: () => [
      { date: 'Sun', prepared: 3400, wasted: 510 },
      { date: 'Mon', prepared: 3450, wasted: 480 },
      { date: 'Tue', prepared: 3420, wasted: 390 },
      { date: 'Wed', prepared: 3500, wasted: 350 },
      { date: 'Thu', prepared: 3300, wasted: 280 },
      { date: 'Fri', prepared: 1200, wasted: 90 },
      { date: 'Sat', prepared: 1250, wasted: 95 },
    ],
    getAccuracyTrend: () => [
      { week: 'W1', accuracy: 92.4 },
      { week: 'W2', accuracy: 94.1 },
      { week: 'W3', accuracy: 95.8 },
      { week: 'W4', accuracy: 96.8 },
    ],
  },
  predictions: {
    forecast: (locationId: number, dateStr: string, period: string) => {
      const baseCount = locationId === 1 ? 1680 : 540;
      const periodMultiplier = period === 'lunch' ? 1.0 : period === 'breakfast' ? 0.45 : 0.35;
      const predicted = Math.round(baseCount * periodMultiplier + (Math.random() * 40 - 20));
      const confidence = 0.90 + Math.random() * 0.08;
      const recommended = Math.round(predicted * 1.05); // 5% buffer
      
      return {
        prediction_date: dateStr,
        location_id: locationId,
        period: period,
        predicted_count: predicted,
        confidence_score: confidence,
        recommended_quantity: recommended,
        predicted_waste: Math.round(predicted * 0.04),
        model_version: 'xgb-v1.0.0',
        shap_explanation: {
          factors: [
            { factor: 'same_dow_last_week', value: `${Math.round(predicted * 0.98)}`, contribution: 45.2 },
            { factor: 'lag_7d', value: `${Math.round(predicted * 0.99)}`, contribution: 32.1 },
            { factor: 'rolling_mean_7d', value: `${Math.round(predicted * 0.96)}`, contribution: 12.5 },
            { factor: 'is_holiday', value: '0', contribution: -2.4 },
            { factor: 'temperature_avg', value: '38°C', contribution: -8.1 },
          ],
          natural_language: `The predicted meal count is ${predicted}. Key factors: same day last week demand increased the prediction; high temperature slightly decreased the expected lunch turnout.`
        }
      };
    }
  },
  chatbot: {
    sendMessage: (message: string) => {
      const lower = message.toLowerCase();
      let response = "I'm REAL.i Assistant. I can help analyze meal consumption patterns, view predictions, or generate reports.";
      
      if (lower.includes('forecast') || lower.includes('predict')) {
        response = "Based on the XGBoost model, the lunch forecast for Riyadh Headquarters tomorrow is **1,720 meals** (confidence score: **95.4%**). I recommend preparing 1,800 meals to maintain a safe 5% buffer.";
      } else if (lower.includes('waste') || lower.includes('wasted')) {
        response = "Total food waste has decreased by **24.5%** since deployment. The onshore plants (Jubail, Yanbu) showed the highest waste reduction after adjusting daily menus.";
      } else if (lower.includes('menu') || lower.includes('recommend')) {
        response = "For high-temperature days (above 40°C), I recommend lighter items: Grilled Chicken Salad, Fruit Platters, and Fish Fillets. These see 12-18% higher demand during hot weather compared to heavy rice dishes.";
      }
      
      return {
        id: Math.random().toString(),
        role: 'assistant',
        content: response,
        created_at: new Date().toISOString()
      };
    }
  }
};

export const api = {
  dashboard: {
    getSummary: async () => {
      try {
        const res = await fetch(`${API_BASE_URL}/dashboard/summary`, { headers: getHeaders() });
        if (!res.ok) throw new Error();
        return await res.json();
      } catch {
        return mockData.dashboard.getSummary();
      }
    },
    getLocationCapacity: async () => {
      try {
        const res = await fetch(`${API_BASE_URL}/dashboard/locations`, { headers: getHeaders() });
        if (!res.ok) throw new Error();
        return await res.json();
      } catch {
        return mockData.dashboard.getLocationCapacity();
      }
    },
    getPeriodShares: async () => {
      try {
        const res = await fetch(`${API_BASE_URL}/dashboard/periods`, { headers: getHeaders() });
        if (!res.ok) throw new Error();
        return await res.json();
      } catch {
        return mockData.dashboard.getPeriodShares();
      }
    },
    getWeeklyWaste: async () => {
      try {
        const res = await fetch(`${API_BASE_URL}/dashboard/waste`, { headers: getHeaders() });
        if (!res.ok) throw new Error();
        return await res.json();
      } catch {
        return mockData.dashboard.getWeeklyWasteTrend();
      }
    }
  },
  predictions: {
    getForecast: async (locationId: number, dateStr: string, period: string) => {
      try {
        const url = `${API_BASE_URL}/predictions/forecast?location_id=${locationId}&date=${dateStr}&period=${period}`;
        const res = await fetch(url, { headers: getHeaders() });
        if (!res.ok) throw new Error();
        return await res.json();
      } catch {
        return mockData.predictions.forecast(locationId, dateStr, period);
      }
    }
  },
  chatbot: {
    sendMessage: async (sessionId: string, message: string) => {
      try {
        const res = await fetch(`${API_BASE_URL}/chatbot/message`, {
          method: 'POST',
          headers: getHeaders(),
          body: JSON.stringify({ session_id: sessionId, message }),
        });
        if (!res.ok) throw new Error();
        return await res.json();
      } catch {
        return mockData.chatbot.sendMessage(message);
      }
    }
  }
};
