import React from 'react';
import { Card, Typography, Row, Col, Statistic, Alert, List, Tag } from 'antd';
import { RobotOutlined, MonitorOutlined, SafetyOutlined } from '@ant-design/icons';

const { Title } = Typography;

const AiMonitor: React.FC = () => {
  const alerts = [
    {
      id: 1,
      type: 'warning',
      message: '股票000001平安银行价格突破预警线',
      time: '10:30:25',
      level: '中'
    },
    {
      id: 2,
      type: 'error',
      message: '检测到异常交易模式',
      time: '10:28:15',
      level: '高'
    },
    {
      id: 3,
      type: 'info',
      message: '市场情绪指数上升',
      time: '10:25:30',
      level: '低'
    }
  ];

  const getAlertIcon = (type: string) => {
    switch (type) {
      case 'warning': return <SafetyOutlined style={{ color: '#faad14' }} />;
      case 'error': return <SafetyOutlined style={{ color: '#ff4d4f' }} />;
      case 'info': return <MonitorOutlined style={{ color: '#1890ff' }} />;
      default: return <MonitorOutlined />;
    }
  };

  const getLevelColor = (level: string) => {
    switch (level) {
      case '高': return 'red';
      case '中': return 'orange';
      case '低': return 'green';
      default: return 'default';
    }
  };

  return (
    <div>
      <Title level={2}>AI盯盘</Title>
      
      <Row gutter={[16, 16]} style={{ marginBottom: 24 }}>
        <Col span={6}>
          <Card>
            <Statistic
              title="监控股票"
              value={156}
              prefix={<MonitorOutlined />}
              suffix="只"
            />
          </Card>
        </Col>
        <Col span={6}>
          <Card>
            <Statistic
              title="今日预警"
              value={12}
              prefix={<SafetyOutlined />}
              suffix="条"
            />
          </Card>
        </Col>
        <Col span={6}>
          <Card>
            <Statistic
              title="AI准确率"
              value={94.5}
              precision={1}
              prefix={<RobotOutlined />}
              suffix="%"
            />
          </Card>
        </Col>
        <Col span={6}>
          <Card>
            <Statistic
              title="运行状态"
              value="正常"
              valueStyle={{ color: '#52c41a' }}
            />
          </Card>
        </Col>
      </Row>

      <Card title="实时预警" style={{ marginBottom: 24 }}>
        <List
          itemLayout="horizontal"
          dataSource={alerts}
          renderItem={(item) => (
            <List.Item>
              <List.Item.Meta
                avatar={getAlertIcon(item.type)}
                title={
                  <div>
                    <span>{item.message}</span>
                    <Tag color={getLevelColor(item.level)} style={{ marginLeft: 8 }}>
                      风险等级: {item.level}
                    </Tag>
                  </div>
                }
                description={`时间: ${item.time}`}
              />
            </List.Item>
          )}
        />
      </Card>

      <Row gutter={[16, 16]}>
        <Col span={12}>
          <Card title="AI分析结果">
            <p>• 市场整体情绪：乐观</p>
            <p>• 主要风险：科技股估值偏高</p>
            <p>• 投资建议：关注低估值蓝筹股</p>
          </Card>
        </Col>
        <Col span={12}>
          <Card title="监控配置">
            <p>• 预警阈值：±5%</p>
            <p>• 监控频率：实时</p>
            <p>• 通知方式：邮件+短信</p>
          </Card>
        </Col>
      </Row>
    </div>
  );
};

export default AiMonitor; 