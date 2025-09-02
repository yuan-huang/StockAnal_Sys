import React from 'react';
import { Card, Typography, List, Tag, Button, Space } from 'antd';
import { BulbOutlined, StarOutlined } from '@ant-design/icons';

const { Title } = Typography;

const StockRecommendations: React.FC = () => {
  const recommendations = [
    {
      id: 1,
      code: '000001',
      name: '平安银行',
      reason: '技术面突破，基本面稳健',
      target: '15.00',
      risk: '低',
      confidence: 85
    },
    {
      id: 2,
      code: '000858',
      name: '五粮液',
      reason: '消费复苏，估值合理',
      target: '180.00',
      risk: '中',
      confidence: 78
    },
    {
      id: 3,
      code: '002415',
      name: '海康威视',
      reason: 'AI概念，业绩增长',
      target: '45.00',
      risk: '中',
      confidence: 72
    }
  ];

  const getRiskColor = (risk: string) => {
    switch (risk) {
      case '低': return 'green';
      case '中': return 'orange';
      case '高': return 'red';
      default: return 'default';
    }
  };

  return (
    <div>
      <Title level={2}>推荐股票</Title>
      
      <Card>
        <List
          itemLayout="horizontal"
          dataSource={recommendations}
          renderItem={(item) => (
            <List.Item
              actions={[
                <Button type="primary" size="small">查看详情</Button>,
                <Button size="small" icon={<StarOutlined />}>关注</Button>
              ]}
            >
              <List.Item.Meta
                title={
                  <Space>
                    <span>{item.code} {item.name}</span>
                    <Tag color={getRiskColor(item.risk)}>风险: {item.risk}</Tag>
                    <Tag color="blue">置信度: {item.confidence}%</Tag>
                  </Space>
                }
                description={
                  <div>
                    <p><strong>推荐理由：</strong>{item.reason}</p>
                    <p><strong>目标价：</strong>¥{item.target}</p>
                  </div>
                }
              />
            </List.Item>
          )}
        />
      </Card>
    </div>
  );
};

export default StockRecommendations; 