import dayjs from 'dayjs';

// 格式化数字
export const formatNumber = (num: number, decimals: number = 2): string => {
  if (isNaN(num)) return '0';
  return num.toLocaleString('zh-CN', {
    minimumFractionDigits: decimals,
    maximumFractionDigits: decimals,
  });
};

// 格式化货币
export const formatCurrency = (amount: number, currency: string = 'USD'): string => {
  if (isNaN(amount)) return '$0.00';
  return new Intl.NumberFormat('zh-CN', {
    style: 'currency',
    currency,
  }).format(amount);
};

// 格式化百分比
export const formatPercent = (value: number, decimals: number = 2): string => {
  if (isNaN(value)) return '0%';
  return `${value.toFixed(decimals)}%`;
};

// 格式化日期
export const formatDate = (date: string | Date, format: string = 'YYYY-MM-DD'): string => {
  return dayjs(date).format(format);
};

// 计算涨跌幅颜色
export const getChangeColor = (change: number): string => {
  if (change > 0) return 'text-green-600';
  if (change < 0) return 'text-red-600';
  return 'text-gray-600';
};

// 防抖函数
export const debounce = <T extends (...args: any[]) => any>(
  func: T,
  wait: number
): ((...args: Parameters<T>) => void) => {
  let timeout: ReturnType<typeof setTimeout>;
  return (...args: Parameters<T>) => {
    clearTimeout(timeout);
    timeout = setTimeout(() => func(...args), wait);
  };
};

// 节流函数
export const throttle = <T extends (...args: any[]) => any>(
  func: T,
  limit: number
): ((...args: Parameters<T>) => void) => {
  let inThrottle: boolean;
  return (...args: Parameters<T>) => {
    if (!inThrottle) {
      func(...args);
      inThrottle = true;
      setTimeout(() => (inThrottle = false), limit);
    }
  };
};

// 生成唯一ID
export const generateId = (): string => {
  return Math.random().toString(36).substr(2, 9);
};

// 深拷贝
export const deepClone = <T>(obj: T): T => {
  if (obj === null || typeof obj !== 'object') return obj;
  if (obj instanceof Date) return new Date(obj.getTime()) as unknown as T;
  if (obj instanceof Array) return obj.map(item => deepClone(item)) as unknown as T;
  if (typeof obj === 'object') {
    const clonedObj = {} as T;
    for (const key in obj) {
      if (obj.hasOwnProperty(key)) {
        clonedObj[key] = deepClone(obj[key]);
      }
    }
    return clonedObj;
  }
  return obj;
}; 