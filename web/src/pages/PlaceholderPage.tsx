import React from 'react';
import { Card, Typography, Button } from 'antd';
import { useNavigate } from 'react-router-dom';

const { Title, Paragraph } = Typography;

interface PlaceholderPageProps {
  title: string;
  description?: string;
}

const PlaceholderPage: React.FC<PlaceholderPageProps> = ({ title, description = '此页面正在开发中...' }) => {
  const navigate = useNavigate();

  return (
    <div style={{ textAlign: 'center', padding: '60px 20px' }}>
      <Title level={2}>{title}</Title>
      <Paragraph style={{ fontSize: '16px', marginBottom: '30px' }}>
        {description}
      </Paragraph>
      <Button type="primary" onClick={() => navigate('/dashboard')}>
        返回首页
      </Button>
    </div>
  );
};

export default PlaceholderPage; 