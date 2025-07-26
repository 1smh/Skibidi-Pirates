import React, { useState, useEffect } from 'react';
import { CheckCircle, AlertCircle, X } from 'lucide-react';

let toastId = 0;
const toasts = [];
const listeners = [];

export const toast = {
  success: (message) => addToast({ type: 'success', message }),
  error: (message) => addToast({ type: 'error', message }),
  info: (message) => addToast({ type: 'info', message }),
};

const addToast = (toast) => {
  const id = ++toastId;
  const newToast = { id, ...toast, createdAt: Date.now() };
  toasts.push(newToast);
  listeners.forEach(listener => listener([...toasts]));
  
  setTimeout(() => {
    removeToast(id);
  }, 5000);
};

const removeToast = (id) => {
  const index = toasts.findIndex(t => t.id === id);
  if (index > -1) {
    toasts.splice(index, 1);
    listeners.forEach(listener => listener([...toasts]));
  }
};

const Toaster = () => {
  const [toastList, setToastList] = useState([]);

  useEffect(() => {
    listeners.push(setToastList);
    return () => {
      const index = listeners.indexOf(setToastList);
      if (index > -1) listeners.splice(index, 1);
    };
  }, []);

  const getIcon = (type) => {
    switch (type) {
      case 'success':
        return <CheckCircle size={20} className="text-green-600" />;
      case 'error':
        return <AlertCircle size={20} className="text-red-600" />;
      default:
        return <AlertCircle size={20} className="text-blue-600" />;
    }
  };

  const getStyles = (type) => {
    switch (type) {
      case 'success':
        return 'bg-green-50 border-green-200';
      case 'error':
        return 'bg-red-50 border-red-200';
      default:
        return 'bg-blue-50 border-blue-200';
    }
  };

  return (
    <div className="fixed top-4 right-4 z-50 space-y-2">
      {toastList.map((toast) => (
        <div
          key={toast.id}
          className={`
            flex items-center gap-3 p-4 rounded-xl border shadow-sm
            animate-in slide-in-from-right duration-300
            ${getStyles(toast.type)}
          `}
        >
          {getIcon(toast.type)}
          <span className="text-sm font-medium flex-1">{toast.message}</span>
          <button
            onClick={() => removeToast(toast.id)}
            className="text-gray-400 hover:text-gray-600 transition-colors"
          >
            <X size={16} />
          </button>
        </div>
      ))}
    </div>
  );
};

export default Toaster;