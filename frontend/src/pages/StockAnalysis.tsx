import React from 'react';
import { Card, Typography, Row, Col, Statistic, Progress, Table } from 'antd';
import { StockOutlined, RiseOutlined, FallOutlined } from '@ant-design/icons';

const { Title } = Typography;

const StockAnalysis: React.FC = () => {
  return (
    <div>
      <Title level={2}>股票深度分析</Title>
      
      <Row gutter={[16, 16]} style={{ marginBottom: 24 }}>
        <Col span={6}>
          <Card>
            <Statistic
              title="当前价格"
              value={45.67}
              precision={2}
              prefix="¥"
              valueStyle={{ color: '#52c41a' }}
            />
          </Card>
        </Col>
        <Col span={6}>
          <Card>
            <Statistic
              title="涨跌幅"
              value={2.45}
              precision={2}
              prefix={<RiseOutlined />}
              suffix="%"
              valueStyle={{ color: '#52c41a' }}
            />
          </Card>
        </Col>
        <Col span={6}>
          <Card>
            <Statistic
              title="成交量"
              value={1234.56}
              precision={2}
              suffix="万手"
            />
          </Card>
        </Col>
        <Col span={6}>
          <Card>
            <Statistic
              title="换手率"
              value={3.45}
              precision={2}
              suffix="%"
            />
          </Card>
        </Col>
      </Row>

      <Card title="技术分析">
        <Row gutter={[16, 16]}>
          <Col span={12}>
            <h4>技术指标</h4>
            <div style={{ marginBottom: 16 }}>
              <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: 8 }}>
                <span>RSI</span>
                <span>65.4</span>
              </div>
              <Progress percent={65} strokeColor="#1890ff" />
            </div>
            <div style={{ marginBottom: 16 }}>
              <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: 8 }}>
                <span>MACD</span>
                <span>金叉</span>
              </div>
              <Progress percent={70} strokeColor="#52c41a" />
            </div>
          </Col>
          <Col span={12}>
            <h4>支撑阻力位</h4>
            <p>支撑位：42.50</p>
            <p>阻力位：48.00</p>
            <p>目标价：50.00</p>
          </Col>
        </Row>
      </Card>
    </div>
  );
};

export default StockAnalysis; 