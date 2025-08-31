// 股票相关类型
export interface Stock {
  id: string;
  symbol: string;
  name: string;
  price: number;
  change: number;
  changePercent: number;
  volume: string;
  marketCap: string;
  sector: string;
  industry: string;
}

// 用户相关类型
export interface User {
  id: string;
  username: string;
  email: string;
  avatar?: string;
  role: 'admin' | 'user' | 'analyst';
}

// 投资组合类型
export interface Portfolio {
  id: string;
  name: string;
  description?: string;
  totalValue: number;
  totalCost: number;
  totalReturn: number;
  returnPercent: number;
  stocks: PortfolioStock[];
}

export interface PortfolioStock {
  stockId: string;
  symbol: string;
  name: string;
  quantity: number;
  avgPrice: number;
  currentPrice: number;
  totalValue: number;
  totalCost: number;
  return: number;
  returnPercent: number;
}

// API响应类型
export interface ApiResponse<T> {
  success: boolean;
  data: T;
  message?: string;
  error?: string;
}

// 分页类型
export interface Pagination {
  current: number;
  pageSize: number;
  total: number;
}

// 表格数据类型
export interface TableData<T> {
  data: T[];
  pagination: Pagination;
} 