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
  Badge,
  Timeline
} from 'antd';
import { 
  SearchOutlined, 
  RiseOutlined, 
  FallOutlined,
  WarningOutlined,
  SafetyOutlined,
  ExclamationCircleOutlined,
  CheckCircleOutlined,
  CloseCircleOutlined,
  AlertOutlined,
  BellOutlined
} from '@ant-design/icons';

const { Title, Text, Paragraph } = Typography;
const { Option } = Select;
const { TabPane } = Tabs;

interface RiskData {
  stockCode: string;
  stockName: string;
  currentPrice: number;
  riskLevel: 'low' | 'medium' | 'high' | 'extreme';
  riskScore: number;
  riskFactors: {
    category: string;
    level: 'low' | 'medium' | 'high';
    description: string;
    impact: string;
    probability: number;
  }[];
  technicalRisks: {
    indicator: string;
    value: number;
    threshold: number;
    status: 'normal' | 'warning' | 'danger';
    description: string;
  }[];
  fundamentalRisks: {
    metric: string;
    value: number;
    industryAvg: number;
    status: 'normal' | 'warning' | 'danger';
    description: string;
  }[];
  marketRisks: {
    type: string;
    level: 'low' | 'medium' | 'high';
    description: string;
    impact: string;
  }[];
  riskHistory: {
    date: string;
    riskLevel: string;
    riskScore: number;
    majorEvents: string[];
  }[];
}

