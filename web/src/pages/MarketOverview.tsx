import React from 'react';
import { Card, Row, Col, Statistic, Table, Typography } from 'antd';
import { ArrowUpOutlined, ArrowDownOutlined } from '@ant-design/icons';

const { Title } = Typography;

const MarketOverview: React.FC = () => {
  const marketData = [
    { key: '1', index: '上证指数', price: '3,123.45', change: '+1.23%', volume: '2,345.67亿' },
    { key: '2', index: '深证成指', price: '10,234.56', change: '-0.87%', volume: '1,876.54亿' },
    { key: '3', index: '创业板指', price: '2,345.67', change: '+2.15%', volume: '987.65亿' },
  ];

  const columns = [
    { title: '指数名称', dataIndex: 'index', key: 'index' },
    { title: '最新价', dataIndex: 'price', key: 'price' },
    { 
      title: '涨跌幅', 
      dataIndex: 'change', 
      key: 'change',
      render: (change: string) => (
        <span style={{ color: change.startsWith('+') ? '#52c41a' : '#ff4d4f' }}>
          {change}
        </span>
      )
    },
    { title: '成交量', dataIndex: 'volume', key: 'volume' },
  ];

  return (
    <div>
      <Title level={2}>市场概览</Title>
      
      <Row gutter={[16, 16]} style={{ marginBottom: 24 }}>
        <Col span={6}>
          <Card>
            <Statistic
              title="上证指数"
              value={3123.45}
              precision={2}
              valueStyle={{ color: '#3f8600' }}
              prefix={<ArrowUpOutlined />}
              suffix="点"
            />
          </Card>
        </Col>
        <Col span={6}>
          <Card>
            <Statistic
              title="深证成指"
              value={10234.56}
              precision={2}
              valueStyle={{ color: '#cf1322' }}
              prefix={<ArrowDownOutlined />}
              suffix="点"
            />
          </Card>
        </Col>
        <Col span={6}>
          <Card>
            <Statistic
              title="创业板指"
              value={2345.67}
              precision={2}
              valueStyle={{ color: '#3f8600' }}
              prefix={<ArrowUpOutlined />}
              suffix="点"
            />
          </Card>
        </Col>
        <Col span={6}>
          <Card>
            <Statistic
              title="北证50"
              value={987.65}
              precision={2}
              valueStyle={{ color: '#3f8600' }}
              prefix={<ArrowUpOutlined />}
              suffix="点"
            />
          </Card>
        </Col>
      </Row>

      <Card title="主要指数行情" style={{ marginBottom: 24 }}>
        <Table 
          columns={columns} 
          dataSource={marketData} 
          pagination={false}
          size="middle"
        />
      </Card>

      <Row gutter={[16, 16]}>
        <Col span={12}>
          <Card title="市场热点">
            <div style={{ padding: '16px 0' }}>
              <p>• 科技股领涨，芯片概念股表现活跃</p>
              <p>• 新能源板块持续走强，光伏概念股大涨</p>
              <p>• 医药板块震荡调整，创新药概念股回调</p>
              <p>• 消费板块企稳回升，白酒概念股反弹</p>
            </div>
          </Card>
        </Col>
        <Col span={12}>
          <Card title="市场情绪">
            <div style={{ padding: '16px 0' }}>
              <p>• 市场情绪指数：65.4 (中性偏乐观)</p>
              <p>• 恐慌贪婪指数：58 (中性)</p>
              <p>• 北向资金：+12.34亿元</p>
              <p>• 融资余额：+23.45亿元</p>
            </div>
          </Card>
        </Col>
      </Row>
    </div>
  );
};

export default MarketOverview; 