import React from 'react';
import { Card, Row, Col, Typography, Progress, Statistic } from 'antd';
import { LineChartOutlined, RiseOutlined, FallOutlined } from '@ant-design/icons';

const { Title } = Typography;

const MarketTrends: React.FC = () => {
  return (
    <div>
      <Title level={2}>市场趋势分析</Title>
      
      <Row gutter={[16, 16]} style={{ marginBottom: 24 }}>
        <Col span={8}>
          <Card>
            <Statistic
              title="上涨股票数量"
              value={1234}
              prefix={<RiseOutlined style={{ color: '#52c41a' }} />}
              suffix="只"
            />
          </Card>
        </Col>
        <Col span={8}>
          <Card>
            <Statistic
              title="下跌股票数量"
              value={876}
              prefix={<FallOutlined style={{ color: '#ff4d4f' }} />}
              suffix="只"
            />
          </Card>
        </Col>
        <Col span={8}>
          <Card>
            <Statistic
              title="平盘股票数量"
              value={234}
              prefix={<LineChartOutlined />}
              suffix="只"
            />
          </Card>
        </Col>
      </Row>

      <Row gutter={[16, 16]} style={{ marginBottom: 24 }}>
        <Col span={12}>
          <Card title="市场强度分析">
            <div style={{ padding: '16px 0' }}>
              <div style={{ marginBottom: 16 }}>
                <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: 8 }}>
                  <span>多头强度</span>
                  <span>75%</span>
                </div>
                <Progress percent={75} strokeColor="#52c41a" />
              </div>
              <div style={{ marginBottom: 16 }}>
                <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: 8 }}>
                  <span>空头强度</span>
                  <span>25%</span>
                </div>
                <Progress percent={25} strokeColor="#ff4d4f" />
              </div>
              <div>
                <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: 8 }}>
                  <span>市场情绪</span>
                  <span>乐观</span>
                </div>
                <Progress percent={80} strokeColor="#1890ff" />
              </div>
            </div>
          </Card>
        </Col>
        <Col span={12}>
          <Card title="技术指标">
            <div style={{ padding: '16px 0' }}>
              <div style={{ marginBottom: 16 }}>
                <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: 8 }}>
                  <span>RSI指标</span>
                  <span>65.4</span>
                </div>
                <Progress percent={65} strokeColor="#1890ff" />
              </div>
              <div style={{ marginBottom: 16 }}>
                <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: 8 }}>
                  <span>MACD指标</span>
                  <span>金叉</span>
                </div>
                <Progress percent={70} strokeColor="#52c41a" />
              </div>
              <div>
                <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: 8 }}>
                  <span>KDJ指标</span>
                  <span>超买</span>
                </div>
                <Progress percent={85} strokeColor="#faad14" />
              </div>
            </div>
          </Card>
        </Col>
      </Row>

      <Card title="趋势预测">
        <div style={{ marginBottom: 16 }}>
          基于当前市场数据分析，预计短期内市场将呈现震荡上行趋势。主要支撑位在3100点附近，
          阻力位在3200点附近。建议投资者关注科技、新能源等板块的投资机会。
        </div>
        <Row gutter={[16, 16]}>
          <Col span={6}>
            <Card size="small" title="短期趋势">
              <div style={{ textAlign: 'center', color: '#52c41a' }}>
                <RiseOutlined style={{ fontSize: 24 }} />
                <div>看涨</div>
              </div>
            </Card>
          </Col>
          <Col span={6}>
            <Card size="small" title="中期趋势">
              <div style={{ textAlign: 'center', color: '#1890ff' }}>
                <LineChartOutlined style={{ fontSize: 24 }} />
                <div>震荡</div>
              </div>
            </Card>
          </Col>
          <Col span={6}>
            <Card size="small" title="长期趋势">
              <div style={{ textAlign: 'center', color: '#52c41a' }}>
                <RiseOutlined style={{ fontSize: 24 }} />
                <div>看涨</div>
              </div>
            </Card>
          </Col>
          <Col span={6}>
            <Card size="small" title="风险等级">
              <div style={{ textAlign: 'center', color: '#faad14' }}>
                <div style={{ fontSize: 24 }}>⚠️</div>
                <div>中等</div>
              </div>
            </Card>
          </Col>
        </Row>
      </Card>
    </div>
  );
};

export default MarketTrends; 