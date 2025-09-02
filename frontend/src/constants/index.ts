// API相关常量
export const API_ENDPOINTS = {
  AUTH: {
    LOGIN: '/auth/login',
    LOGOUT: '/auth/logout',
    REFRESH: '/auth/refresh',
    PROFILE: '/auth/profile',
  },
  STOCKS: {
    LIST: '/stocks',
    DETAIL: '/stocks/:id',
    SEARCH: '/stocks/search',
    QUOTE: '/stocks/:id/quote',
  },
  PORTFOLIO: {
    LIST: '/portfolio',
    DETAIL: '/portfolio/:id',
    CREATE: '/portfolio',
    UPDATE: '/portfolio/:id',
    DELETE: '/portfolio/:id',
  },
  ANALYSIS: {
    TECHNICAL: '/analysis/technical',
    FUNDAMENTAL: '/analysis/fundamental',
    SENTIMENT: '/analysis/sentiment',
  },
} as const;

// 股票相关常量
export const STOCK_SECTORS = [
  '科技',
  '金融',
  '医疗保健',
  '消费品',
  '工业',
  '能源',
  '材料',
  '公用事业',
  '房地产',
  '通信服务',
] as const;

export const STOCK_INDUSTRIES = {
  科技: ['软件', '硬件', '互联网', '半导体', '人工智能'],
  金融: ['银行', '保险', '投资', '房地产信托'],
  医疗保健: ['制药', '生物技术', '医疗器械', '医疗服务'],
  消费品: ['零售', '食品饮料', '服装', '家居'],
  工业: ['制造', '建筑', '运输', '航空航天'],
  能源: ['石油天然气', '可再生能源', '公用事业'],
  材料: ['化工', '金属', '建筑材料'],
  公用事业: ['电力', '天然气', '水务'],
  房地产: ['住宅', '商业', '工业地产'],
  通信服务: ['电信', '媒体', '娱乐'],
} as const;

// 时间相关常量
export const TIME_PERIODS = {
  DAY: '1d',
  WEEK: '1w',
  MONTH: '1m',
  QUARTER: '3m',
  YEAR: '1y',
  FIVE_YEARS: '5y',
} as const;

// 图表相关常量
export const CHART_TYPES = {
  LINE: 'line',
  CANDLESTICK: 'candlestick',
  BAR: 'bar',
  AREA: 'area',
  SCATTER: 'scatter',
} as const;

// 主题相关常量
export const THEMES = {
  LIGHT: 'light',
  DARK: 'dark',
  AUTO: 'auto',
} as const;

// 本地存储键名
export const STORAGE_KEYS = {
  THEME: 'theme',
  TOKEN: 'token',
  USER_INFO: 'userInfo',
  SETTINGS: 'settings',
} as const;

// 分页默认值
export const PAGINATION_DEFAULTS = {
  PAGE_SIZE: 20,
  PAGE_SIZE_OPTIONS: ['10', '20', '50', '100'],
} as const; 