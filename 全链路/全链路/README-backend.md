# 农产品全链路管理系统后端

这个后端服务从管理者的角度提供农户和运输数据的分析功能，并能直接生成分析图片。

## 功能特性

- **农户分析**: 生成农户数据分析图表，包括地区分布、作物类型、质量评分等
- **运输分析**: 生成运输数据分析图表，包括路线成本、运输方式、效率评分等
- **综合分析**: 生成全链路综合分析报告，包含热力图、效率对比等

## 安装依赖

```bash
pip install -r requirements.txt
```

## 运行服务

```bash
python backend.py
```

服务将在 http://localhost:5000 启动

## API 端点

### 主页
- `GET /` - API 文档和可用端点列表

### 分析图片生成
- `GET /api/analysis/farmers` - 生成农户分析图片
- `GET /api/analysis/transport` - 生成运输分析图片
- `GET /api/analysis/comprehensive` - 生成综合分析图片

### 数据接口
- `GET /api/data/farmers` - 获取农户数据 (JSON)
- `GET /api/data/transport` - 获取运输数据 (JSON)

## 使用示例

在浏览器中访问以下URL来获取分析图片：

1. 农户分析: http://localhost:5000/api/analysis/farmers
2. 运输分析: http://localhost:5000/api/analysis/transport
3. 综合分析: http://localhost:5000/api/analysis/comprehensive

## 数据说明

系统使用模拟数据，包括：
- 50个农户的数据（地区、作物类型、种植面积、产量、质量评分等）
- 100条运输记录（路线、距离、重量、成本、时间、运输方式等）

## 技术栈

- Flask - Web框架
- Matplotlib - 图表生成
- Seaborn - 统计图表
- Pandas - 数据处理
- NumPy - 数值计算

## 扩展说明

在生产环境中，可以：
1. 连接真实数据库替换模拟数据
2. 添加用户认证和权限管理
3. 实现数据上传和实时更新
4. 添加更多分析维度和图表类型