import React from 'react';
import { Card, Typography, Table, Tag, Button, Space } from 'antd';
import { HeartOutlined, StarOutlined } from '@ant-design/icons';

const { Title } = Typography;

const Watchlist: React.FC = () => {
  const watchlistData = [
    {
      key: '1',
      code: '000001',
      name: '平安银行',
      price: '12.34',
      change: '+2.45%',
      pe: '8.5',
      pb: '0.8',
      sector: '银行'
    },
    {
      key: '2',
      code: '000858',
      name: '五粮液',
      price: '156.78',
      change: '+3.67%',
      pe: '25.6',
      pb: '8.9',
      sector: '白酒'
    },
    {
      key: '3',
      code: '002415',
      name: '海康威视',
      price: '34.56',
      change: '-1.23%',
      pe: '18.9',
      pb: '3.2',
      sector: '科技'
    }
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
    {
      title: '操作',
      key: 'action',
      render: () => (
        <Space>
          <Button type="link" size="small">查看详情</Button>
          <Button type="link" size="small" danger>取消关注</Button>
        </Space>
      ),
    },
  ];

  return (
    <div>
      <Title level={2}>关注列表</Title>
      
      <Card title="我的关注" extra={<Button type="primary" icon={<StarOutlined />}>添加关注</Button>}>
        <Table 
          columns={columns} 
          dataSource={watchlistData} 
          pagination={false}
          size="middle"
        />
      </Card>
    </div>
  );
};

export default Watchlist; 