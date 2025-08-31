import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { ConfigProvider } from 'antd';
import zhCN from 'antd/locale/zh_CN';
import MainLayout from './components/layout/MainLayout';
import ErrorBoundary from './components/common/ErrorBoundary';
import { generateAllRoutes } from './router/routes';
import './App.scss';

function App() {
  return (
    <ErrorBoundary>
      <ConfigProvider locale={zhCN}>
        <Router>
          <Routes>
            <Route path="/" element={<Navigate to="/dashboard" replace />} />
            {generateAllRoutes().map(route => (
              <Route
                key={route.props.path}
                path={route.props.path}
                element={
                  <MainLayout>
                    {route.props.element}
                  </MainLayout>
                }
              />
            ))}
            

          </Routes>
        </Router>
      </ConfigProvider>
    </ErrorBoundary>
  );
}

export default App;
