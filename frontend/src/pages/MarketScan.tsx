import React, { useState } from 'react';
import { 
  Card, 
  Form, 
  Input, 
  Select, 
  Button, 
  Row, 
  Col, 
  Typography, 
  Space,
  Tag,
  Progress,
  Statistic,
  Divider,
  Alert,
  Table,
  Tabs,
  List,
  Avatar,
  Badge
} from 'antd';
import { 
  SearchOutlined, 
  RiseOutlined, 
  FallOutlined,
  DollarOutlined,
  BarChartOutlined,
  LineChartOutlined,
  PieChartOutlined,
  TrendingUpOutlined,
  TrendingDownOutlined,
  FireOutlined,
  StarOutlined,
  WarningOutlined
} from '@ant-design/icons';

const { Title, Text, Paragraph } = Typography;
const { Option } = Select;
const { TabPane } = Tabs;

interface MarketData {
  date: string;
  marketIndex: {
    name: string;
    value: number;
    change: number;
    changePercent: number;
    volume: number;
    turnover: number;
  };
  sectorPerformance: {
    name: string;
    change: number;
    changePercent: number;
    volume: number;
    leadingStocks: string[];
  }[];
  hotStocks: {
    code: string;
    name: string;
    price: number;
    change: number;
    changePercent: number;
    volume: number;
    reason: string;
  }[];
  marketSentiment: {
    bullish: number;
    bearish: number;
    neutral: number;
    fearGreedIndex: number;
  };
  capitalFlow: {
    mainNetInflow: number;
    northboundNetInflow: number;
    institutionalNetInflow: number;
    retailNetInflow: number;
  };
}

