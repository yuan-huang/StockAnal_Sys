import React, { useState, useEffect } from 'react';
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
  Timeline,
  Steps,
  Result,
  List,
  Avatar,
  Badge,
  Modal,
  message
} from 'antd';
import { 
  SearchOutlined, 
  RiseOutlined, 
  FallOutlined,
  CheckCircleOutlined,
  ClockCircleOutlined,
  ExclamationCircleOutlined,
  RobotOutlined,
  BrainOutlined,
  LineChartOutlined,
  ThunderboltOutlined,
  PlayCircleOutlined,
  PauseCircleOutlined,
  StopOutlined,
  DeleteOutlined,
  EyeOutlined
} from '@ant-design/icons';

const { Title, Text, Paragraph } = Typography;
const { Option } = Select;
const { Step } = Steps;

interface AgentTask {
  taskId: string;
  stockCode: string;
  stockName: string;
  status: 'pending' | 'running' | 'completed' | 'failed';
  progress: number;
  currentStep: string;
  startTime: string;
  estimatedTime: string;
  result?: {
    analysis: string;
    recommendation: string;
    confidence: number;
    riskLevel: string;
    targetPrice: number;
  };
}

interface AgentAnalysis {
  stockCode: string;
  stockName: string;
  analysis: {
    technical: string;
    fundamental: string;
    sentiment: string;
    macro: string;
  };
  recommendation: {
    action: string;
    confidence: number;
    reasoning: string;
    riskFactors: string[];
    opportunities: string[];
  };
  timeline: {
    shortTerm: { price: number; probability: number };
    mediumTerm: { price: number; probability: number };
    longTerm: { price: number; probability: number };
  };
}

