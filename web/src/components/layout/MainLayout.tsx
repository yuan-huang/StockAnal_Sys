import React, { useState, useEffect } from 'react';
import { Layout, theme } from 'antd';
import Header from './Header';

const { Content } = Layout;

interface MainLayoutProps {
  children: React.ReactNode;
}

const MainLayout: React.FC<MainLayoutProps> = ({ children }) => {
  const [isDarkTheme, setIsDarkTheme] = useState(false);
  const { token } = theme.useToken();

  useEffect(() => {
    const savedTheme = localStorage.getItem('theme');
    if (savedTheme === 'dark') {
      setIsDarkTheme(true);
      document.documentElement.setAttribute('data-theme', 'dark');
    }
  }, []);

  const handleThemeToggle = () => {
    const newTheme = !isDarkTheme;
    setIsDarkTheme(newTheme);
    if (newTheme) {
      document.documentElement.setAttribute('data-theme', 'dark');
      localStorage.setItem('theme', 'dark');
    } else {
      document.documentElement.removeAttribute('data-theme');
      localStorage.setItem('theme', 'light');
    }
  };

  return (
    <Layout style={{ minHeight: '100vh' }}>
      <Header onThemeToggle={handleThemeToggle} isDarkTheme={isDarkTheme} />
      
      <Layout>
        <Content style={{ 
          padding: '24px', 
          background: isDarkTheme ? '#141414' : '#fafafa',
          transition: 'all 0.3s',
          marginLeft: 0,
        }}>
          <div style={{ 
            background: isDarkTheme ? '#1f1f1f' : '#fff', 
            borderRadius: '8px', 
            boxShadow: '0 1px 2px 0 rgba(0, 0, 0, 0.03)', 
            padding: '24px', 
            minHeight: 'calc(100vh - 120px)',
            transition: 'all 0.3s'
          }}>
            {children}
          </div>
        </Content>
      </Layout>
    </Layout>
  );
};

export default MainLayout; 