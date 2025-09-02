import React from 'react';
import { Card, Typography, Table, Tag, DatePicker, Select, Button, Space } from 'antd';
import { FileTextOutlined, SearchOutlined, DownloadOutlined } from '@ant-design/icons';

const { Title } = Typography;
const { RangePicker } = DatePicker;
const { Option } = Select;

const SystemLogs: React.FC = () => {
  const logData = [
    {
      key: '1',
      timestamp: '2024-01-15 10:30:25',
      level: 'INFO',
      module: '用户管理',
      message: '用户登录成功',
      details: '用户ID: 12345, IP: 192.168.1.100'
    },
    {
      key: '2',
      timestamp: '2024-01-15 10:28:15',
      level: 'WARNING',
      module: '数据同步',
      message: '数据同步延迟',
      details: '同步延迟: 5分钟, 影响范围: 市场数据'
    },
    {
      key: '3',
      timestamp: '2024-01-15 10:25:30',
      level: 'ERROR',
      module: 'API服务',
      message: 'API调用失败',
      details: '错误代码: 500, 接口: /api/market/data'
    }
  ];

  const columns = [
    {
      title: '时间',
      dataIndex: 'timestamp',
      key: 'timestamp',
      width: 180
    },
    {
      title: '级别',
      dataIndex: 'level',
      key: 'level',
      width: 100,
      render: (level: string) => {
        let color = 'default';
        if (level === 'ERROR') color = 'error';
        else if (level === 'WARNING') color = 'warning';
        else if (level === 'INFO') color = 'processing';
        
        return <Tag color={color}>{level}</Tag>;
      }
    },
    {
      title: '模块',
      dataIndex: 'module',
      key: 'module',
      width: 120
    },
    {
      title: '消息',
      dataIndex: 'message',
      key: 'message'
    },
    {
      title: '详情',
      dataIndex: 'details',
      key: 'details',
      ellipsis: true
    }
  ];

  return (
    <div>
      <Title level={2}>系统日志</Title>
      
      <Card style={{ marginBottom: 24 }}>
        <Space>
          <RangePicker showTime placeholder={['开始时间', '结束时间']} />
          <Select placeholder="日志级别" style={{ width: 120 }}>
            <Option value="ALL">全部级别</Option>
            <Option value="ERROR">错误</Option>
            <Option value="WARNING">警告</Option>
            <Option value="INFO">信息</Option>
          </Select>
          <Select placeholder="模块" style={{ width: 120 }}>
            <Option value="ALL">全部模块</Option>
            <Option value="用户管理">用户管理</Option>
            <Option value="数据同步">数据同步</Option>
            <Option value="API服务">API服务</Option>
          </Select>
          <Button type="primary" icon={<SearchOutlined />}>
            查询
          </Button>
          <Button icon={<DownloadOutlined />}>
            导出日志
          </Button>
        </Space>
      </Card>

      <Card title="日志列表">
        <Table 
          columns={columns} 
          dataSource={logData} 
          pagination={{ pageSize: 20 }}
          size="middle"
          scroll={{ x: 1000 }}
        />
      </Card>
    </div>
  );
};

export default SystemLogs; 