const AgentAnalysis: React.FC = () => {
  const [form] = Form.useForm();
  const [loading, setLoading] = useState(false);
  const [activeTasks, setActiveTasks] = useState<AgentTask[]>([]);
  const [analysisResult, setAnalysisResult] = useState<AgentAnalysis | null>(null);
  const [showResult, setShowResult] = useState(false);
  const [selectedTask, setSelectedTask] = useState<AgentTask | null>(null);
  const [isModalVisible, setIsModalVisible] = useState(false);

  useEffect(() => {
    // 模拟获取活跃任务
    const mockTasks: AgentTask[] = [
      {
        taskId: 'task_001',
        stockCode: '600519',
        stockName: '贵州茅台',
        status: 'running',
        progress: 65,
        currentStep: '技术面分析',
        startTime: '2024-01-15 10:30:00',
        estimatedTime: '约15分钟'
      },
      {
        taskId: 'task_002',
        stockCode: '000858',
        stockName: '五粮液',
        status: 'pending',
        progress: 0,
        currentStep: '等待中',
        startTime: '2024-01-15 10:35:00',
        estimatedTime: '约20分钟'
      }
    ];
    setActiveTasks(mockTasks);
  }, []);

  const handleAnalysis = async (values: any) => {
    setLoading(true);
    try {
      // 模拟API调用
      await new Promise(resolve => setTimeout(resolve, 2000));
      
      // 模拟智能体分析结果
      const mockResult: AgentAnalysis = {
        stockCode: values.stockCode,
        stockName: '贵州茅台',
        analysis: {
          technical: '技术面显示股价处于上升通道，MACD金叉确认，RSI指标健康，短期有望突破前期高点。',
          fundamental: '基本面稳健，ROE持续提升，现金流充裕，品牌护城河深厚，长期投资价值突出。',
          sentiment: '市场情绪积极，机构持仓增加，散户关注度提升，社交媒体讨论热度上升。',
          macro: '宏观经济环境改善，消费升级趋势持续，政策面支持，行业景气度向好。'
        },
        recommendation: {
          action: '强烈推荐买入',
          confidence: 85,
          reasoning: '综合技术面、基本面、情绪面和宏观面分析，该股票具备多重利好因素，投资价值显著。',
          riskFactors: ['估值偏高', '政策风险', '市场波动'],
          opportunities: ['消费升级', '品牌价值提升', '海外扩张']
        },
        timeline: {
          shortTerm: { price: 1800, probability: 75 },
          mediumTerm: { price: 2000, probability: 65 },
          longTerm: { price: 2500, probability: 55 }
        }
      };
      
      setAnalysisResult(mockResult);
      setShowResult(true);
    } catch (error) {
      console.error('分析失败:', error);
      message.error('智能体分析失败，请重试');
    } finally {
      setLoading(false);
    }
  };

  const handleTaskAction = (taskId: string, action: 'start' | 'pause' | 'stop' | 'delete') => {
    switch (action) {
      case 'start':
        message.success('任务已启动');
        break;
      case 'pause':
        message.info('任务已暂停');
        break;
      case 'stop':
        message.warning('任务已停止');
        break;
      case 'delete':
        Modal.confirm({
          title: '确认删除',
          content: '确定要删除这个分析任务吗？',
          onOk: () => {
            setActiveTasks(prev => prev.filter(task => task.taskId !== taskId));
            message.success('任务已删除');
          }
        });
        break;
    }
  };

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'running': return 'processing';
      case 'completed': return 'success';
      case 'failed': return 'error';
      default: return 'default';
    }
  };

  const getStatusIcon = (status: string) => {
    switch (status) {
      case 'running': return <PlayCircleOutlined />;
      case 'completed': return <CheckCircleOutlined />;
      case 'failed': return <ExclamationCircleOutlined />;
      default: return <ClockCircleOutlined />;
    }
  };

  const getRiskLevelColor = (riskLevel: string) => {
    switch (riskLevel) {
      case '低': return 'success';
      case '中': return 'warning';
      case '高': return 'error';
      default: return 'default';
    }
  };

  return (
    <div style={{ padding: '24px' }}>
      <Title level={2}>
        <RobotOutlined style={{ marginRight: 8 }} />
        智能体分析
      </Title>
      <Paragraph type="secondary">
        基于AI智能体的多维度股票分析，结合技术面、基本面、情绪面和宏观面数据，提供智能化投资建议
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
          
          <Form.Item name="analysisType" initialValue="comprehensive">
            <Select style={{ width: 150 }}>
              <Option value="comprehensive">综合分析</Option>
              <Option value="technical">技术面分析</Option>
              <Option value="fundamental">基本面分析</Option>
              <Option value="sentiment">情绪面分析</Option>
            </Select>
          </Form.Item>
          
          <Form.Item name="timeHorizon" initialValue="1y">
            <Select style={{ width: 120 }}>
              <Option value="6m">6个月</Option>
              <Option value="1y">1年</Option>
              <Option value="2y">2年</Option>
            </Select>
          </Form.Item>
          
          <Form.Item>
            <Button 
              type="primary" 
              htmlType="submit" 
              loading={loading}
              icon={<BrainOutlined />}
            >
              启动智能分析
            </Button>
          </Form.Item>
        </Form>
      </Card>

      {/* 活跃任务监控 */}
      {activeTasks.length > 0 && (
        <Card title="活跃分析任务" style={{ marginBottom: '24px' }}>
          <List
            dataSource={activeTasks}
            renderItem={(task) => (
              <List.Item
                actions={[
                  <Button
                    key="view"
                    type="text"
                    icon={<EyeOutlined />}
                    onClick={() => {
                      setSelectedTask(task);
                      setIsModalVisible(true);
                    }}
                  >
                    查看详情
                  </Button>,
                  <Button
                    key="pause"
                    type="text"
                    icon={<PauseCircleOutlined />}
                    onClick={() => handleTaskAction(task.taskId, 'pause')}
                    disabled={task.status !== 'running'}
                  >
                    暂停
                  </Button>,
                  <Button
                    key="stop"
                    type="text"
                    icon={<StopOutlined />}
                    onClick={() => handleTaskAction(task.taskId, 'stop')}
                    disabled={task.status === 'completed'}
                  >
                    停止
                  </Button>,
                  <Button
                    key="delete"
                    type="text"
                    icon={<DeleteOutlined />}
                    onClick={() => handleTaskAction(task.taskId, 'delete')}
                    danger
                  >
                    删除
                  </Button>
                ]}
              >
                <List.Item.Meta
                  avatar={
                    <Badge status={getStatusColor(task.status) as any}>
                      <Avatar icon={getStatusIcon(task.status)} />
                    </Badge>
                  }
                  title={
                    <Space>
                      <Text strong>{task.stockName}</Text>
                      <Tag color="blue">{task.stockCode}</Tag>
                      <Tag color={getStatusColor(task.status)}>
                        {task.status === 'running' ? '分析中' : 
                         task.status === 'completed' ? '已完成' : 
                         task.status === 'failed' ? '失败' : '等待中'}
                      </Tag>
                    </Space>
                  }
                  description={
                    <div>
                      <Text type="secondary">当前步骤: {task.currentStep}</Text>
                      <br />
                      <Text type="secondary">开始时间: {task.startTime}</Text>
                      <br />
                      <Text type="secondary">预计完成: {task.estimatedTime}</Text>
                    </div>
                  }
                />
                <div style={{ width: 200 }}>
                  <Progress 
                    percent={task.progress} 
                    status={task.status === 'failed' ? 'exception' : undefined}
                    format={percent => `${percent}%`}
                  />
                </div>
              </List.Item>
            )}
          />
        </Card>
      )}

      {/* 分析结果 */}
      {showResult && analysisResult && (
        <div>
          {/* 分析概览 */}
          <Row gutter={[24, 24]} style={{ marginBottom: '24px' }}>
            <Col span={8}>
              <Card>
                <Statistic
                  title="投资建议"
                  value={analysisResult.recommendation.action}
                  valueStyle={{ color: '#52c41a', fontSize: '16px' }}
                />
              </Card>
            </Col>
            <Col span={8}>
              <Card>
                <Statistic
                  title="置信度"
                  value={analysisResult.recommendation.confidence}
                  suffix="%"
                  valueStyle={{ color: '#1890ff' }}
                />
              </Card>
            </Col>
            <Col span={8}>
              <Card>
                <Statistic
                  title="风险等级"
                  value={analysisResult.recommendation.riskLevel || '中'}
                  valueStyle={{ color: '#faad14' }}
                />
              </Card>
            </Col>
          </Row>

          {/* 详细分析 */}
          <Row gutter={[24, 24]} style={{ marginBottom: '24px' }}>
            <Col span={12}>
              <Card title="技术面分析">
                <Paragraph>{analysisResult.analysis.technical}</Paragraph>
              </Card>
            </Col>
            <Col span={12}>
              <Card title="基本面分析">
                <Paragraph>{analysisResult.analysis.fundamental}</Paragraph>
              </Card>
            </Col>
            <Col span={12}>
              <Card title="情绪面分析">
                <Paragraph>{analysisResult.analysis.sentiment}</Paragraph>
              </Card>
            </Col>
            <Col span={12}>
              <Card title="宏观面分析">
                <Paragraph>{analysisResult.analysis.macro}</Paragraph>
              </Card>
            </Col>
          </Row>

          {/* 投资建议 */}
          <Card title="智能投资建议" style={{ marginBottom: '24px' }}>
            <Row gutter={[24, 24]}>
              <Col span={12}>
                <Alert
                  message="推荐理由"
                  description={analysisResult.recommendation.reasoning}
                  type="info"
                  showIcon
                />
              </Col>
              <Col span={12}>
                <div>
                  <Text strong>风险因素:</Text>
                  <div style={{ marginTop: '8px' }}>
                    {analysisResult.recommendation.riskFactors.map((risk, index) => (
                      <Tag key={index} color="red" style={{ marginBottom: '4px' }}>
                        {risk}
                      </Tag>
                    ))}
                  </div>
                  <Divider />
                  <Text strong>发展机遇:</Text>
                  <div style={{ marginTop: '8px' }}>
                    {analysisResult.recommendation.opportunities.map((opportunity, index) => (
                      <Tag key={index} color="green" style={{ marginBottom: '4px' }}>
                        {opportunity}
                      </Tag>
                    ))}
                  </div>
                </div>
              </Col>
            </Row>
          </Card>

          {/* 时间轴预测 */}
          <Card title="智能预测时间轴">
            <Timeline>
              <Timeline.Item color="green">
                <p><Text strong>短期预测 (3个月)</Text></p>
                <p>目标价格: ¥{analysisResult.timeline.shortTerm.price}</p>
                <p>实现概率: {analysisResult.timeline.shortTerm.probability}%</p>
              </Timeline.Item>
              <Timeline.Item color="blue">
                <p><Text strong>中期预测 (6个月)</Text></p>
                <p>目标价格: ¥{analysisResult.timeline.mediumTerm.price}</p>
                <p>实现概率: {analysisResult.timeline.mediumTerm.probability}%</p>
              </Timeline.Item>
              <Timeline.Item color="purple">
                <p><Text strong>长期预测 (12个月)</Text></p>
                <p>目标价格: ¥{analysisResult.timeline.longTerm.price}</p>
                <p>实现概率: {analysisResult.timeline.longTerm.probability}%</p>
              </Timeline.Item>
            </Timeline>
          </Card>
        </div>
      )}

      {/* 任务详情模态框 */}
      <Modal
        title="任务详情"
        visible={isModalVisible}
        onCancel={() => setIsModalVisible(false)}
        footer={null}
        width={600}
      >
        {selectedTask && (
          <div>
            <Row gutter={[16, 16]}>
              <Col span={12}>
                <Text strong>股票代码:</Text>
                <br />
                <Text>{selectedTask.stockCode}</Text>
              </Col>
              <Col span={12}>
                <Text strong>股票名称:</Text>
                <br />
                <Text>{selectedTask.stockName}</Text>
              </Col>
              <Col span={12}>
                <Text strong>任务状态:</Text>
                <br />
                <Tag color={getStatusColor(selectedTask.status)}>
                  {selectedTask.status === 'running' ? '分析中' : 
                   selectedTask.status === 'completed' ? '已完成' : 
                   selectedTask.status === 'failed' ? '失败' : '等待中'}
                </Tag>
              </Col>
              <Col span={12}>
                <Text strong>当前进度:</Text>
                <br />
                <Progress percent={selectedTask.progress} size="small" />
              </Col>
              <Col span={24}>
                <Text strong>当前步骤:</Text>
                <br />
                <Text>{selectedTask.currentStep}</Text>
              </Col>
              <Col span={12}>
                <Text strong>开始时间:</Text>
                <br />
                <Text>{selectedTask.startTime}</Text>
              </Col>
              <Col span={12}>
                <Text strong>预计完成:</Text>
                <br />
                <Text>{selectedTask.estimatedTime}</Text>
              </Col>
            </Row>
          </div>
        )}
      </Modal>
    </div>
  );
};

export default AgentAnalysis; 