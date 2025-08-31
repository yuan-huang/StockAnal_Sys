import { create } from 'zustand';
import type { Stock } from '../types';

interface StockState {
  // 状态
  stocks: Stock[];
  watchlist: string[]; // 股票代码数组
  selectedStock: Stock | null;
  isLoading: boolean;
  error: string | null;
  
  // 分页
  currentPage: number;
  pageSize: number;
  total: number;
  
  // 筛选
  searchQuery: string;
  sectorFilter: string;
  industryFilter: string;
  
  // 操作
  fetchStocks: (page?: number, pageSize?: number) => Promise<void>;
  fetchStockDetail: (symbol: string) => Promise<void>;
  searchStocks: (query: string) => Promise<void>;
  addToWatchlist: (symbol: string) => void;
  removeFromWatchlist: (symbol: string) => void;
  setFilters: (filters: { sector?: string; industry?: string }) => void;
  clearFilters: () => void;
  setLoading: (loading: boolean) => void;
  setError: (error: string | null) => void;
}

export const useStockStore = create<StockState>((set, get) => ({
  // 初始状态
  stocks: [],
  watchlist: [],
  selectedStock: null,
  isLoading: false,
  error: null,
  currentPage: 1,
  pageSize: 20,
  total: 0,
  searchQuery: '',
  sectorFilter: '',
  industryFilter: '',

  // 获取股票列表
  fetchStocks: async (page = 1, pageSize = 20) => {
    set({ isLoading: true, error: null });
    try {
      // 模拟API调用
      await new Promise(resolve => setTimeout(resolve, 800));
      
      // 模拟股票数据
      const mockStocks: Stock[] = [
        {
          id: '1',
          symbol: 'AAPL',
          name: '苹果公司',
          price: 150.25,
          change: 2.5,
          changePercent: 1.69,
          volume: '45.2M',
          marketCap: '2.4T',
          sector: '科技',
          industry: '硬件'
        },
        {
          id: '2',
          symbol: 'GOOGL',
          name: '谷歌公司',
          price: 2750.80,
          change: -1.2,
          changePercent: -0.04,
          volume: '12.8M',
          marketCap: '1.8T',
          sector: '科技',
          industry: '互联网'
        },
        {
          id: '3',
          symbol: 'MSFT',
          name: '微软公司',
          price: 320.45,
          change: 3.8,
          changePercent: 1.20,
          volume: '28.9M',
          marketCap: '2.1T',
          sector: '科技',
          industry: '软件'
        },
        {
          id: '4',
          symbol: 'TSLA',
          name: '特斯拉公司',
          price: 245.67,
          change: -5.2,
          changePercent: -2.07,
          volume: '35.6M',
          marketCap: '780B',
          sector: '工业',
          industry: '汽车'
        },
        {
          id: '5',
          symbol: 'AMZN',
          name: '亚马逊公司',
          price: 135.89,
          change: 1.8,
          changePercent: 1.34,
          volume: '42.1M',
          marketCap: '1.4T',
          sector: '消费品',
          industry: '零售'
        }
      ];
      
      set({
        stocks: mockStocks,
        currentPage: page,
        pageSize,
        total: mockStocks.length,
        isLoading: false
      });
    } catch (error) {
      set({ 
        error: '获取股票数据失败', 
        isLoading: false 
      });
      console.error('Fetch stocks failed:', error);
    }
  },

  // 获取股票详情
  fetchStockDetail: async (symbol: string) => {
    set({ isLoading: true, error: null });
    try {
      // 模拟API调用
      await new Promise(resolve => setTimeout(resolve, 500));
      
      const stock = get().stocks.find(s => s.symbol === symbol);
      if (stock) {
        set({ selectedStock: stock, isLoading: false });
      } else {
        set({ error: '股票不存在', isLoading: false });
      }
    } catch (error) {
      set({ 
        error: '获取股票详情失败', 
        isLoading: false 
      });
      console.error('Fetch stock detail failed:', error);
    }
  },

  // 搜索股票
  searchStocks: async (query: string) => {
    set({ searchQuery: query, isLoading: true, error: null });
    try {
      // 模拟API调用
      await new Promise(resolve => setTimeout(resolve, 600));
      
      const allStocks = get().stocks;
      const filteredStocks = allStocks.filter(stock => 
        stock.symbol.toLowerCase().includes(query.toLowerCase()) ||
        stock.name.toLowerCase().includes(query.toLowerCase())
      );
      
      set({
        stocks: filteredStocks,
        total: filteredStocks.length,
        isLoading: false
      });
    } catch (error) {
      set({ 
        error: '搜索股票失败', 
        isLoading: false 
      });
      console.error('Search stocks failed:', error);
    }
  },

  // 添加到关注列表
  addToWatchlist: (symbol: string) => {
    const { watchlist } = get();
    if (!watchlist.includes(symbol)) {
      set({ watchlist: [...watchlist, symbol] });
    }
  },

  // 从关注列表移除
  removeFromWatchlist: (symbol: string) => {
    const { watchlist } = get();
    set({ watchlist: watchlist.filter(s => s !== symbol) });
  },

  // 设置筛选条件
  setFilters: (filters: { sector?: string; industry?: string }) => {
    set((state) => ({
      ...state,
      ...filters
    }));
  },

  // 清除筛选条件
  clearFilters: () => {
    set({ sectorFilter: '', industryFilter: '' });
  },

  // 设置加载状态
  setLoading: (loading: boolean) => {
    set({ isLoading: loading });
  },

  // 设置错误信息
  setError: (error: string | null) => {
    set({ error });
  }
})); 