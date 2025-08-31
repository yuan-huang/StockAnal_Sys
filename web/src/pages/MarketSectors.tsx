import React from 'react';
import { Card, Row, Col, Typography, Table, Tag, Progress } from 'antd';
import { FundOutlined, FireOutlined, RiseOutlined, FallOutlined } from '@ant-design/icons';

const { Title } = Typography;

const MarketSectors: React.FC = () => {
  const sectorData = [
    {
      key: '1',
      sector: '科技板块',
      change: '+3.45%',
      volume: '456.78亿',
      strength: 85,
      status: '强势',
      hot: true,
    },
    {
      key: '2',
      sector: '新能源',
      change: '+2.87%',
      volume: '234.56亿',
      strength: 78,
      status: '强势',
      hot: true,
    },
    {
      key: '3',
      sector: '医药生物',
      change: '-1.23%',
      volume: '123.45亿',
      strength: 45,
      status: '弱势',
      hot: false,
    },
    {
      key: '4',
      sector: '消费板块',
      change: '+0.98%',
      volume: '345.67亿',
      strength: 62,
      status: '中性',
      hot: false,
    },
    {
      key: '5',
      sector: '金融板块',
      change: '-0.45%',
      volume: '567.89亿',
      strength: 38,
      status: '弱势',
      hot: false,
    },
  ];

  const columns = [
    {
      title: '板块名称',
      dataIndex: 'sector',
      key: 'sector',
      render: (sector: string, record: any) => (
        <div style={{ display: 'flex', alignItems: 'center', gap: 8 }}>
          <FundOutlined />
          <span>{sector}</span>
          {record.hot && <FireOutlined style={{ color: '#ff4d4f' }} />}
        </div>
      ),
    },
    {
      title: '涨跌幅',
      dataIndex: 'change',
      key: 'change',
      render: (change: string) => (
        <span style={{ 
          color: change.startsWith('+') ? '#52c41a' : '#ff4d4f',
          fontWeight: 'bold'
        }}>
          {change}
        </span>
      ),
    },
    {
      title: '成交量',
      dataIndex: 'volume',
      key: 'volume',
    },
    {
      title: '板块强度',
      dataIndex: 'strength',
      key: 'strength',
      render: (strength: number) => (
        <Progress 
          percent={strength} 
          size="small" 
          strokeColor={strength > 70 ? '#52c41a' : strength > 50 ? '#faad14' : '#ff4d4f'}
        />
      ),
    },
    {
      title: '状态',
      dataIndex: 'status',
      key: 'status',
      render: (status: string) => {
        let color = 'default';
        if (status === '强势') color = 'success';
        else if (status === '弱势') color = 'error';
        else if (status === '中性') color = 'warning';
        
        return <Tag color={color}>{status}</Tag>;
      },
    },
  ];

  return (
    <div>
      <Title level={2}>板块分析</Title>
      
      <Row gutter={[16, 16]} style={{ marginBottom: 24 }}>
        <Col span={6}>
          <Card>
            <div style={{ textAlign: 'center' }}>
              <RiseOutlined style={{ fontSize: 32, color: '#52c41a' }} />
              <div style={{ fontSize: 24, fontWeight: 'bold', color: '#52c41a' }}>12</div>
              <div>上涨板块</div>
            </div>
          </Card>
        </Col>
        <Col span={6}>
          <Card>
            <div style={{ textAlign: 'center' }}>
              <FallOutlined style={{ fontSize: 32, color: '#ff4d4f' }} />
              <div style={{ fontSize: 24, fontWeight: 'bold', color: '#ff4d4f' }}>8</div>
              <div>下跌板块</div>
            </div>
          </Card>
        </Col>
        <Col span={6}>
          <Card>
            <div style={{ textAlign: 'center' }}>
              <FundOutlined style={{ fontSize: 32, color: '#1890ff' }} />
              <div style={{ fontSize: 24, fontWeight: 'bold', color: '#1890ff' }}>5</div>
              <div>平盘板块</div>
            </div>
          </Card>
        </Col>
        <Col span={6}>
          <Card>
            <div style={{ textAlign: 'center' }}>
              <FireOutlined style={{ fontSize: 32, color: '#ff4d4f' }} />
              <div style={{ fontSize: 24, fontWeight: 'bold', color: '#ff4d4f' }}>3</div>
              <div>热点板块</div>
            </div>
          </Card>
        </Col>
      </Row>

      <Card title="板块行情" style={{ marginBottom: 24 }}>
        <Table 
          columns={columns} 
          dataSource={sectorData} 
          pagination={false}
          size="middle"
        />
      </Card>

      <Row gutter={[16, 16]}>
        <Col span={12}>
          <Card title="强势板块分析">
            <div style={{ padding: '16px 0' }}>
              <h4>科技板块</h4>
              <p>• 芯片概念股集体大涨，中芯国际、韦尔股份等领涨</p>
              <p>• 人工智能概念股表现活跃，科大讯飞、寒武纪等涨幅居前</p>
              <p>• 5G概念股持续走强，中兴通讯、华为概念股表现亮眼</p>
              
              <h4>新能源板块</h4>
              <p>• 光伏概念股集体大涨，隆基绿能、通威股份等领涨</p>
              <p>• 新能源汽车概念股表现活跃，比亚迪、宁德时代等涨幅居前</p>
              <p>• 储能概念股持续走强，阳光电源、亿纬锂能等表现亮眼</p>
            </div>
          </Card>
        </Col>
        <Col span={12}>
          <Card title="弱势板块分析">
            <div style={{ padding: '16px 0' }}>
              <h4>医药生物</h4>
              <p>• 创新药概念股集体回调，恒瑞医药、复星医药等领跌</p>
              <p>• 医疗器械概念股表现低迷，迈瑞医疗、乐普医疗等跌幅居前</p>
              <p>• 生物疫苗概念股持续走弱，智飞生物、康泰生物等表现不佳</p>
              
              <h4>金融板块</h4>
              <p>• 银行股集体回调，招商银行、平安银行等领跌</p>
              <p>• 保险股表现低迷，中国平安、中国人寿等跌幅居前</p>
              <p>• 券商股持续走弱，中信证券、华泰证券等表现不佳</p>
            </div>
          </Card>
        </Col>
      </Row>
    </div>
  );
};

export default MarketSectors; 