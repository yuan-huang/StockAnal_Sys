import React from 'react';
import { Card, Typography, Form, Switch, InputNumber, Button, Row, Col, Input } from 'antd';
import { SettingOutlined } from '@ant-design/icons';

const { Title } = Typography;

const SystemSettings: React.FC = () => {
  return (
    <div>
      <Title level={2}>系统设置</Title>
      
      <Row gutter={[16, 16]}>
        <Col span={12}>
          <Card title="基本设置">
            <Form layout="vertical">
              <Form.Item label="系统名称" name="systemName">
                <Input placeholder="请输入系统名称" />
              </Form.Item>
              <Form.Item label="刷新频率(秒)" name="refreshRate">
                <InputNumber min={1} max={60} defaultValue={5} />
              </Form.Item>
              <Form.Item label="启用通知" name="enableNotification" valuePropName="checked">
                <Switch />
              </Form.Item>
              <Form.Item>
                <Button type="primary">保存设置</Button>
              </Form.Item>
            </Form>
          </Card>
        </Col>
        
        <Col span={12}>
          <Card title="显示设置">
            <Form layout="vertical">
              <Form.Item label="默认主题" name="defaultTheme">
                <Switch checkedChildren="深色" unCheckedChildren="浅色" />
              </Form.Item>
              <Form.Item label="图表颜色" name="chartColors">
                <Input placeholder="请输入图表颜色" />
              </Form.Item>
              <Form.Item label="字体大小" name="fontSize">
                <InputNumber min={12} max={20} defaultValue={14} />
              </Form.Item>
            </Form>
          </Card>
        </Col>
      </Row>
    </div>
  );
};

export default SystemSettings; 