const MarketScan: React.FC = () => {
  const [form] = Form.useForm();
  const [loading, setLoading] = useState(false);
  const [marketData, setMarketData] = useState<MarketData | null>(null);
  const [showResult, setShowResult] = useState(false);

  const handleScan = async (values: any) => {
    setLoading(true);
    try {
      // 模拟API调用
      await new Promise(resolve => setTimeout(resolve, 2000));
      
      // 模拟市场扫描数据
      const mockData: MarketData = {
        date: '2024-01-15',
        marketIndex: {
          name: '上证指数',
          value: 3150.25,
          change: 25.50,
          changePercent: 0.82,
          volume: 2.8e11,
          turnover: 3.2e11
        },
        sectorPerformance: [
          {
            name: '白酒',
            change: 2.85,
            changePercent: 3.2,
            volume: 1.2e10,
            leadingStocks: ['贵州茅台', '五粮液', '泸州老窖']
          },
          {
            name: '新能源',
            change: 1.95,
            changePercent: 2.1,
            volume: 8.5e9,
            leadingStocks: ['宁德时代', '比亚迪', '隆基绿能']
          },
          {
            name: '医药',
            change: -0.85,
            changePercent: -0.9,
            volume: 6.8e9,
            leadingStocks: ['恒瑞医药', '迈瑞医疗', '药明康德']
          },
          {
            name: '银行',
            change: 0.45,
            changePercent: 0.5,
            volume: 4.2e9,
            leadingStocks: ['招商银行', '平安银行', '兴业银行']
          }
        ],
        hotStocks: [
          {
            code: '600519',
            name: '贵州茅台',
            price: 1688.00,
            change: 12.50,
            changePercent: 0.75,
            volume: 8.5e7,
            reason: '消费升级+品牌价值提升'
          },
          {
            code: '300750',
            name: '宁德时代',
            price: 185.50,
            change: 8.50,
            changePercent: 4.81,
            volume: 2.1e8,
            reason: '新能源政策利好+业绩超预期'
          },
          {
            code: '000858',
            name: '五粮液',
            price: 168.80,
            change: 5.20,
            changePercent: 3.18,
            volume: 1.8e8,
            reason: '白酒板块轮动+估值修复'
          }
        ],
        marketSentiment: {
          bullish: 65,
          bearish: 20,
          neutral: 15,
          fearGreedIndex: 72
        },
        capitalFlow: {
          mainNetInflow: 15.8e9,
          northboundNetInflow: 8.5e9,
          institutionalNetInflow: 22.3e9,
          retailNetInflow: -12.1e9
        }
      };
      
      setMarketData(mockData);
      setShowResult(true);
    } catch (error) {
      console.error('扫描失败:', error);
    } finally {
      setLoading(false);
    }
  };

  const getChangeColor = (change: number) => {
    return change > 0 ? '#52c41a' : change < 0 ? '#ff4d4f' : '#666';
  };

  const getChangeIcon = (change: number) => {
    return change > 0 ? <RiseOutlined /> : change < 0 ? <FallOutlined /> : null;
  };

  const getSentimentColor = (index: number) => {
    if (index >= 80) return '#52c41a';
    if (index >= 60) return '#1890ff';
    if (index >= 40) return '#faad14';
    return '#ff4d4f';
  };

  const getSentimentText = (index: number) => {
    if (index >= 80) return '极度贪婪';
    if (index >= 60) return '贪婪';
    if (index >= 40) return '中性';
    if (index >= 20) return '恐惧';
    return '极度恐惧';
  };

  const sectorColumns = [
    {
      title: '板块名称',
      dataIndex: 'name',
      key: 'name',
      width: 120,
    },
    {
      title: '涨跌幅',
      dataIndex: 'changePercent',
      key: 'changePercent',
      width: 100,
      render: (changePercent: number) => (
        <Space>
          {getChangeIcon(changePercent)}
          <Text style={{ color: getChangeColor(changePercent) }}>
            {changePercent > 0 ? '+' : ''}{changePercent.toFixed(2)}%
          </Text>
        </Space>
      ),
    },
    {
      title: '成交量(亿)',
      dataIndex: 'volume',
      key: 'volume',
      width: 120,
      render: (volume: number) => (volume / 1e8).toFixed(2),
    },
    {
      title: '领涨股票',
      dataIndex: 'leadingStocks',
      key: 'leadingStocks',
      render: (stocks: string[]) => (
        <Space wrap>
          {stocks.map((stock, index) => (
            <Tag key={index} color="blue">{stock}</Tag>
          ))}
        </Space>
      ),
    },
  ];

  const hotStockColumns = [
    {
      title: '股票代码',
      dataIndex: 'code',
      key: 'code',
      width: 100,
    },
    {
      title: '股票名称',
      dataIndex: 'name',
      key: 'name',
      width: 120,
    },
    {
      title: '当前价格',
      dataIndex: 'price',
      key: 'price',
      width: 100,
      render: (price: number) => `¥${price.toFixed(2)}`,
    },
    {
      title: '涨跌幅',
      dataIndex: 'changePercent',
      key: 'changePercent',
      width: 100,
      render: (changePercent: number) => (
        <Space>
          {getChangeIcon(changePercent)}
          <Text style={{ color: getChangeColor(changePercent) }}>
            {changePercent > 0 ? '+' : ''}{changePercent.toFixed(2)}%
          </Text>
        </Space>
      ),
    },
    {
      title: '成交量(万)',
      dataIndex: 'volume',
      key: 'volume',
      width: 120,
      render: (volume: number) => (volume / 1e4).toFixed(0),
    },
    {
      title: '上涨原因',
      dataIndex: 'reason',
      key: 'reason',
      render: (reason: string) => (
        <Tag color="green" icon={<FireOutlined />}>
          {reason}
        </Tag>
      ),
    },
  ];

  return (
    <div style={{ padding: '24px' }}>
      <Title level={2}>
        <BarChartOutlined style={{ marginRight: 8 }} />
        市场扫描
      </Title>
      <Paragraph type="secondary">
        实时扫描市场动态，包括指数表现、板块轮动、热门股票和市场情绪等关键信息
      </Paragraph>
      
      {/* 扫描表单 */}
      <Card style={{ marginBottom: '24px' }}>
        <Form
          form={form}
          layout="inline"
          onFinish={handleScan}
          style={{ alignItems: 'center' }}
        >
          <Form.Item name="scanType" initialValue="comprehensive">
            <Select style={{ width: 150 }}>
              <Option value="comprehensive">综合扫描</Option>
              <Option value="sector">板块扫描</Option>
              <Option value="hot">热门扫描</Option>
              <Option value="sentiment">情绪扫描</Option>
            </Select>
          </Form.Item>
          
          <Form.Item name="timeRange" initialValue="1d">
            <Select style={{ width: 120 }}>
              <Option value="1d">1日</Option>
              <Option value="3d">3日</Option>
              <Option value="5d">5日</Option>
              <Option value="1w">1周</Option>
            </Select>
          </Form.Item>
          
          <Form.Item>
            <Button 
              type="primary" 
              htmlType="submit" 
              loading={loading}
              icon={<SearchOutlined />}
            >
              开始扫描
            </Button>
          </Form.Item>
        </Form>
      </Card>

      {/* 扫描结果 */}
      {showResult && marketData && (
        <div>
          {/* 市场指数 */}
          <Card title="市场指数概览" style={{ marginBottom: '24px' }}>
            <Row gutter={[24, 24]}>
              <Col span={8}>
                <Card size="small">
                  <Statistic
                    title={marketData.marketIndex.name}
                    value={marketData.marketIndex.value}
                    precision={2}
                    valueStyle={{ color: '#1890ff', fontSize: '24px' }}
                  />
                  <div style={{ marginTop: '8px' }}>
                    <Space>
                      {getChangeIcon(marketData.marketIndex.change)}
                      <Text 
                        type={marketData.marketIndex.change > 0 ? 'success' : 'danger'}
                        style={{ fontSize: '16px' }}
                      >
                        {marketData.marketIndex.change > 0 ? '+' : ''}
                        {marketData.marketIndex.change.toFixed(2)} 
                        ({marketData.marketIndex.changePercent.toFixed(2)}%)
                      </Text>
                    </Space>
                  </div>
                </Card>
              </Col>
              <Col span={8}>
                <Card size="small">
                  <Statistic
                    title="成交量"
                    value={marketData.marketIndex.volume / 1e8}
                    suffix="亿元"
                    precision={2}
                    valueStyle={{ color: '#52c41a' }}
                  />
                </Card>
              </Col>
              <Col span={8}>
                <Card size="small">
                  <Statistic
                    title="成交额"
                    value={marketData.marketIndex.turnover / 1e8}
                    suffix="亿元"
                    precision={2}
                    valueStyle={{ color: '#faad14' }}
                  />
                </Card>
              </Col>
            </Row>
          </Card>

          {/* 板块表现 */}
          <Card title="板块表现" style={{ marginBottom: '24px' }}>
            <Table
              columns={sectorColumns}
              dataSource={marketData.sectorPerformance}
              pagination={false}
              size="small"
              scroll={{ x: 600 }}
            />
          </Card>

          {/* 热门股票 */}
          <Card title="热门股票" style={{ marginBottom: '24px' }}>
            <Table
              columns={hotStockColumns}
              dataSource={marketData.hotStocks}
              pagination={false}
              size="small"
              scroll={{ x: 800 }}
            />
          </Card>

          {/* 市场情绪 */}
          <Row gutter={[24, 24]} style={{ marginBottom: '24px' }}>
            <Col span={12}>
              <Card title="市场情绪分析">
                <Row gutter={[16, 16]}>
                  <Col span={12}>
                    <div style={{ textAlign: 'center' }}>
                      <Progress
                        type="circle"
                        percent={marketData.marketSentiment.bullish}
                        format={percent => `${percent}%`}
                        strokeColor="#52c41a"
                      />
                      <div style={{ marginTop: '8px' }}>
                        <Text strong style={{ color: '#52c41a' }}>看涨</Text>
                      </div>
                    </div>
                  </Col>
                  <Col span={12}>
                    <div style={{ textAlign: 'center' }}>
                      <Progress
                        type="circle"
                        percent={marketData.marketSentiment.bearish}
                        format={percent => `${percent}%`}
                        strokeColor="#ff4d4f"
                      />
                      <div style={{ marginTop: '8px' }}>
                        <Text strong style={{ color: '#ff4d4f' }}>看跌</Text>
                      </div>
                    </div>
                  </Col>
                </Row>
                <Divider />
                <div style={{ textAlign: 'center' }}>
                  <Title level={4} style={{ color: getSentimentColor(marketData.marketSentiment.fearGreedIndex) }}>
                    恐惧贪婪指数: {marketData.marketSentiment.fearGreedIndex}
                  </Title>
                  <Text style={{ color: getSentimentColor(marketData.marketSentiment.fearGreedIndex) }}>
                    {getSentimentText(marketData.marketSentiment.fearGreedIndex)}
                  </Text>
                </div>
              </Card>
            </Col>
            <Col span={12}>
              <Card title="资金流向概览">
                <Row gutter={[16, 16]}>
                  <Col span={12}>
                    <Card size="small">
                      <Statistic
                        title="主力资金"
                        value={marketData.capitalFlow.mainNetInflow / 1e8}
                        suffix="亿"
                        precision={2}
                        valueStyle={{ color: getChangeColor(marketData.capitalFlow.mainNetInflow) }}
                      />
                    </Card>
                  </Col>
                  <Col span={12}>
                    <Card size="small">
                      <Statistic
                        title="北向资金"
                        value={marketData.capitalFlow.northboundNetInflow / 1e8}
                        suffix="亿"
                        precision={2}
                        valueStyle={{ color: getChangeColor(marketData.capitalFlow.northboundNetInflow) }}
                      />
                    </Card>
                  </Col>
                  <Col span={12}>
                    <Card size="small">
                      <Statistic
                        title="机构资金"
                        value={marketData.capitalFlow.institutionalNetInflow / 1e8}
                        suffix="亿"
                        precision={2}
                        valueStyle={{ color: getChangeColor(marketData.capitalFlow.institutionalNetInflow) }}
                      />
                    </Card>
                  </Col>
                  <Col span={12}>
                    <Card size="small">
                      <Statistic
                        title="散户资金"
                        value={marketData.capitalFlow.retailNetInflow / 1e8}
                        suffix="亿"
                        precision={2}
                        valueStyle={{ color: getChangeColor(marketData.capitalFlow.retailNetInflow) }}
                      />
                    </Card>
                  </Col>
                </Row>
              </Card>
            </Col>
          </Row>

          {/* 市场分析结论 */}
          <Card title="市场扫描结论">
            <Row gutter={[24, 24]}>
              <Col span={12}>
                <Alert
                  message="市场特征"
                  description={
                    <div>
                      <p>• 市场整体表现稳健，主要指数小幅上涨</p>
                      <p>• 消费板块表现强势，白酒、新能源领涨</p>
                      <p>• 市场情绪偏向乐观，机构资金持续流入</p>
                      <p>• 北向资金净流入，外资看好A股市场</p>
                    </div>
                  }
                  type="info"
                  showIcon
                />
              </Col>
              <Col span={12}>
                <Alert
                  message="投资建议"
                  description={
                    <div>
                      <p><strong>市场评级：</strong><Tag color="success">积极</Tag></p>
                      <p><strong>关注板块：</strong>消费、新能源、医药</p>
                      <p><strong>操作策略：</strong>可适当加仓，关注板块轮动</p>
                      <p><strong>风险提示：</strong>注意市场波动，控制仓位</p>
                    </div>
                  }
                  type="success"
                  showIcon
                />
              </Col>
            </Row>
          </Card>
        </div>
      )}
    </div>
  );
};

export default MarketScan; 