const RiskMonitor: React.FC = () => {
  const [form] = Form.useForm();
  const [loading, setLoading] = useState(false);
  const [riskData, setRiskData] = useState<RiskData | null>(null);
  const [showResult, setShowResult] = useState(false);

  const handleAnalysis = async (values: any) => {
    setLoading(true);
    try {
      // 模拟API调用
      await new Promise(resolve => setTimeout(resolve, 2000));
      
      // 模拟风险监控数据
      const mockData: RiskData = {
        stockCode: values.stockCode,
        stockName: '贵州茅台',
        currentPrice: 1688.00,
        riskLevel: 'medium',
        riskScore: 65,
        riskFactors: [
          {
            category: '估值风险',
            level: 'high',
            description: '当前PE估值处于历史高位',
            impact: '股价回调风险增加',
            probability: 70
          },
          {
            category: '政策风险',
            level: 'medium',
            description: '白酒行业政策不确定性',
            impact: '政策变化可能影响业绩',
            probability: 45
          },
          {
            category: '市场风险',
            level: 'low',
            description: '市场整体波动风险',
            impact: '系统性风险影响有限',
            probability: 25
          }
        ],
        technicalRisks: [
          {
            indicator: 'RSI',
            value: 75,
            threshold: 70,
            status: 'warning',
            description: 'RSI指标接近超买区域'
          },
          {
            indicator: 'MACD',
            value: 0.85,
            threshold: 1.0,
            status: 'normal',
            description: 'MACD指标正常'
          },
          {
            indicator: '布林带位置',
            value: 0.85,
            threshold: 0.8,
            status: 'warning',
            description: '股价接近布林带上轨'
          }
        ],
        fundamentalRisks: [
          {
            metric: 'PE比率',
            value: 28.5,
            industryAvg: 25.0,
            status: 'warning',
            description: 'PE估值高于行业平均'
          },
          {
            metric: 'PB比率',
            value: 12.3,
            industryAvg: 8.5,
            status: 'danger',
            description: 'PB估值显著高于行业平均'
          },
          {
            metric: '资产负债率',
            value: 15.0,
            industryAvg: 45.0,
            status: 'normal',
            description: '负债水平健康'
          }
        ],
        marketRisks: [
          {
            type: '流动性风险',
            level: 'low',
            description: '股票流动性良好',
            impact: '影响较小'
          },
          {
            type: '汇率风险',
            level: 'medium',
            description: '人民币汇率波动',
            impact: '可能影响海外业务'
          },
          {
            type: '利率风险',
            level: 'low',
            description: '利率环境相对稳定',
            impact: '影响有限'
          }
        ],
        riskHistory: [
          {
            date: '2024-01-10',
            riskLevel: '低',
            riskScore: 45,
            majorEvents: ['技术指标正常', '基本面稳健']
          },
          {
            date: '2024-01-12',
            riskLevel: '中',
            riskScore: 65,
            majorEvents: ['估值偏高', '技术指标超买']
          },
          {
            date: '2024-01-15',
            riskLevel: '中',
            riskScore: 65,
            majorEvents: ['政策不确定性', '市场波动']
          }
        ]
      };
      
      setRiskData(mockData);
      setShowResult(true);
    } catch (error) {
      console.error('分析失败:', error);
    } finally {
      setLoading(false);
    }
  };

  const getRiskLevelColor = (level: string) => {
    switch (level) {
      case 'low': return 'success';
      case 'medium': return 'warning';
      case 'high': return 'error';
      case 'extreme': return 'error';
      default: return 'default';
    }
  };

  const getRiskLevelText = (level: string) => {
    switch (level) {
      case 'low': return '低风险';
      case 'medium': return '中风险';
      case 'high': return '高风险';
      case 'extreme': return '极高风险';
      default: return '未知';
    }
  };

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'normal': return 'success';
      case 'warning': return 'warning';
      case 'danger': return 'error';
      default: return 'default';
    }
  };

  const getStatusIcon = (status: string) => {
    switch (status) {
      case 'normal': return <CheckCircleOutlined />;
      case 'warning': return <ExclamationCircleOutlined />;
      case 'danger': return <CloseCircleOutlined />;
      default: return <AlertOutlined />;
    }
  };

  const riskFactorColumns = [
    {
      title: '风险类别',
      dataIndex: 'category',
      key: 'category',
      width: 120,
    },
    {
      title: '风险等级',
      dataIndex: 'level',
      key: 'level',
      width: 100,
      render: (level: string) => (
        <Tag color={getRiskLevelColor(level)}>
          {getRiskLevelText(level)}
        </Tag>
      ),
    },
    {
      title: '风险描述',
      dataIndex: 'description',
      key: 'description',
      width: 200,
    },
    {
      title: '影响程度',
      dataIndex: 'impact',
      key: 'impact',
      width: 150,
    },
    {
      title: '发生概率',
      dataIndex: 'probability',
      key: 'probability',
      width: 100,
      render: (probability: number) => (
        <Progress 
          percent={probability} 
          size="small" 
          strokeColor={probability > 60 ? '#ff4d4f' : probability > 40 ? '#faad14' : '#52c41a'}
          showInfo={false}
        />
      ),
    },
  ];

  const technicalRiskColumns = [
    {
      title: '技术指标',
      dataIndex: 'indicator',
      key: 'indicator',
      width: 120,
    },
    {
      title: '当前值',
      dataIndex: 'value',
      key: 'value',
      width: 100,
      render: (value: number) => value.toFixed(2),
    },
    {
      title: '阈值',
      dataIndex: 'threshold',
      key: 'threshold',
      width: 100,
      render: (threshold: number) => threshold.toFixed(2),
    },
    {
      title: '状态',
      dataIndex: 'status',
      key: 'status',
      width: 100,
      render: (status: string) => (
        <Tag color={getStatusColor(status)} icon={getStatusIcon(status)}>
          {status === 'normal' ? '正常' : status === 'warning' ? '警告' : '危险'}
        </Tag>
      ),
    },
    {
      title: '说明',
      dataIndex: 'description',
      key: 'description',
      render: (description: string) => <Text>{description}</Text>,
    },
  ];

  const fundamentalRiskColumns = [
    {
      title: '财务指标',
      dataIndex: 'metric',
      key: 'metric',
      width: 120,
    },
    {
      title: '当前值',
      dataIndex: 'value',
      key: 'value',
      width: 100,
      render: (value: number) => value.toFixed(2),
    },
    {
      title: '行业平均',
      dataIndex: 'industryAvg',
      key: 'industryAvg',
      width: 120,
      render: (avg: number) => avg.toFixed(2),
    },
    {
      title: '状态',
      dataIndex: 'status',
      key: 'status',
      width: 100,
      render: (status: string) => (
        <Tag color={getStatusColor(status)} icon={getStatusIcon(status)}>
          {status === 'normal' ? '正常' : status === 'warning' ? '警告' : '危险'}
        </Tag>
      ),
    },
    {
      title: '说明',
      dataIndex: 'description',
      key: 'description',
      render: (description: string) => <Text>{description}</Text>,
    },
  ];

  return (
    <div style={{ padding: '24px' }}>
      <Title level={2}>
        <SafetyOutlined style={{ marginRight: 8 }} />
        风险监控
      </Title>
      <Paragraph type="secondary">
        全面监控股票投资风险，包括技术面风险、基本面风险、市场风险等多维度风险评估
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
          
          <Form.Item name="riskType" initialValue="comprehensive">
            <Select style={{ width: 150 }}>
              <Option value="comprehensive">综合风险评估</Option>
              <Option value="technical">技术面风险</Option>
              <Option value="fundamental">基本面风险</Option>
              <Option value="market">市场风险</Option>
            </Select>
          </Form.Item>
          
          <Form.Item>
            <Button 
              type="primary" 
              htmlType="submit" 
              loading={loading}
              icon={<SafetyOutlined />}
            >
              开始风险评估
            </Button>
          </Form.Item>
        </Form>
      </Card>

      {/* 风险评估结果 */}
      {showResult && riskData && (
        <div>
          {/* 风险概览 */}
          <Row gutter={[24, 24]} style={{ marginBottom: '24px' }}>
            <Col span={8}>
              <Card>
                <Statistic
                  title="综合风险等级"
                  value={getRiskLevelText(riskData.riskLevel)}
                  valueStyle={{ 
                    color: getRiskLevelColor(riskData.riskLevel) === 'success' ? '#52c41a' :
                           getRiskLevelColor(riskData.riskLevel) === 'warning' ? '#faad14' : '#ff4d4f'
                  }}
                />
                <Progress 
                  percent={riskData.riskScore} 
                  strokeColor={riskData.riskScore > 70 ? '#ff4d4f' : riskData.riskScore > 50 ? '#faad14' : '#52c41a'}
                  showInfo={false}
                  style={{ marginTop: 16 }}
                />
              </Card>
            </Col>
            <Col span={8}>
              <Card>
                <Statistic
                  title="风险评分"
                  value={riskData.riskScore}
                  suffix="分"
                  valueStyle={{ 
                    color: riskData.riskScore > 70 ? '#ff4d4f' : riskData.riskScore > 50 ? '#faad14' : '#52c41a'
                  }}
                />
                <Text type="secondary">
                  {riskData.riskScore > 70 ? '高风险' : riskData.riskScore > 50 ? '中风险' : '低风险'}
                </Text>
              </Card>
            </Col>
            <Col span={8}>
              <Card>
                <Statistic
                  title="当前价格"
                  value={riskData.currentPrice}
                  suffix="元"
                  precision={2}
                  valueStyle={{ color: '#1890ff' }}
                />
              </Card>
            </Col>
          </Row>

          {/* 详细风险评估 */}
          <Tabs defaultActiveKey="1" style={{ marginBottom: '24px' }}>
            <TabPane tab="风险因素分析" key="1">
              <Card>
                <Table
                  columns={riskFactorColumns}
                  dataSource={riskData.riskFactors}
                  pagination={false}
                  size="small"
                  scroll={{ x: 700 }}
                />
              </Card>
            </TabPane>
            <TabPane tab="技术面风险" key="2">
              <Card>
                <Table
                  columns={technicalRiskColumns}
                  dataSource={riskData.technicalRisks}
                  pagination={false}
                  size="small"
                  scroll={{ x: 600 }}
                />
              </Card>
            </TabPane>
            <TabPane tab="基本面风险" key="3">
              <Card>
                <Table
                  columns={fundamentalRiskColumns}
                  dataSource={riskData.fundamentalRisks}
                  pagination={false}
                  size="small"
                  scroll={{ x: 600 }}
                />
              </Card>
            </TabPane>
            <TabPane tab="市场风险" key="4">
              <Card>
                <List
                  dataSource={riskData.marketRisks}
                  renderItem={(risk) => (
                    <List.Item>
                      <List.Item.Meta
                        title={
                          <Space>
                            <Text strong>{risk.type}</Text>
                            <Tag color={getRiskLevelColor(risk.level)}>
                              {getRiskLevelText(risk.level)}
                            </Tag>
                          </Space>
                        }
                        description={
                          <div>
                            <p>{risk.description}</p>
                            <p><Text type="secondary">影响: {risk.impact}</Text></p>
                          </div>
                        }
                      />
                    </List.Item>
                  )}
                />
              </Card>
            </TabPane>
          </Tabs>

          {/* 风险历史 */}
          <Card title="风险变化历史" style={{ marginBottom: '24px' }}>
            <Timeline>
              {riskData.riskHistory.map((item, index) => (
                <Timeline.Item 
                  key={index}
                  color={item.riskScore > 70 ? 'red' : item.riskScore > 50 ? 'orange' : 'green'}
                >
                  <p><Text strong>{item.date}</Text></p>
                  <p>风险等级: <Tag color={getRiskLevelColor(item.riskLevel === '低' ? 'low' : item.riskLevel === '中' ? 'medium' : 'high')}>
                    {item.riskLevel}
                  </Tag></p>
                  <p>风险评分: {item.riskScore}分</p>
                  <p>主要事件:</p>
                  <ul>
                    {item.majorEvents.map((event, eventIndex) => (
                      <li key={eventIndex}><Text>{event}</Text></li>
                    ))}
                  </ul>
                </Timeline.Item>
              ))}
            </Timeline>
          </Card>

          {/* 风险建议 */}
          <Card title="风险控制建议">
            <Row gutter={[24, 24]}>
              <Col span={12}>
                <Alert
                  message="风险提示"
                  description={
                    <div>
                      <p>• 当前风险等级: <Tag color={getRiskLevelColor(riskData.riskLevel)}>
                        {getRiskLevelText(riskData.riskLevel)}
                      </Tag></p>
                      <p>• 主要风险: 估值偏高、政策不确定性</p>
                      <p>• 技术风险: RSI超买、布林带位置偏高</p>
                      <p>• 基本面风险: PE、PB估值高于行业平均</p>
                    </div>
                  }
                  type="warning"
                  showIcon
                />
              </Col>
              <Col span={12}>
                <Alert
                  message="风险控制措施"
                  description={
                    <div>
                      <p><strong>仓位控制：</strong>建议仓位不超过总资产的15%</p>
                      <p><strong>止损设置：</strong>建议止损位¥1500</p>
                      <p><strong>操作策略：</strong>可逢高减仓，等待回调机会</p>
                      <p><strong>关注重点：</strong>政策变化、估值回归、技术指标修复</p>
                    </div>
                  }
                  type="info"
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

export default RiskMonitor; 