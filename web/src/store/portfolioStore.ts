import { create } from 'zustand';
import { persist } from 'zustand/middleware';
import type { Portfolio, PortfolioStock } from '../types';

interface PortfolioState {
  // 状态
  portfolios: Portfolio[];
  currentPortfolio: Portfolio | null;
  isLoading: boolean;
  error: string | null;
  
  // 操作
  createPortfolio: (name: string, description?: string) => Promise<boolean>;
  updatePortfolio: (id: string, updates: Partial<Portfolio>) => Promise<boolean>;
  deletePortfolio: (id: string) => Promise<boolean>;
  selectPortfolio: (id: string) => void;
  
  // 股票操作
  addStock: (portfolioId: string, stock: PortfolioStock) => Promise<boolean>;
  removeStock: (portfolioId: string, stockId: string) => Promise<boolean>;
  updateStockQuantity: (portfolioId: string, stockId: string, quantity: number) => Promise<boolean>;
  
  // 计算
  calculateTotalValue: (portfolioId: string) => number;
  calculateTotalReturn: (portfolioId: string) => number;
  calculateReturnPercent: (portfolioId: string) => number;
  
  // 工具方法
  setLoading: (loading: boolean) => void;
  setError: (error: string | null) => void;
}

export const usePortfolioStore = create<PortfolioState>()(
  persist(
    (set, get) => ({
      // 初始状态
      portfolios: [],
      currentPortfolio: null,
      isLoading: false,
      error: null,

      // 创建投资组合
      createPortfolio: async (name: string, description?: string) => {
        set({ isLoading: true, error: null });
        try {
          // 模拟API调用
          await new Promise(resolve => setTimeout(resolve, 500));
          
          const newPortfolio: Portfolio = {
            id: Date.now().toString(),
            name,
            description: description || '',
            totalValue: 0,
            totalCost: 0,
            totalReturn: 0,
            returnPercent: 0,
            stocks: []
          };
          
          set((state) => ({
            portfolios: [...state.portfolios, newPortfolio],
            currentPortfolio: newPortfolio,
            isLoading: false
          }));
          
          return true;
        } catch (error) {
          set({ 
            error: '创建投资组合失败', 
            isLoading: false 
          });
          console.error('Create portfolio failed:', error);
          return false;
        }
      },

      // 更新投资组合
      updatePortfolio: async (id: string, updates: Partial<Portfolio>) => {
        set({ isLoading: true, error: null });
        try {
          // 模拟API调用
          await new Promise(resolve => setTimeout(resolve, 500));
          
          set((state) => ({
            portfolios: state.portfolios.map(p => 
              p.id === id ? { ...p, ...updates } : p
            ),
            currentPortfolio: state.currentPortfolio?.id === id 
              ? { ...state.currentPortfolio, ...updates }
              : state.currentPortfolio,
            isLoading: false
          }));
          
          return true;
        } catch (error) {
          set({ 
            error: '更新投资组合失败', 
            isLoading: false 
          });
          console.error('Update portfolio failed:', error);
          return false;
        }
      },

      // 删除投资组合
      deletePortfolio: async (id: string) => {
        set({ isLoading: true, error: null });
        try {
          // 模拟API调用
          await new Promise(resolve => setTimeout(resolve, 500));
          
          set((state) => ({
            portfolios: state.portfolios.filter(p => p.id !== id),
            currentPortfolio: state.currentPortfolio?.id === id 
              ? null 
              : state.currentPortfolio,
            isLoading: false
          }));
          
          return true;
        } catch (error) {
          set({ 
            error: '删除投资组合失败', 
            isLoading: false 
          });
          console.error('Delete portfolio failed:', error);
          return false;
        }
      },

      // 选择投资组合
      selectPortfolio: (id: string) => {
        const portfolio = get().portfolios.find(p => p.id === id);
        if (portfolio) {
          set({ currentPortfolio: portfolio });
        }
      },

      // 添加股票
      addStock: async (portfolioId: string, stock: PortfolioStock) => {
        set({ isLoading: true, error: null });
        try {
          // 模拟API调用
          await new Promise(resolve => setTimeout(resolve, 500));
          
          set((state) => {
            const updatedPortfolios = state.portfolios.map(p => {
              if (p.id === portfolioId) {
                const existingStock = p.stocks.find(s => s.stockId === stock.stockId);
                if (existingStock) {
                  // 如果股票已存在，更新数量
                  const updatedStock = {
                    ...existingStock,
                    quantity: existingStock.quantity + stock.quantity,
                    totalCost: existingStock.avgPrice * (existingStock.quantity + stock.quantity),
                    totalValue: stock.currentPrice * (existingStock.quantity + stock.quantity)
                  };
                  
                  const updatedStocks = p.stocks.map(s => 
                    s.stockId === stock.stockId ? updatedStock : s
                  );
                  
                  return { ...p, stocks: updatedStocks };
                } else {
                  // 添加新股票
                  return { ...p, stocks: [...p.stocks, stock] };
                }
              }
              return p;
            });
            
            return { portfolios: updatedPortfolios, isLoading: false };
          });
          
          return true;
        } catch (error) {
          set({ 
            error: '添加股票失败', 
            isLoading: false 
          });
          console.error('Add stock failed:', error);
          return false;
        }
      },

      // 移除股票
      removeStock: async (portfolioId: string, stockId: string) => {
        set({ isLoading: true, error: null });
        try {
          // 模拟API调用
          await new Promise(resolve => setTimeout(resolve, 500));
          
          set((state) => ({
            portfolios: state.portfolios.map(p => 
              p.id === portfolioId 
                ? { ...p, stocks: p.stocks.filter(s => s.stockId !== stockId) }
                : p
            ),
            isLoading: false
          }));
          
          return true;
        } catch (error) {
          set({ 
            error: '移除股票失败', 
            isLoading: false 
          });
          console.error('Remove stock failed:', error);
          return false;
        }
      },

      // 更新股票数量
      updateStockQuantity: async (portfolioId: string, stockId: string, quantity: number) => {
        set({ isLoading: true, error: null });
        try {
          // 模拟API调用
          await new Promise(resolve => setTimeout(resolve, 500));
          
          set((state) => ({
            portfolios: state.portfolios.map(p => {
              if (p.id === portfolioId) {
                const updatedStocks = p.stocks.map(s => {
                  if (s.stockId === stockId) {
                    return {
                      ...s,
                      quantity,
                      totalCost: s.avgPrice * quantity,
                      totalValue: s.currentPrice * quantity
                    };
                  }
                  return s;
                });
                return { ...p, stocks: updatedStocks };
              }
              return p;
            }),
            isLoading: false
          }));
          
          return true;
        } catch (error) {
          set({ 
            error: '更新股票数量失败', 
            isLoading: false 
          });
          console.error('Update stock quantity failed:', error);
          return false;
        }
      },

      // 计算总价值
      calculateTotalValue: (portfolioId: string) => {
        const portfolio = get().portfolios.find(p => p.id === portfolioId);
        if (!portfolio) return 0;
        return portfolio.stocks.reduce((sum, stock) => sum + stock.totalValue, 0);
      },

      // 计算总收益
      calculateTotalReturn: (portfolioId: string) => {
        const portfolio = get().portfolios.find(p => p.id === portfolioId);
        if (!portfolio) return 0;
        return portfolio.stocks.reduce((sum, stock) => sum + stock.return, 0);
      },

      // 计算收益率
      calculateReturnPercent: (portfolioId: string) => {
        const portfolio = get().portfolios.find(p => p.id === portfolioId);
        if (!portfolio) return 0;
        const totalCost = portfolio.stocks.reduce((sum, stock) => sum + stock.totalCost, 0);
        const totalReturn = portfolio.stocks.reduce((sum, stock) => sum + stock.return, 0);
        return totalCost > 0 ? (totalReturn / totalCost) * 100 : 0;
      },

      // 设置加载状态
      setLoading: (loading: boolean) => {
        set({ isLoading: loading });
      },

      // 设置错误信息
      setError: (error: string | null) => {
        set({ error });
      }
    }),
    {
      name: 'portfolio-storage',
      partialize: (state) => ({ 
        portfolios: state.portfolios,
        currentPortfolio: state.currentPortfolio
      })
    }
  )
); 