import React, { useState } from 'react';
import { 
  Card, 
  Form, 
  Input, 
  Select, 
  Button, 
  Row, 
  Col, 
  Table, 
  Typography, 
  Space,
  Tag,
  Progress,
  Statistic,
  Divider,
  Alert
} from 'antd';
import { 
  SearchOutlined, 
  RiseOutlined, 
  FallOutlined,
  CheckCircleOutlined,
  CloseCircleOutlined,
  ExclamationCircleOutlined,
  DollarOutlined,
  BarChartOutlined,
  LineChartOutlined
} from '@ant-design/icons';

const { Title, Text, Paragraph } = Typography;
const { Option } = Select;

interface FundamentalData {
  stockCode: string;
  stockName: string;
  industry: string;
  marketCap: number;
  pe: number;
  pb: number;
  ps: number;
  roe: number;
  roa: number;
  debtRatio: number;
  currentRatio: number;
  quickRatio: number;
  grossMargin: number;
  netMargin: number;
  revenueGrowth: number;
  profitGrowth: number;
  dividendYield: number;
  score: number;
}

const FundamentalAnalysis: React.FC = () => {
  const [form] = Form.useForm();
  const [loading, setLoading] = useState(false);
  const [fundamentalData, setFundamentalData] = useState<FundamentalData | null>(null);
  const [showResult, setShowResult] = useState(false);

  const handleAnalysis = async (values: any) => {
    setLoading(true);
    try {
      // 模拟API调用
      await new Promise(resolve => setTimeout(resolve, 2000));
      
      // 模拟基本面数据
      const mockData: FundamentalData = {
        stockCode: values.stockCode,
        stockName: '贵州茅台',
        industry: '白酒',
        marketCap: 2.1e12,
        pe: 28.5,
        pb: 12.3,
        ps: 15.8,
        roe: 25.8,
        roa: 18.5,
        debtRatio: 0.15,
        currentRatio: 3.2,
        quickRatio: 2.8,
        grossMargin: 91.5,
        netMargin: 52.3,
        revenueGrowth: 12.5,
        profitGrowth: 15.8,
        dividendYield: 1.2,
        score: 88
      };
      
      setFundamentalData(mockData);
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

  const getGrowthColor = (growth: number) => {
    if (growth > 0) return '#52c41a';
    if (growth < 0) return '#ff4d4f';
    return '#faad14';
  };

  const getGrowthIcon = (growth: number) => {
    if (growth > 0) return <RiseOutlined style={{ color: '#52c41a' }} />;
    if (growth < 0) return <FallOutlined style={{ color: '#ff4d4f' }} />;
    return <ExclamationCircleOutlined style={{ color: '#faad14' }} />;
  };

  const columns = [
    {
      title: '指标',
      dataIndex: 'indicator',
      key: 'indicator',
      width: 120,
    },
    {
      title: '数值',
      dataIndex: 'value',
      key: 'value',
      width: 100,
      render: (value: any, record: any) => {
        if (record.type === 'percentage') {
          return (
            <Space>
              {getGrowthIcon(value)}
              <Text style={{ color: getGrowthColor(value) }}>
                {value > 0 ? '+' : ''}{value.toFixed(2)}%
              </Text>
            </Space>
          );
        }
        if (record.type === 'ratio') {
          return <Text>{value.toFixed(2)}</Text>;
        }
        if (record.type === 'currency') {
          return <Text>¥{(value / 1e8).toFixed(2)}亿</Text>;
        }
        return <Text>{value}</Text>;
      },
    },
    {
      title: '行业平均',
      dataIndex: 'industryAvg',
      key: 'industryAvg',
      width: 100,
      render: (value: any, record: any) => {
        if (record.type === 'percentage') {
          return <Text>{value.toFixed(2)}%</Text>;
        }
        if (record.type === 'ratio') {
          return <Text>{value.toFixed(2)}</Text>;
        }
        return <Text>{value}</Text>;
      },
    },
    {
      title: '评级',
      dataIndex: 'rating',
      key: 'rating',
      width: 80,
      render: (rating: string) => {
        let color = 'default';
        if (rating === '优秀') color = 'success';
        else if (rating === '良好') color = 'processing';
        else if (rating === '一般') color = 'warning';
        else if (rating === '较差') color = 'error';
        
        return <Tag color={color}>{rating}</Tag>;
      },
    },
  ];

  const getTableData = (data: FundamentalData) => [
    {
      key: '1',
      indicator: '市盈率(PE)',
      value: data.pe,
      industryAvg: 25.0,
      rating: data.pe < 20 ? '优秀' : data.pe < 30 ? '良好' : data.pe < 40 ? '一般' : '较差',
      type: 'ratio'
    },
    {
      key: '2',
      indicator: '市净率(PB)',
      value: data.pb,
      industryAvg: 8.5,
      rating: data.pb < 5 ? '优秀' : data.pb < 10 ? '良好' : data.pb < 15 ? '一般' : '较差',
      type: 'ratio'
    },
    {
      key: '3',
      indicator: '市销率(PS)',
      value: data.ps,
      industryAvg: 12.0,
      rating: data.ps < 8 ? '优秀' : data.ps < 15 ? '良好' : data.ps < 20 ? '一般' : '较差',
      type: 'ratio'
    },
    {
      key: '4',
      indicator: '净资产收益率',
      value: data.roe,
      industryAvg: 15.0,
      rating: data.roe > 20 ? '优秀' : data.roe > 15 ? '良好' : data.roe > 10 ? '一般' : '较差',
      type: 'percentage'
    },
    {
      key: '5',
      indicator: '总资产收益率',
      value: data.roa,
      industryAvg: 10.0,
      rating: data.roa > 15 ? '优秀' : data.roa > 10 ? '良好' : data.roa > 5 ? '一般' : '较差',
      type: 'percentage'
    },
    {
      key: '6',
      indicator: '资产负债率',
      value: data.debtRatio * 100,
      industryAvg: 45.0,
      rating: data.debtRatio < 0.3 ? '优秀' : data.debtRatio < 0.5 ? '良好' : data.debtRatio < 0.7 ? '一般' : '较差',
      type: 'percentage'
    },
    {
      key: '7',
      indicator: '流动比率',
      value: data.currentRatio,
      industryAvg: 2.0,
      rating: data.currentRatio > 2.5 ? '优秀' : data.currentRatio > 2.0 ? '良好' : data.currentRatio > 1.5 ? '一般' : '较差',
      type: 'ratio'
    },
    {
      key: '8',
      indicator: '毛利率',
      value: data.grossMargin,
      industryAvg: 65.0,
      rating: data.grossMargin > 80 ? '优秀' : data.grossMargin > 65 ? '良好' : data.grossMargin > 50 ? '一般' : '较差',
      type: 'percentage'
    },
    {
      key: '9',
      indicator: '净利率',
      value: data.netMargin,
      industryAvg: 35.0,
      rating: data.netMargin > 45 ? '优秀' : data.netMargin > 35 ? '良好' : data.netMargin > 25 ? '一般' : '较差',
      type: 'percentage'
    },
    {
      key: '10',
      indicator: '营收增长率',
      value: data.revenueGrowth,
      industryAvg: 8.0,
      rating: data.revenueGrowth > 15 ? '优秀' : data.revenueGrowth > 8 ? '良好' : data.revenueGrowth > 0 ? '一般' : '较差',
      type: 'percentage'
    },
    {
      key: '11',
      indicator: '净利润增长率',
      value: data.profitGrowth,
      industryAvg: 10.0,
      rating: data.profitGrowth > 20 ? '优秀' : data.profitGrowth > 10 ? '良好' : data.profitGrowth > 0 ? '一般' : '较差',
      type: 'percentage'
    },
    {
      key: '12',
      indicator: '股息率',
      value: data.dividendYield,
      industryAvg: 2.5,
      rating: data.dividendYield > 4 ? '优秀' : data.dividendYield > 2.5 ? '良好' : data.dividendYield > 1 ? '一般' : '较差',
      type: 'percentage'
    },
  ];

  return (
    <div style={{ padding: '24px' }}>
      <Title level={2}>基本面分析</Title>
      <Paragraph type="secondary">
        通过分析公司的财务指标、盈利能力、成长性等基本面因素，评估股票的投资价值
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
          
          <Form.Item name="marketType" initialValue="A">
            <Select style={{ width: 100 }}>
              <Option value="A">A股</Option>
              <Option value="HK">港股</Option>
              <Option value="US">美股</Option>
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
      {showResult && fundamentalData && (
        <div>
          {/* 基本信息 */}
          <Row gutter={[24, 24]} style={{ marginBottom: '24px' }}>
            <Col span={8}>
              <Card>
                <Statistic
                  title="综合评分"
                  value={fundamentalData.score}
                  suffix="分"
                  valueStyle={{ color: getScoreColor(fundamentalData.score) }}
                />
                <Progress 
                  percent={fundamentalData.score} 
                  strokeColor={getScoreColor(fundamentalData.score)}
                  showInfo={false}
                  style={{ marginTop: 16 }}
                />
              </Card>
            </Col>
            <Col span={8}>
              <Card>
                <Statistic
                  title="市值"
                  value={fundamentalData.marketCap / 1e12}
                  suffix="万亿"
                  precision={2}
                  valueStyle={{ color: '#1890ff' }}
                  prefix={<DollarOutlined />}
                />
              </Card>
            </Col>
            <Col span={8}>
              <Card>
                <Statistic
                  title="行业"
                  value={fundamentalData.industry}
                  valueStyle={{ color: '#52c41a' }}
                  prefix={<BarChartOutlined />}
                />
              </Card>
            </Col>
          </Row>

          {/* 详细指标表格 */}
          <Card title="财务指标分析" style={{ marginBottom: '24px' }}>
            <Table
              columns={columns}
              dataSource={getTableData(fundamentalData)}
              pagination={false}
              size="small"
              scroll={{ x: 600 }}
            />
          </Card>

          {/* 投资建议 */}
          <Card title="投资建议">
            <Row gutter={[24, 24]}>
              <Col span={12}>
                <Alert
                  message="基本面分析结论"
                  description={
                    <div>
                      <p>基于财务指标分析，该股票基本面表现：</p>
                      <ul>
                        <li>盈利能力：<Tag color="success">优秀</Tag></li>
                        <li>成长性：<Tag color="processing">良好</Tag></li>
                        <li>财务健康度：<Tag color="success">优秀</Tag></li>
                        <li>估值水平：<Tag color="warning">一般</Tag></li>
                      </ul>
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
                      <p><strong>综合评级：</strong><Tag color="success">推荐买入</Tag></p>
                      <p><strong>目标价位：</strong>¥1800-2000</p>
                      <p><strong>风险提示：</strong>估值偏高，需关注市场波动</p>
                      <p><strong>持有周期：</strong>中长期（6-12个月）</p>
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

export default FundamentalAnalysis; 