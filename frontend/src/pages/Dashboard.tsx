import React, { useState } from 'react';
import { 
  Card, 
  Form, 
  Input, 
  Select, 
  Button, 
  Row, 
  Col, 
  Badge, 
  Typography, 
  Space,
  Divider,
  List,
  Progress,
  Alert,
  Spin
} from 'antd';
import { 
  SearchOutlined, 
  RiseOutlined, 
  FallOutlined,
  CheckCircleOutlined,
  CloseCircleOutlined,
  ExclamationCircleOutlined
} from '@ant-design/icons';

const { Title, Text } = Typography;
const { Option } = Select;

interface StockAnalysis {
  stockCode: string;
  stockName: string;
  currentPrice: number;
  priceChange: number;
  priceChangePercent: number;
  totalScore: number;
  recommendation: string;
  technicalIndicators: {
    rsi: number;
    maTrend: string;
    macdSignal: string;
    volatility: number;
  };
  fundamentalMetrics: {
    pe: number;
    pb: number;
    roe: number;
    debtRatio: number;
  };
}

const Dashboard: React.FC = () => {
  const [form] = Form.useForm();
  const [loading, setLoading] = useState(false);
  const [analysisResult, setAnalysisResult] = useState<StockAnalysis | null>(null);
  const [showResult, setShowResult] = useState(false);

  const handleAnalysis = async (values: any) => {
    setLoading(true);
    try {
      // 模拟API调用
      await new Promise(resolve => setTimeout(resolve, 2000));
      
      // 模拟分析结果
      const mockResult: StockAnalysis = {
        stockCode: values.stockCode,
        stockName: '贵州茅台',
        currentPrice: 1688.00,
        priceChange: 12.50,
        priceChangePercent: 0.75,
        totalScore: 85,
        recommendation: '强烈推荐',
        technicalIndicators: {
          rsi: 65.2,
          maTrend: '上升趋势',
          macdSignal: '买入信号',
          volatility: 0.18
        },
        fundamentalMetrics: {
          pe: 28.5,
          pb: 12.3,
          roe: 25.8,
          debtRatio: 0.15
        }
      };
      
      setAnalysisResult(mockResult);
      setShowResult(true);
    } catch (error) {
      console.error('分析失败:', error);
    } finally {
      setLoading(false);
    }
  };

  const getScoreColor = (score: number) => {
    if (score >= 80) return '#52c41a';
    if (score >= 60) return '#1890ff';
    if (score >= 40) return '#faad14';
    return '#ff4d4f';
  };

  const getTrendIcon = (trend: string) => {
    if (trend.includes('上升') || trend.includes('买入')) {
      return <RiseOutlined style={{ color: '#52c41a' }} />;
    }
    if (trend.includes('下降') || trend.includes('卖出')) {
      return <FallOutlined style={{ color: '#ff4d4f' }} />;
    }
    return <ExclamationCircleOutlined style={{ color: '#faad14' }} />;
  };

  const getRecommendationIcon = (recommendation: string) => {
    if (recommendation.includes('推荐')) {
      return <CheckCircleOutlined style={{ color: '#52c41a' }} />;
    }
    if (recommendation.includes('谨慎') || recommendation.includes('卖出')) {
      return <CloseCircleOutlined style={{ color: '#ff4d4f' }} />;
    }
    return <ExclamationCircleOutlined style={{ color: '#faad14' }} />;
  };

  // 图表数据
  const priceChartData = [
    { date: '2024-01', price: 1600 },
    { date: '2024-02', price: 1650 },
    { date: '2024-03', price: 1688 },
  ];

  const radarChartData = [
    { indicator: '技术面', value: 85 },
    { indicator: '基本面', value: 90 },
    { indicator: '资金面', value: 75 },
    { indicator: '情绪面', value: 80 },
    { indicator: '风险面', value: 70 },
  ];

  return (
    <div style={{ padding: '24px' }}>
      <Title level={2}>智能股票分析</Title>
      
      {/* 分析表单 */}
      <Card style={{ marginBottom: '24px' }}>
        <Form
          form={form}
          layout="inline"
          onFinish={handleAnalysis}
          style={{ alignItems: 'center' }}
        >
          <Form.Item
            name="stockCode"
            rules={[{ required: true, message: '请输入股票代码' }]}
          >
            <Input
              placeholder="例如: 600519"
              style={{ width: 150 }}
              prefix={<SearchOutlined />}
            />
          </Form.Item>
          
          <Form.Item name="marketType" initialValue="A">
            <Select style={{ width: 100 }}>
              <Option value="A">A股</Option>
              <Option value="HK">港股</Option>
              <Option value="US">美股</Option>
            </Select>
          </Form.Item>
          
          <Form.Item name="analysisPeriod" initialValue="1y">
            <Select style={{ width: 120 }}>
              <Option value="1m">1个月</Option>
              <Option value="3m">3个月</Option>
              <Option value="6m">6个月</Option>
              <Option value="1y">1年</Option>
            </Select>
          </Form.Item>
          
          <Form.Item>
            <Button 
              type="primary" 
              htmlType="submit" 
              loading={loading}
              icon={<SearchOutlined />}
            >
              分析
            </Button>
          </Form.Item>
        </Form>
      </Card>

      {/* 分析结果 */}
      {showResult && analysisResult && (
        <div>
          <Row gutter={[24, 24]}>
            {/* 股票概要 */}
            <Col span={12}>
              <Card title="股票概要">
                <Row gutter={16}>
                  <Col span={14}>
                    <Title level={3} style={{ margin: 0 }}>
                      {analysisResult.stockName}
                    </Title>
                    <Text type="secondary">
                      {analysisResult.stockCode}
                    </Text>
                  </Col>
                  <Col span={10} style={{ textAlign: 'right' }}>
                    <Title level={3} style={{ margin: 0, color: '#1890ff' }}>
                      ¥{analysisResult.currentPrice.toFixed(2)}
                    </Title>
                    <Space>
                      {analysisResult.priceChange > 0 ? (
                        <RiseOutlined style={{ color: '#52c41a' }} />
                      ) : (
                        <FallOutlined style={{ color: '#ff4d4f' }} />
                      )}
                      <Text 
                        type={analysisResult.priceChange > 0 ? 'success' : 'danger'}
                      >
                        {analysisResult.priceChange > 0 ? '+' : ''}
                        {analysisResult.priceChange.toFixed(2)} 
                        ({analysisResult.priceChangePercent.toFixed(2)}%)
                      </Text>
                    </Space>
                  </Col>
                </Row>
                
                <Divider />
                
                <Row gutter={16}>
                  <Col span={12}>
                    <div style={{ marginBottom: '16px' }}>
                      <Text type="secondary">综合评分:</Text>
                      <div style={{ marginTop: '8px' }}>
                        <Badge
                          count={analysisResult.totalScore}
                          style={{
                            backgroundColor: getScoreColor(analysisResult.totalScore),
                            fontSize: '18px',
                            padding: '8px 16px',
                            borderRadius: '20px'
                          }}
                        />
                      </div>
                    </div>
                    
                    <div>
                      <Text type="secondary">投资建议:</Text>
                      <div style={{ marginTop: '8px' }}>
                        <Space>
                          {getRecommendationIcon(analysisResult.recommendation)}
                          <Text strong>{analysisResult.recommendation}</Text>
                        </Space>
                      </div>
                    </div>
                  </Col>
                  
                  <Col span={12}>
                    <Text type="secondary">技术面指标:</Text>
                    <List
                      size="small"
                      dataSource={[
                        { label: 'RSI', value: analysisResult.technicalIndicators.rsi },
                        { label: 'MA趋势', value: analysisResult.technicalIndicators.maTrend },
                        { label: 'MACD信号', value: analysisResult.technicalIndicators.macdSignal },
                        { label: '波动率', value: analysisResult.technicalIndicators.volatility },
                      ]}
                      renderItem={item => (
                                                 <List.Item style={{ padding: '4px 0' }}>
                           <Text type="secondary">{item.label}:</Text>
                           <Space style={{ marginLeft: '8px' }}>
                             {getTrendIcon(String(item.value))}
                             <Text>{item.value}</Text>
                           </Space>
                         </List.Item>
                      )}
                    />
                  </Col>
                </Row>
              </Card>
            </Col>

            {/* 基本面指标 */}
            <Col span={12}>
              <Card title="基本面指标">
                <Row gutter={[16, 16]}>
                  <Col span={12}>
                    <Card size="small">
                      <div style={{ textAlign: 'center' }}>
                        <Title level={4} style={{ margin: 0, color: '#1890ff' }}>
                          {analysisResult.fundamentalMetrics.pe}
                        </Title>
                        <Text type="secondary">市盈率(PE)</Text>
                      </div>
                    </Card>
                  </Col>
                  <Col span={12}>
                    <Card size="small">
                      <div style={{ textAlign: 'center' }}>
                        <Title level={4} style={{ margin: 0, color: '#52c41a' }}>
                          {analysisResult.fundamentalMetrics.pb}
                        </Title>
                        <Text type="secondary">市净率(PB)</Text>
                      </div>
                    </Card>
                  </Col>
                  <Col span={12}>
                    <Card size="small">
                      <div style={{ textAlign: 'center' }}>
                        <Title level={4} style={{ margin: 0, color: '#faad14' }}>
                          {analysisResult.fundamentalMetrics.roe}%
                        </Title>
                        <Text type="secondary">净资产收益率</Text>
                      </div>
                    </Card>
                  </Col>
                  <Col span={12}>
                    <Card size="small">
                      <div style={{ textAlign: 'center' }}>
                        <Title level={4} style={{ margin: 0, color: '#ff4d4f' }}>
                          {analysisResult.fundamentalMetrics.debtRatio}%
                        </Title>
                        <Text type="secondary">资产负债率</Text>
                      </div>
                    </Card>
                  </Col>
                </Row>
              </Card>
            </Col>
          </Row>

          {/* 图表区域 */}
          <Row gutter={[24, 24]} style={{ marginTop: '24px' }}>
            <Col span={12}>
              <Card title="价格走势">
                <div style={{ height: 300, display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
                  <Text type="secondary">图表组件需要安装 @ant-design/plots 包</Text>
                </div>
              </Card>
            </Col>
            <Col span={12}>
              <Card title="综合评分雷达图">
                <div style={{ height: 300, display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
                  <Text type="secondary">图表组件需要安装 @ant-design/plots 包</Text>
                </div>
              </Card>
            </Col>
          </Row>
        </div>
      )}

      {/* 加载状态 */}
      {loading && (
        <div style={{ textAlign: 'center', padding: '50px' }}>
          <Spin size="large" />
          <div style={{ marginTop: '16px' }}>
            <Text>正在分析股票数据，请稍候...</Text>
          </div>
        </div>
      )}
    </div>
  );
};

export default Dashboard; 