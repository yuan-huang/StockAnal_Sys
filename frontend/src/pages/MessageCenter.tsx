import React from 'react';
import { Card, Typography, List, Badge, Tag, Space, Button } from 'antd';
import { MessageOutlined, BellOutlined, FileTextOutlined } from '@ant-design/icons';

const { Title } = Typography;

const MessageCenter: React.FC = () => {
  const messages = [
    {
      id: 1,
      type: 'notification',
      title: '系统维护通知',
      content: '系统将于今晚22:00-24:00进行维护升级',
      time: '2024-01-15 10:30',
      read: false
    },
    {
      id: 2,
      type: 'alert',
      title: '股票价格预警',
      content: '您关注的股票000001平安银行已触发价格预警',
      time: '2024-01-15 09:15',
      read: false
    },
    {
      id: 3,
      type: 'report',
      title: '月度分析报告',
      content: '2024年1月市场分析报告已生成，请查收',
      time: '2024-01-15 08:00',
      read: true
    }
  ];

  const getTypeIcon = (type: string) => {
    switch (type) {
      case 'notification':
        return <BellOutlined style={{ color: '#1890ff' }} />;
      case 'alert':
        return <MessageOutlined style={{ color: '#ff4d4f' }} />;
      case 'report':
        return <FileTextOutlined style={{ color: '#52c41a' }} />;
      default:
        return <MessageOutlined />;
    }
  };

  const getTypeTag = (type: string) => {
    switch (type) {
      case 'notification':
        return <Tag color="blue">系统通知</Tag>;
      case 'alert':
        return <Tag color="red">预警消息</Tag>;
      case 'report':
        return <Tag color="green">分析报告</Tag>;
      default:
        return <Tag>其他</Tag>;
    }
  };

  return (
    <div>
      <Title level={2}>消息中心</Title>
      
      <Space style={{ marginBottom: 16 }}>
        <Button type="primary">全部已读</Button>
        <Button>清空消息</Button>
        <Button>消息设置</Button>
      </Space>

      <Card>
        <List
          itemLayout="horizontal"
          dataSource={messages}
          renderItem={(item) => (
            <List.Item
              actions={[
                <Button type="link" size="small">
                  {item.read ? '已读' : '标记已读'}
                </Button>,
                <Button type="link" size="small">删除</Button>
              ]}
            >
              <List.Item.Meta
                avatar={
                  <Badge dot={!item.read}>
                    {getTypeIcon(item.type)}
                  </Badge>
                }
                title={
                  <Space>
                    <span>{item.title}</span>
                    {getTypeTag(item.type)}
                    <span style={{ color: '#999', fontSize: '12px' }}>{item.time}</span>
                  </Space>
                }
                description={item.content}
              />
            </List.Item>
          )}
        />
      </Card>
    </div>
  );
};

export default MessageCenter; 