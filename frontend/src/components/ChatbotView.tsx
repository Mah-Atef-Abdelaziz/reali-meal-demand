'use client';

import React, { useState, useRef, useEffect } from 'react';
import { 
  MessageSquare, 
  Send, 
  Trash2, 
  Bot, 
  User, 
  Sparkles,
  ArrowRight,
  TrendingUp,
  Trash
} from 'lucide-react';
import { api } from '../lib/api';

interface Message {
  id: string;
  role: 'user' | 'assistant' | 'system';
  content: string;
  created_at: string;
}

const QUICK_PROMPTS = [
  { text: "What is tomorrow's lunch forecast?", icon: TrendingUp },
  { text: "How much did food waste decrease?", icon: Trash2 },
  { text: "What menu items are recommended for hot weather?", icon: Sparkles },
];

export default function ChatbotView() {
  const [messages, setMessages] = useState<Message[]>([
    {
      id: 'welcome',
      role: 'assistant',
      content: "Hello! I am **REAL.i Smart Assistant**. I am integrated with your meal demand database and predictive machine learning models.\n\nYou can ask me questions like:\n* *\"What is the forecasted lunch demand for Riyadh HQ tomorrow?\"*\n* *\"How much did we save in food waste cost this week?\"*\n* *\"Recommend a menu configuration based on weather forecasts.\"*",
      created_at: new Date().toISOString()
    }
  ]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const handleSend = async (textToSend?: string) => {
    const messageText = textToSend || input;
    if (!messageText.trim()) return;

    const userMsg: Message = {
      id: Math.random().toString(),
      role: 'user',
      content: messageText,
      created_at: new Date().toISOString()
    };

    setMessages(prev => [...prev, userMsg]);
    setInput('');
    setLoading(true);

    try {
      const response = await api.chatbot.sendMessage('default-session', messageText);
      const assistantMsg: Message = {
        id: response.id || Math.random().toString(),
        role: 'assistant',
        content: response.content,
        created_at: response.created_at || new Date().toISOString()
      };
      setMessages(prev => [...prev, assistantMsg]);
    } catch {
      // Fallback message if something fails
      setMessages(prev => [...prev, {
        id: Math.random().toString(),
        role: 'assistant',
        content: "Sorry, I encountered an issue connecting to the RAG intelligence backend. Please try again later.",
        created_at: new Date().toISOString()
      }]);
    } finally {
      setLoading(false);
    }
  };

  const handleClearChat = () => {
    setMessages([
      {
        id: 'welcome',
        role: 'assistant',
        content: "Hello! Chat session reset. How can I help you optimize meal demand metrics today?",
        created_at: new Date().toISOString()
      }
    ]);
  };

  // Helper to render markdown-like bold and bullet lists simply
  const renderMessageContent = (content: string) => {
    return content.split('\n').map((line, idx) => {
      let formatted = line;
      
      // Simple Bold formatting
      const boldRegex = /\*\*(.*?)\*\*/g;
      const parts = [];
      let lastIndex = 0;
      let match;
      
      while ((match = boldRegex.exec(line)) !== null) {
        parts.push(line.substring(lastIndex, match.index));
        parts.push(<strong key={match.index} className="text-gold-400 font-bold">{match[1]}</strong>);
        lastIndex = boldRegex.lastIndex;
      }
      parts.push(line.substring(lastIndex));
      
      // Check for bullet points
      if (line.trim().startsWith('* ')) {
        return (
          <li key={idx} className="ml-4 list-disc text-xs text-charcoal-200 mt-1 leading-relaxed">
            {parts.length > 1 ? parts : line.replace('* ', '')}
          </li>
        );
      }
      
      return (
        <p key={idx} className="text-xs text-charcoal-150 leading-relaxed min-h-[1rem]">
          {parts.length > 1 ? parts : line}
        </p>
      );
    });
  };

  return (
    <div className="flex bg-charcoal-950 min-h-screen flex-1 overflow-hidden">
      {/* Main Chat Interface */}
      <div className="flex-1 flex flex-col justify-between h-screen relative">
        {/* Chat Header */}
        <div className="p-6 border-b border-charcoal-800 bg-charcoal-900/60 flex justify-between items-center z-10">
          <div className="flex items-center gap-3">
            <div className="h-9 w-9 rounded-lg bg-gold-500/10 border border-gold-500/30 flex items-center justify-center">
              <Bot className="h-5 w-5 text-gold-500" />
            </div>
            <div>
              <h3 className="text-sm font-bold text-white tracking-wide flex items-center gap-2">
                RAG Smart Assistant
                <span className="text-[9px] bg-emerald-500/15 border border-emerald-500/35 text-emerald-400 px-1.5 py-0.5 rounded font-bold uppercase tracking-wider">
                  OpenAI RAG
                </span>
              </h3>
              <p className="text-[10px] text-charcoal-400 mt-0.5">Ask questions about daily counts, waste reduction, and menus.</p>
            </div>
          </div>
          <button 
            onClick={handleClearChat}
            className="flex items-center gap-1.5 px-3 py-1.5 text-xs font-semibold text-charcoal-400 hover:text-white rounded-lg hover:bg-charcoal-800/60 border border-charcoal-800 transition-colors cursor-pointer"
          >
            <Trash className="h-3.5 w-3.5" />
            Reset Chat
          </button>
        </div>

        {/* Message Board */}
        <div className="flex-1 overflow-y-auto p-8 space-y-6 pb-24">
          <div className="max-w-3xl mx-auto space-y-6">
            {messages.map((msg) => {
              const isAssistant = msg.role === 'assistant';
              return (
                <div 
                  key={msg.id} 
                  className={`flex gap-4 ${isAssistant ? 'justify-start' : 'justify-end'}`}
                >
                  {isAssistant && (
                    <div className="h-8 w-8 rounded-lg bg-gold-500/10 border border-gold-500/20 flex items-center justify-center shrink-0">
                      <Bot className="h-4.5 w-4.5 text-gold-500" />
                    </div>
                  )}
                  <div className={`max-w-[75%] p-4.5 rounded-2xl border text-xs leading-relaxed space-y-1.5 shadow-sm ${
                    isAssistant 
                      ? 'bg-charcoal-900 border-charcoal-800/80 text-charcoal-100 rounded-tl-sm' 
                      : 'bg-gradient-to-br from-gold-500/10 to-gold-600/10 border-gold-500/20 text-white rounded-tr-sm'
                  }`}>
                    {isAssistant ? renderMessageContent(msg.content) : <p className="font-medium">{msg.content}</p>}
                    <span className="text-[9px] text-charcoal-500 font-semibold block text-right mt-1.5 select-none">
                      {new Date(msg.created_at).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
                    </span>
                  </div>
                  {!isAssistant && (
                    <div className="h-8 w-8 rounded-lg bg-charcoal-800 border border-charcoal-700 flex items-center justify-center shrink-0">
                      <User className="h-4.5 w-4.5 text-gold-500" />
                    </div>
                  )}
                </div>
              );
            })}
            
            {loading && (
              <div className="flex gap-4 justify-start">
                <div className="h-8 w-8 rounded-lg bg-gold-500/10 border border-gold-500/20 flex items-center justify-center shrink-0">
                  <Bot className="h-4.5 w-4.5 text-gold-500" />
                </div>
                <div className="bg-charcoal-900 border border-charcoal-800/80 p-4 rounded-2xl rounded-tl-sm flex items-center gap-1">
                  <span className="h-1.5 w-1.5 bg-gold-500 rounded-full animate-bounce" style={{ animationDelay: '0ms' }} />
                  <span className="h-1.5 w-1.5 bg-gold-500 rounded-full animate-bounce" style={{ animationDelay: '150ms' }} />
                  <span className="h-1.5 w-1.5 bg-gold-500 rounded-full animate-bounce" style={{ animationDelay: '300ms' }} />
                </div>
              </div>
            )}
            <div ref={messagesEndRef} />
          </div>
        </div>

        {/* Input Dock Area */}
        <div className="absolute bottom-0 left-0 right-0 p-6 bg-gradient-to-t from-charcoal-950 via-charcoal-950 to-transparent border-t border-charcoal-900/40">
          <div className="max-w-3xl mx-auto space-y-4">
            {/* Quick Prompts */}
            {messages.length === 1 && (
              <div className="flex flex-wrap gap-3">
                {QUICK_PROMPTS.map((prompt, idx) => {
                  const Icon = prompt.icon;
                  return (
                    <button
                      key={idx}
                      onClick={() => handleSend(prompt.text)}
                      className="flex items-center gap-2 px-4 py-2 bg-charcoal-900 hover:bg-charcoal-800 border border-charcoal-800 hover:border-gold-500/30 text-charcoal-200 hover:text-white rounded-full text-xs font-semibold transition-all duration-200 shadow-sm cursor-pointer"
                    >
                      <Icon className="h-3.5 w-3.5 text-gold-500" />
                      <span>{prompt.text}</span>
                      <ArrowRight className="h-3 w-3 text-charcoal-400" />
                    </button>
                  );
                })}
              </div>
            )}

            {/* Chat Box */}
            <div className="relative flex items-center">
              <input
                type="text"
                placeholder="Ask about forecasts, waste logs, weather impact..."
                value={input}
                onChange={(e) => setInput(e.target.value)}
                onKeyDown={(e) => e.key === 'Enter' && handleSend()}
                className="w-full bg-charcoal-900 border border-charcoal-800 rounded-2xl px-6 py-4 pr-16 text-xs text-white placeholder-charcoal-400 focus:outline-none focus:border-gold-500/80 font-medium shadow-inner"
              />
              <button
                onClick={() => handleSend()}
                disabled={!input.trim() || loading}
                className="absolute right-3.5 bg-gradient-to-r from-gold-500 to-gold-600 hover:from-gold-600 hover:to-gold-700 text-charcoal-950 p-2.5 rounded-xl transition-all shadow-md shadow-gold-500/10 cursor-pointer disabled:opacity-50 disabled:cursor-not-allowed"
              >
                <Send className="h-4.5 w-4.5" />
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
