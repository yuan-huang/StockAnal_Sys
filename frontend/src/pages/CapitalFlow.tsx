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
  Avatar
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
  TrendingDownOutlined
} from '@ant-design/icons';

const { Title, Text, Paragraph } = Typography;
const { Option } = Select;
const { TabPane } = Tabs;

interface CapitalFlowData {
  stockCode: string;
  stockName: string;
  currentPrice: number;
  priceChange: number;
  priceChangePercent: number;
  mainNetInflow: number;
  mainNetInflowPercent: number;
  retailNetInflow: number;
  retailNetInflowPercent: number;
  institutionalNetInflow: number;
  institutionalNetInflowPercent: number;
  northboundNetInflow: number;
  northboundNetInflowPercent: number;
  volume: number;
  turnover: number;
  marketCap: number;
  flowHistory: {
    date: string;
    mainFlow: number;
    retailFlow: number;
    institutionalFlow: number;
    northboundFlow: number;
  }[];
  topHolders: {
    name: string;
    type: string;
    shares: number;
    percentage: number;
    change: number;
  }[];
}

const CapitalFlow: React.FC = () => {
  const [form] = Form.useForm();
  const [loading, setLoading] = useState(false);
  const [capitalFlowData, setCapitalFlowData] = useState<CapitalFlowData | null>(null);
  const [showResult, setShowResult] = useState(false);

  const handleAnalysis = async (values: any) => {
    setLoading(true);
    try {
      // 模拟API调用
      await new Promise(resolve => setTimeout(resolve, 2000));
      
      // 模拟资金流向数据
      const mockData: CapitalFlowData = {
        stockCode: values.stockCode,
        stockName: '贵州茅台',
        currentPrice: 1688.00,
        priceChange: 12.50,
        priceChangePercent: 0.75,
        mainNetInflow: 2.5e9,
        mainNetInflowPercent: 15.2,
        retailNetInflow: -1.2e9,
        retailNetInflowPercent: -8.5,
        institutionalNetInflow: 3.8e9,
        institutionalNetInflowPercent: 22.1,
        northboundNetInflow: 0.8e9,
        northboundNetInflowPercent: 4.8,
        volume: 8.5e7,
        turnover: 1.43e11,
        marketCap: 2.1e12,
        flowHistory: [
          { date: '2024-01-10', mainFlow: 1.2e9, retailFlow: -0.8e9, institutionalFlow: 2.1e9, northboundFlow: 0.3e9 },
          { date: '2024-01-11', mainFlow: 1.8e9, retailFlow: -1.1e9, institutionalFlow: 2.5e9, northboundFlow: 0.5e9 },
          { date: '2024-01-12', mainFlow: 2.1e9, retailFlow: -1.3e9, institutionalFlow: 3.2e9, northboundFlow: 0.7e9 },
          { date: '2024-01-13', mainFlow: 2.5e9, retailFlow: -1.2e9, institutionalFlow: 3.8e9, northboundFlow: 0.8e9 },
          { date: '2024-01-14', mainFlow: 2.3e9, retailFlow: -1.0e9, institutionalFlow: 3.5e9, northboundFlow: 0.6e9 }
        ],
        topHolders: [
          { name: '贵州茅台集团', type: '国有股东', shares: 6.78e8, percentage: 54.0, change: 0 },
          { name: '香港中央结算', type: '外资股东', shares: 1.23e8, percentage: 9.8, change: 0.5 },
          { name: '中国证券金融', type: '机构股东', shares: 8.56e7, percentage: 6.8, change: -0.2 },
          { name: '中央汇金', type: '机构股东', shares: 6.78e7, percentage: 5.4, change: 0.1 },
          { name: '社保基金', type: '机构股东', shares: 5.43e7, percentage: 4.3, change: 0.3 }
        ]
      };
      
      setCapitalFlowData(mockData);
      setShowResult(true);
    } catch (error) {
      console.error('分析失败:', error);
    } finally {
      setLoading(false);
    }
  };

  const getFlowColor = (value: number) => {
    return value > 0 ? '#52c41a' : '#ff4d4f';
  };

  const getFlowIcon = (value: number) => {
    return value > 0 ? <RiseOutlined /> : <FallOutlined />;
  };

  const getFlowTag = (value: number) => {
    return value > 0 ? 
      <Tag color="green" icon={<RiseOutlined />}>净流入</Tag> : 
      <Tag color="red" icon={<FallOutlined />}>净流出</Tag>;
  };

  const flowHistoryColumns = [
    {
      title: '日期',
      dataIndex: 'date',
      key: 'date',
      width: 120,
    },
    {
      title: '主力资金',
      dataIndex: 'mainFlow',
      key: 'mainFlow',
      width: 120,
      render: (value: number) => (
        <Space>
          {getFlowIcon(value)}
          <Text style={{ color: getFlowColor(value) }}>
            {(value / 1e8).toFixed(2)}亿
          </Text>
        </Space>
      ),
    },
    {
      title: '散户资金',
      dataIndex: 'retailFlow',
      key: 'retailFlow',
      width: 120,
      render: (value: number) => (
        <Space>
          {getFlowIcon(value)}
          <Text style={{ color: getFlowColor(value) }}>
            {(value / 1e8).toFixed(2)}亿
          </Text>
        </Space>
      ),
    },
    {
      title: '机构资金',
      dataIndex: 'institutionalFlow',
      key: 'institutionalFlow',
      width: 120,
      render: (value: number) => (
        <Space>
          {getFlowIcon(value)}
          <Text style={{ color: getFlowColor(value) }}>
            {(value / 1e8).toFixed(2)}亿
          </Text>
        </Space>
      ),
    },
    {
      title: '北向资金',
      dataIndex: 'northboundFlow',
      key: 'northboundFlow',
      width: 120,
      render: (value: number) => (
        <Space>
          {getFlowIcon(value)}
          <Text style={{ color: getFlowColor(value) }}>
            {(value / 1e8).toFixed(2)}亿
          </Text>
        </Space>
      ),
    },
  ];

  const holdersColumns = [
    {
      title: '股东名称',
      dataIndex: 'name',
      key: 'name',
      width: 200,
    },
    {
      title: '股东类型',
      dataIndex: 'type',
      key: 'type',
      width: 120,
      render: (type: string) => {
        let color = 'default';
        if (type.includes('国有')) color = 'red';
        else if (type.includes('外资')) color = 'blue';
        else if (type.includes('机构')) color = 'green';
        return <Tag color={color}>{type}</Tag>;
      },
    },
    {
      title: '持股数量(万股)',
      dataIndex: 'shares',
      key: 'shares',
      width: 150,
      render: (shares: number) => (shares / 1e4).toFixed(0),
    },
    {
      title: '持股比例(%)',
      dataIndex: 'percentage',
      key: 'percentage',
      width: 120,
      render: (percentage: number) => percentage.toFixed(1),
    },
    {
      title: '变动(%)',
      dataIndex: 'change',
      key: 'change',
      width: 100,
      render: (change: number) => (
        <Text style={{ color: change > 0 ? '#52c41a' : change < 0 ? '#ff4d4f' : '#666' }}>
          {change > 0 ? '+' : ''}{change.toFixed(1)}
        </Text>
      ),
    },
  ];

  return (
    <div style={{ padding: '24px' }}>
      <Title level={2}>
        <DollarOutlined style={{ marginRight: 8 }} />
        资金流向分析
      </Title>
      <Paragraph type="secondary">
        分析股票的资金流向情况，包括主力资金、散户资金、机构资金和北向资金的流入流出情况
      </Paragraph>
      
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
          
          <Form.Item name="timeRange" initialValue="5d">
            <Select style={{ width: 120 }}>
              <Option value="1d">1日</Option>
              <Option value="3d">3日</Option>
              <Option value="5d">5日</Option>
              <Option value="10d">10日</Option>
              <Option value="1m">1月</Option>
            </Select>
          </Form.Item>
          
          <Form.Item>
            <Button 
              type="primary" 
              htmlType="submit" 
              loading={loading}
              icon={<BarChartOutlined />}
            >
              分析资金流向
            </Button>
          </Form.Item>
        </Form>
      </Card>

      {/* 分析结果 */}
      {showResult && capitalFlowData && (
        <div>
          {/* 基本信息 */}
          <Row gutter={[24, 24]} style={{ marginBottom: '24px' }}>
            <Col span={8}>
              <Card>
                <Statistic
                  title="当前价格"
                  value={capitalFlowData.currentPrice}
                  suffix="元"
                  precision={2}
                  valueStyle={{ color: '#1890ff' }}
                  prefix={<DollarOutlined />}
                />
                <div style={{ marginTop: '8px' }}>
                  <Space>
                    {capitalFlowData.priceChange > 0 ? (
                      <RiseOutlined style={{ color: '#52c41a' }} />
                    ) : (
                      <FallOutlined style={{ color: '#ff4d4f' }} />
                    )}
                    <Text 
                      type={capitalFlowData.priceChange > 0 ? 'success' : 'danger'}
                    >
                      {capitalFlowData.priceChange > 0 ? '+' : ''}
                      {capitalFlowData.priceChange.toFixed(2)} 
                      ({capitalFlowData.priceChangePercent.toFixed(2)}%)
                    </Text>
                  </Space>
                </div>
              </Card>
            </Col>
            <Col span={8}>
              <Card>
                <Statistic
                  title="成交量"
                  value={capitalFlowData.volume / 1e4}
                  suffix="万股"
                  precision={0}
                  valueStyle={{ color: '#52c41a' }}
                />
              </Card>
            </Col>
            <Col span={8}>
              <Card>
                <Statistic
                  title="成交额"
                  value={capitalFlowData.turnover / 1e8}
                  suffix="亿元"
                  precision={2}
                  valueStyle={{ color: '#faad14' }}
                />
              </Card>
            </Col>
          </Row>

          {/* 资金流向概览 */}
          <Card title="资金流向概览" style={{ marginBottom: '24px' }}>
            <Row gutter={[24, 24]}>
              <Col span={6}>
                <Card size="small">
                  <div style={{ textAlign: 'center' }}>
                    <Title level={4} style={{ margin: 0, color: getFlowColor(capitalFlowData.mainNetInflow) }}>
                      {(capitalFlowData.mainNetInflow / 1e8).toFixed(2)}亿
                    </Title>
                    <Text type="secondary">主力资金</Text>
                    <div style={{ marginTop: '8px' }}>
                      {getFlowTag(capitalFlowData.mainNetInflow)}
                    </div>
                    <Text style={{ color: getFlowColor(capitalFlowData.mainNetInflow) }}>
                      {capitalFlowData.mainNetInflowPercent > 0 ? '+' : ''}
                      {capitalFlowData.mainNetInflowPercent.toFixed(1)}%
                    </Text>
                  </div>
                </Card>
              </Col>
              <Col span={6}>
                <Card size="small">
                  <div style={{ textAlign: 'center' }}>
                    <Title level={4} style={{ margin: 0, color: getFlowColor(capitalFlowData.retailNetInflow) }}>
                      {(capitalFlowData.retailNetInflow / 1e8).toFixed(2)}亿
                    </Title>
                    <Text type="secondary">散户资金</Text>
                    <div style={{ marginTop: '8px' }}>
                      {getFlowTag(capitalFlowData.retailNetInflow)}
                    </div>
                    <Text style={{ color: getFlowColor(capitalFlowData.retailNetInflow) }}>
                      {capitalFlowData.retailNetInflowPercent > 0 ? '+' : ''}
                      {capitalFlowData.retailNetInflowPercent.toFixed(1)}%
                    </Text>
                  </div>
                </Card>
              </Col>
              <Col span={6}>
                <Card size="small">
                  <div style={{ textAlign: 'center' }}>
                    <Title level={4} style={{ color: getFlowColor(capitalFlowData.institutionalNetInflow) }}>
                      {(capitalFlowData.institutionalNetInflow / 1e8).toFixed(2)}亿
                    </Title>
                    <Text type="secondary">机构资金</Text>
                    <div style={{ marginTop: '8px' }}>
                      {getFlowTag(capitalFlowData.institutionalNetInflow)}
                    </div>
                    <Text style={{ color: getFlowColor(capitalFlowData.institutionalNetInflow) }}>
                      {capitalFlowData.institutionalNetInflowPercent > 0 ? '+' : ''}
                      {capitalFlowData.institutionalNetInflowPercent.toFixed(1)}%
                    </Text>
                  </div>
                </Card>
              </Col>
              <Col span={6}>
                <Card size="small">
                  <div style={{ textAlign: 'center' }}>
                    <Title level={4} style={{ color: getFlowColor(capitalFlowData.northboundNetInflow) }}>
                      {(capitalFlowData.northboundNetInflow / 1e8).toFixed(2)}亿
                    </Title>
                    <Text type="secondary">北向资金</Text>
                    <div style={{ marginTop: '8px' }}>
                      {getFlowTag(capitalFlowData.northboundNetInflow)}
                    </div>
                    <Text style={{ color: getFlowColor(capitalFlowData.northboundNetInflow) }}>
                      {capitalFlowData.northboundNetInflowPercent > 0 ? '+' : ''}
                      {capitalFlowData.northboundNetInflowPercent.toFixed(1)}%
                    </Text>
                  </div>
                </Card>
              </Col>
            </Row>
          </Card>

          {/* 详细数据 */}
          <Tabs defaultActiveKey="1" style={{ marginBottom: '24px' }}>
            <TabPane tab="资金流向历史" key="1">
              <Card>
                <Table
                  columns={flowHistoryColumns}
                  dataSource={capitalFlowData.flowHistory}
                  pagination={false}
                  size="small"
                  scroll={{ x: 600 }}
                />
              </Card>
            </TabPane>
            <TabPane tab="前十大股东" key="2">
              <Card>
                <Table
                  columns={holdersColumns}
                  dataSource={capitalFlowData.topHolders}
                  pagination={false}
                  size="small"
                  scroll={{ x: 700 }}
                />
              </Card>
            </TabPane>
          </Tabs>

          {/* 投资建议 */}
          <Card title="资金流向分析结论">
            <Row gutter={[24, 24]}>
              <Col span={12}>
                <Alert
                  message="资金流向特征"
                  description={
                    <div>
                      <p>• 主力资金持续净流入，显示机构看好</p>
                      <p>• 散户资金净流出，可能存在分歧</p>
                      <p>• 机构资金大幅净流入，专业投资者认可</p>
                      <p>• 北向资金净流入，外资持续加仓</p>
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
                      <p><strong>资金面评级：</strong><Tag color="success">优秀</Tag></p>
                      <p><strong>投资建议：</strong>资金面支撑强劲，建议关注</p>
                      <p><strong>风险提示：</strong>注意主力资金流向变化</p>
                      <p><strong>操作策略：</strong>可逢低分批建仓</p>
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

export default CapitalFlow; 