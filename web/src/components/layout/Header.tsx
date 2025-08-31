import React, { useState } from 'react';
import { Layout, Button, Avatar, Dropdown, Input, Space, Badge } from 'antd';
import { 
  UserOutlined, 
  SettingOutlined, 
  LogoutOutlined, 
  SearchOutlined,
  MoonOutlined,
  SunOutlined
} from '@ant-design/icons';
import { useNavigate, useLocation } from 'react-router-dom';
import { 
  mainMenuItems, 
  adminMenuItems, 
  userMenuItems,
  findParentMenuByPath 
} from '../../router/menuConfig';

const { Header: AntHeader } = Layout;
const { Search } = Input;

interface HeaderProps {
  onThemeToggle: () => void;
  isDarkTheme: boolean;
}

const Header: React.FC<HeaderProps> = ({ onThemeToggle, isDarkTheme }) => {
  const navigate = useNavigate();
  const location = useLocation();
  const [searchValue, setSearchValue] = useState('');
  const [selectedMainMenu, setSelectedMainMenu] = useState<string | null>(null);



  const handleMenuClick = (key: string) => {
    if (key === 'logout') {
      // 处理退出登录逻辑
      navigate('/login');
    } else if (key.startsWith('/')) {
      // 检查是否是一级菜单
      const mainMenuItem = mainMenuItems.find(item => item.key === key);
      if (mainMenuItem && mainMenuItem.children && mainMenuItem.children.length > 0) {
        // 如果是一级菜单且有子菜单，只设置选中状态，不跳转
        setSelectedMainMenu(key);
      } else {
        // 如果是没有子菜单的菜单项，才跳转
        setSelectedMainMenu(null);
        navigate(key);
      }
    }
  };

  const handleSearch = (value: string) => {
    if (value.trim()) {
      navigate(`/stock_detail/${value.trim()}`);
    }
  };

  const isAdmin = true; // 这里应该从用户状态或权限系统获取

  // 获取当前选中一级菜单的子菜单
  const getCurrentSubMenu = () => {
    if (!selectedMainMenu) return null;
    const menuItem = mainMenuItems.find(item => item.key === selectedMainMenu);
    return menuItem?.children || null;
  };

  const currentSubMenu = getCurrentSubMenu();

  // 根据当前路径自动设置选中的一级菜单
  React.useEffect(() => {
    const currentPath = location.pathname;
    const parentMenu = findParentMenuByPath(currentPath);
    
    if (parentMenu) {
      setSelectedMainMenu(parentMenu.key);
    } else {
      // 检查是否是一级菜单本身
      const isMainMenu = mainMenuItems.some(item => item.key === currentPath);
      if (isMainMenu) {
        setSelectedMainMenu(currentPath);
      } else {
        setSelectedMainMenu(null);
      }
    }
  }, [location.pathname]);

  return (
    <>
      <AntHeader style={{ 
        background: '#1890ff', 
        borderBottom: '1px solid #f0f0f0', 
        padding: '0 24px', 
        display: 'flex', 
        alignItems: 'center', 
        justifyContent: 'space-between',
        position: 'relative',
        zIndex: 1001,
      }}>
        <div style={{ display: 'flex', alignItems: 'center' }}>
          <h1 style={{ 
            fontSize: '20px', 
            fontWeight: 'bold', 
            color: '#fff', 
            marginRight: '32px',
            margin: 0
          }}>
            <span style={{ marginRight: 8, fontSize: '24px' }}>💡</span>
            FinCore AI
          </h1>
          
          {/* 一级菜单 */}
          <div style={{ display: 'flex', alignItems: 'center' }}>
            {mainMenuItems.map((item) => (
              <div
                key={item.key}
                className="menu-item"
                onClick={() => {
                  if (item.children && item.children.length > 0) {
                    // 如果是一级菜单且有子菜单，只设置选中状态，不跳转
                    setSelectedMainMenu(item.key);
                  } else {
                    // 如果没有子菜单，直接跳转
                    handleMenuClick(item.key);
                  }
                }}
                style={{
                  display: 'flex',
                  alignItems: 'center',
                  gap: '6px',
                  padding: '12px 16px',
                  borderRadius: '6px',
                  cursor: 'pointer',
                  color: '#fff',
                  fontWeight: selectedMainMenu === item.key ? '600' : '400',
                  backgroundColor: selectedMainMenu === item.key ? 'rgba(255, 255, 255, 0.2)' : 'transparent',
                  transition: 'all 0.2s',
                  fontSize: '14px',
                  whiteSpace: 'nowrap',
                  position: 'relative',
                }}
                onMouseEnter={(e) => {
                  if (selectedMainMenu !== item.key) {
                    e.currentTarget.style.backgroundColor = 'rgba(255, 255, 255, 0.1)';
                  }
                }}
                onMouseLeave={(e) => {
                  if (selectedMainMenu !== item.key) {
                    e.currentTarget.style.backgroundColor = 'transparent';
                  }
                }}
              >
                {item.icon}
                <span>{item.label}</span>
                {item.children && item.children.length > 0 && (
                  <div 
                    className="submenu-dropdown"
                    style={{
                      position: 'absolute',
                      top: '100%',
                      left: '0',
                      right: '0',
                      background: '#fff',
                      border: '1px solid #f0f0f0',
                      borderRadius: '6px',
                      boxShadow: '0 4px 12px rgba(0, 0, 0, 0.15)',
                      padding: '8px 0',
                      marginTop: '4px',
                      opacity: 0,
                      visibility: 'hidden',
                      transform: 'translateY(-10px)',
                      transition: 'all 0.2s ease',
                      zIndex: 1002,
                      minWidth: '160px',
                    }}
                  >
                    {item.children.map((child) => (
                      <div
                        key={child.key}
                        onClick={(e) => {
                          e.stopPropagation();
                          handleMenuClick(child.key);
                        }}
                        style={{
                          display: 'flex',
                          alignItems: 'center',
                          gap: '8px',
                          padding: '8px 16px',
                          cursor: 'pointer',
                          color: '#333',
                          fontSize: '13px',
                          transition: 'all 0.2s',
                        }}
                        onMouseEnter={(e) => {
                          e.currentTarget.style.backgroundColor = '#f5f5f5';
                        }}
                        onMouseLeave={(e) => {
                          e.currentTarget.style.backgroundColor = 'transparent';
                        }}
                      >
                        {child.icon}
                        <span>{child.label}</span>
                      </div>
                    ))}
                  </div>
                )}
              </div>
            ))}
            
            {/* 管理员菜单 */}
            {isAdmin && (
              <div style={{ marginLeft: '16px', display: 'flex', alignItems: 'center' }}>
                {adminMenuItems.map((item) => (
                  <div
                    key={item.key}
                    onClick={() => handleMenuClick(item.key)}
                    style={{
                      display: 'flex',
                      alignItems: 'center',
                      gap: '6px',
                      padding: '12px 16px',
                      borderRadius: '6px',
                      cursor: 'pointer',
                      color: '#fff',
                      fontWeight: '400',
                      transition: 'all 0.2s',
                      fontSize: '14px',
                      whiteSpace: 'nowrap',
                    }}
                    onMouseEnter={(e) => {
                      e.currentTarget.style.backgroundColor = 'rgba(255, 255, 255, 0.1)';
                    }}
                    onMouseLeave={(e) => {
                      e.currentTarget.style.backgroundColor = 'transparent';
                    }}
                  >
                    {item.icon}
                    <span>{item.label}</span>
                  </div>
                ))}
              </div>
            )}
          </div>
        </div>
        
        <div style={{ display: 'flex', alignItems: 'center', gap: '16px' }}>
          <Button 
            type="text" 
            icon={isDarkTheme ? <SunOutlined /> : <MoonOutlined />}
            onClick={onThemeToggle}
            style={{ color: '#fff' }}
          />
          
          <Search
            placeholder="搜索股票代码/名称"
            allowClear
            enterButton={<SearchOutlined />}
            size="middle"
            style={{ width: 250 }}
            value={searchValue}
            onChange={(e) => setSearchValue(e.target.value)}
            onSearch={handleSearch}
          />
          
          {isAdmin ? (
            <Dropdown
              menu={{
                items: userMenuItems,
                onClick: ({ key }) => handleMenuClick(key),
              }}
              placement="bottomRight"
            >
              <Avatar 
                icon={<UserOutlined />} 
                style={{ cursor: 'pointer', backgroundColor: '#fff', color: '#1890ff' }} 
              />
            </Dropdown>
          ) : (
            <Button 
              type="default" 
              icon={<UserOutlined />}
              onClick={() => navigate('/login')}
              style={{ color: '#1890ff', borderColor: '#fff', backgroundColor: '#fff' }}
            >
              登录
            </Button>
          )}
        </div>
      </AntHeader>

      {/* 二级菜单 - 只在选中一级菜单后显示 */}
      {currentSubMenu && currentSubMenu.length > 0 && (
        <div 
          style={{
            background: '#fff',
            borderBottom: '1px solid #f0f0f0',
            padding: '12px 24px',
            position: 'sticky',
            top: 64,
            zIndex: 1000,
            boxShadow: '0 2px 8px rgba(0, 0, 0, 0.1)',
          }}
        >
          <div style={{ 
            display: 'flex', 
            gap: '24px', 
            alignItems: 'center',
            maxWidth: '1400px',
            margin: '0 auto',
            flexWrap: 'wrap',
            justifyContent: 'flex-start'
          }}>
            {currentSubMenu.map((item) => (
              <div
                key={item.key}
                onClick={() => navigate(item.key)}
                style={{
                  display: 'flex',
                  alignItems: 'center',
                  gap: '6px',
                  padding: '8px 16px',
                  borderRadius: '6px',
                  cursor: 'pointer',
                  color: location.pathname === item.key ? '#1890ff' : '#666',
                  fontWeight: location.pathname === item.key ? '500' : 'normal',
                  backgroundColor: location.pathname === item.key ? '#f0f8ff' : 'transparent',
                  transition: 'all 0.2s',
                  fontSize: '14px',
                  whiteSpace: 'nowrap',
                  border: location.pathname === item.key ? '1px solid #d6e4ff' : '1px solid transparent',
                }}
                onMouseEnter={(e) => {
                  if (location.pathname !== item.key) {
                    e.currentTarget.style.backgroundColor = '#f5f5f5';
                    e.currentTarget.style.transform = 'translateY(-1px)';
                  }
                }}
                onMouseLeave={(e) => {
                  if (location.pathname !== item.key) {
                    e.currentTarget.style.backgroundColor = 'transparent';
                    e.currentTarget.style.transform = 'translateY(0)';
                  }
                }}
              >
                {item.icon}
                <span>{item.label}</span>
              </div>
            ))}
          </div>
        </div>
      )}
    </>
  );
};

// 添加CSS样式来实现子菜单悬停效果
const styles = `
  .submenu-dropdown {
    opacity: 0;
    visibility: hidden;
    transform: translateY(-10px);
    transition: all 0.2s ease;
    pointer-events: none;
  }
  
  .menu-item:hover .submenu-dropdown {
    opacity: 1;
    visibility: visible;
    transform: translateY(0);
    pointer-events: auto;
  }
`;

// 动态添加样式到页面
if (typeof document !== 'undefined') {
  const styleElement = document.createElement('style');
  styleElement.textContent = styles;
  document.head.appendChild(styleElement);
}

export default Header; 