import redis

try:
    # 连接Redis
    r = redis.Redis(host='localhost', port=6379, db=0)
    print('Redis连接测试成功')
    
    # 测试HMSET命令
    r.hmset('test_key', {'field1': 'value1', 'field2': 'value2'})
    print('HMSET命令测试成功')
    
    # 测试ZADD命令（Redis 3.x语法）
    r.zadd('test_sorted_set', 1.0, 'member1')
    print('ZADD命令测试成功')
    
    # 清理测试数据
    r.delete('test_key', 'test_sorted_set')
    print('清理测试数据完成')
    
except Exception as e:
    print(f'Redis测试失败: {e}') 