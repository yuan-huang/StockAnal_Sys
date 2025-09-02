import React from 'react';
import { Card, Row, Col, Typography, Form, Input, Select, Button, Table, Tag } from 'antd';
import { SearchOutlined, FilterOutlined } from '@ant-design/icons';

const { Title } = Typography;
const { Option } = Select;

const StockScreening: React.FC = () => {
  const stockData = [
    { key: '1', code: '000001', name: '平安银行', price: '12.34', change: '+2.45%', pe: '8.5', pb: '0.8', sector: '银行' },
    { key: '2', code: '000002', name: '万科A', price: '18.76', change: '-1.23%', pe: '12.3', pb: '1.2', sector: '房地产' },
    { key: '3', code: '000858', name: '五粮液', price: '156.78', change: '+3.67%', pe: '25.6', pb: '8.9', sector: '白酒' },
  ];

  const columns = [
    { title: '股票代码', dataIndex: 'code', key: 'code' },
    { title: '股票名称', dataIndex: 'name', key: 'name' },
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
    { title: '市盈率', dataIndex: 'pe', key: 'pe' },
    { title: '市净率', dataIndex: 'pb', key: 'pb' },
    { title: '所属板块', dataIndex: 'sector', key: 'sector' },
  ];

  return (
    <div>
      <Title level={2}>股票筛选</Title>
      
      <Card title="筛选条件" style={{ marginBottom: 24 }}>
        <Form layout="inline">
          <Form.Item label="股票代码">
            <Input placeholder="请输入股票代码" style={{ width: 120 }} />
          </Form.Item>
          <Form.Item label="股票名称">
            <Input placeholder="请输入股票名称" style={{ width: 120 }} />
          </Form.Item>
          <Form.Item label="所属板块">
            <Select placeholder="请选择板块" style={{ width: 120 }}>
              <Option value="tech">科技</Option>
              <Option value="finance">金融</Option>
              <Option value="consumer">消费</Option>
              <Option value="energy">新能源</Option>
            </Select>
          </Form.Item>
          <Form.Item label="市盈率">
            <Input placeholder="最小值" style={{ width: 80 }} />
            <span style={{ margin: '0 8px' }}>-</span>
            <Input placeholder="最大值" style={{ width: 80 }} />
          </Form.Item>
          <Form.Item>
            <Button type="primary" icon={<SearchOutlined />}>
              筛选
            </Button>
          </Form.Item>
        </Form>
      </Card>

      <Card title="筛选结果">
        <Table 
          columns={columns} 
          dataSource={stockData} 
          pagination={{ pageSize: 10 }}
          size="middle"
        />
      </Card>
    </div>
  );
};

export default StockScreening; 