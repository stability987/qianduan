#!/usr/bin/env python3
"""
backend.py - 农产品全链路管理系统后端
从管理者的角度分析农户和运输数据，并生成分析图片
"""

from flask import Flask, send_file, jsonify
import matplotlib
matplotlib.use('Agg')  # 使用非GUI后端
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
import io
import base64
from datetime import datetime, timedelta

app = Flask(__name__)

# 设置matplotlib使用中文字体（如果需要）
plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号

# 模拟农户数据
def generate_farmer_data():
    """生成模拟农户数据"""
    farmers = []
    regions = ['云南大理', '江西赣州', '山东烟台', '新疆阿克苏', '浙江杭州', '内蒙古', '河北承德']

    for i in range(50):
        farmer = {
            'id': f'F{i+1:03d}',
            'name': f'农户{i+1}',
            'region': np.random.choice(regions),
            'crop_type': np.random.choice(['葡萄', '脐橙', '车厘子', '核桃', '杏仁', '腰果', '茶叶', '糙米', '杂粮', '燕麦']),
            'area': np.random.uniform(5, 100),  # 种植面积（亩）
            'yield': np.random.uniform(1000, 50000),  # 年产量（kg）
            'quality_score': np.random.uniform(70, 100),  # 质量评分
            'certifications': np.random.choice(['有机', '绿色', '地理标志', '无'], p=[0.3, 0.4, 0.2, 0.1])
        }
        farmers.append(farmer)

    return pd.DataFrame(farmers)

# 模拟运输数据
def generate_transport_data():
    """生成模拟运输数据"""
    transports = []
    routes = ['云南-北京', '江西-上海', '山东-广州', '新疆-深圳', '浙江-杭州本地', '内蒙古-天津', '河北-石家庄']

    for i in range(100):
        transport = {
            'id': f'T{i+1:03d}',
            'route': np.random.choice(routes),
            'distance': np.random.uniform(500, 3000),  # 距离（km）
            'weight': np.random.uniform(1000, 50000),  # 运输重量（kg）
            'cost': np.random.uniform(500, 15000),  # 运输成本（元）
            'time': np.random.uniform(1, 7),  # 运输时间（天）
            'method': np.random.choice(['公路', '铁路', '航空'], p=[0.7, 0.2, 0.1]),
            'efficiency_score': np.random.uniform(60, 100)  # 效率评分
        }
        transports.append(transport)

    return pd.DataFrame(transports)

# 全局数据
farmer_df = generate_farmer_data()
transport_df = generate_transport_data()

@app.route('/')
def index():
    """主页"""
    return jsonify({
        'message': '农产品全链路管理系统后端API',
        'endpoints': {
            '农户分析': '/api/analysis/farmers',
            '运输分析': '/api/analysis/transport',
            '综合报告': '/api/analysis/comprehensive'
        }
    })

@app.route('/api/analysis/farmers')
def farmer_analysis():
    """生成农户分析图片"""
    fig, axes = plt.subplots(2, 2, figsize=(12, 10))
    fig.suptitle('农户数据分析报告', fontsize=16, fontweight='bold')

    # 1. 各地区农户数量分布
    region_counts = farmer_df['region'].value_counts()
    axes[0,0].bar(region_counts.index, region_counts.values, color='skyblue')
    axes[0,0].set_title('各地区农户数量分布')
    axes[0,0].set_ylabel('农户数量')
    axes[0,0].tick_params(axis='x', rotation=45)

    # 2. 作物类型分布
    crop_counts = farmer_df['crop_type'].value_counts()
    axes[0,1].pie(crop_counts.values, labels=crop_counts.index, autopct='%1.1f%%')
    axes[0,1].set_title('作物类型分布')

    # 3. 种植面积 vs 产量散点图
    colors = {'有机': 'green', '绿色': 'lightgreen', '地理标志': 'orange', '无': 'gray'}
    cert_colors = farmer_df['certifications'].map(colors)
    axes[1,0].scatter(farmer_df['area'], farmer_df['yield'], c=cert_colors, alpha=0.6)
    axes[1,0].set_title('种植面积 vs 年产量')
    axes[1,0].set_xlabel('种植面积（亩）')
    axes[1,0].set_ylabel('年产量（kg）')

    # 4. 质量评分分布
    axes[1,1].hist(farmer_df['quality_score'], bins=20, color='lightcoral', edgecolor='black')
    axes[1,1].set_title('产品质量评分分布')
    axes[1,1].set_xlabel('质量评分')
    axes[1,1].set_ylabel('频次')

    plt.tight_layout()

    # 保存到内存
    buf = io.BytesIO()
    plt.savefig(buf, format='png', dpi=150, bbox_inches='tight')
    buf.seek(0)
    plt.close()

    return send_file(buf, mimetype='image/png')

@app.route('/api/analysis/transport')
def transport_analysis():
    """生成运输分析图片"""
    fig, axes = plt.subplots(2, 2, figsize=(12, 10))
    fig.suptitle('运输数据分析报告', fontsize=16, fontweight='bold')

    # 1. 运输路线成本分析
    route_costs = transport_df.groupby('route')['cost'].mean().sort_values()
    axes[0,0].barh(route_costs.index, route_costs.values, color='salmon')
    axes[0,0].set_title('各路线平均运输成本')
    axes[0,0].set_xlabel('平均成本（元）')

    # 2. 运输方式分布
    method_counts = transport_df['method'].value_counts()
    axes[0,1].pie(method_counts.values, labels=method_counts.index, autopct='%1.1f%%')
    axes[0,1].set_title('运输方式分布')

    # 3. 距离 vs 成本关系
    colors = {'公路': 'blue', '铁路': 'green', '航空': 'red'}
    method_colors = transport_df['method'].map(colors)
    axes[1,0].scatter(transport_df['distance'], transport_df['cost'], c=method_colors, alpha=0.6)
    axes[1,0].set_title('运输距离 vs 成本')
    axes[1,0].set_xlabel('距离（km）')
    axes[1,0].set_ylabel('成本（元）')

    # 4. 运输效率评分分布
    axes[1,1].hist(transport_df['efficiency_score'], bins=20, color='lightblue', edgecolor='black')
    axes[1,1].set_title('运输效率评分分布')
    axes[1,1].set_xlabel('效率评分')
    axes[1,1].set_ylabel('频次')

    plt.tight_layout()

    # 保存到内存
    buf = io.BytesIO()
    plt.savefig(buf, format='png', dpi=150, bbox_inches='tight')
    buf.seek(0)
    plt.close()

    return send_file(buf, mimetype='image/png')

@app.route('/api/analysis/comprehensive')
def comprehensive_analysis():
    """生成综合分析图片"""
    fig, axes = plt.subplots(3, 2, figsize=(15, 12))
    fig.suptitle('农产品全链路综合分析报告', fontsize=18, fontweight='bold')

    # 1. 农户区域分布热力图
    region_crop = pd.crosstab(farmer_df['region'], farmer_df['crop_type'])
    sns.heatmap(region_crop, annot=True, fmt='d', cmap='YlOrRd', ax=axes[0,0])
    axes[0,0].set_title('各地区作物分布热力图')
    axes[0,0].tick_params(axis='x', rotation=45)

    # 2. 运输成本效率分析
    transport_df['cost_per_km'] = transport_df['cost'] / transport_df['distance']
    transport_df['time_efficiency'] = transport_df['weight'] / transport_df['time']

    axes[0,1].scatter(transport_df['cost_per_km'], transport_df['efficiency_score'], alpha=0.6, color='purple')
    axes[0,1].set_title('运输成本效率 vs 评分')
    axes[0,1].set_xlabel('成本/公里（元/km）')
    axes[0,1].set_ylabel('效率评分')

    # 3. 农户质量与产量关系
    quality_yield = farmer_df.groupby(pd.cut(farmer_df['quality_score'], bins=5))['yield'].mean()
    quality_yield.plot(kind='bar', ax=axes[1,0], color='green')
    axes[1,0].set_title('质量评分区间平均产量')
    axes[1,0].set_xlabel('质量评分区间')
    axes[1,0].set_ylabel('平均产量（kg）')
    axes[1,0].tick_params(axis='x', rotation=45)

    # 4. 运输方式对比
    method_stats = transport_df.groupby('method').agg({
        'cost': 'mean',
        'time': 'mean',
        'efficiency_score': 'mean'
    })
    method_stats.plot(kind='bar', ax=axes[1,1])
    axes[1,1].set_title('运输方式综合对比')
    axes[1,1].set_ylabel('平均值')
    axes[1,1].legend(['平均成本', '平均时间', '平均效率'])

    # 5. 地区农产品价值分析
    farmer_df['estimated_value'] = farmer_df['yield'] * farmer_df['quality_score'] / 10  # 简化的价值估算
    region_value = farmer_df.groupby('region')['estimated_value'].sum().sort_values(ascending=False)
    region_value.plot(kind='bar', ax=axes[2,0], color='orange')
    axes[2,0].set_title('各地区农产品估算总价值')
    axes[2,0].set_ylabel('估算价值')
    axes[2,0].tick_params(axis='x', rotation=45)

    # 6. 供应链效率综合指标
    # 计算综合效率评分
    farmer_df['farmer_efficiency'] = (farmer_df['yield'] / farmer_df['area']) * (farmer_df['quality_score'] / 100)
    transport_df['transport_efficiency'] = transport_df['efficiency_score'] / transport_df['time']

    overall_efficiency = {
        '农户平均效率': farmer_df['farmer_efficiency'].mean(),
        '运输平均效率': transport_df['transport_efficiency'].mean(),
        '供应链综合效率': (farmer_df['farmer_efficiency'].mean() + transport_df['transport_efficiency'].mean()) / 2
    }

    axes[2,1].bar(overall_efficiency.keys(), overall_efficiency.values(), color=['lightblue', 'lightgreen', 'gold'])
    axes[2,1].set_title('供应链效率综合指标')
    axes[2,1].set_ylabel('效率评分')
    axes[2,1].tick_params(axis='x', rotation=45)

    plt.tight_layout()

    # 保存到内存
    buf = io.BytesIO()
    plt.savefig(buf, format='png', dpi=150, bbox_inches='tight')
    buf.seek(0)
    plt.close()

    return send_file(buf, mimetype='image/png')

@app.route('/api/data/farmers')
def get_farmer_data():
    """获取农户数据JSON"""
    return jsonify(farmer_df.to_dict('records'))

@app.route('/api/data/transport')
def get_transport_data():
    """获取运输数据JSON"""
    return jsonify(transport_df.to_dict('records'))

if __name__ == '__main__':
    print("启动农产品全链路管理系统后端...")
    print("访问 http://localhost:5000 查看API文档")
    print("农户分析图片: http://localhost:5000/api/analysis/farmers")
    print("运输分析图片: http://localhost:5000/api/analysis/transport")
    print("综合分析图片: http://localhost:5000/api/analysis/comprehensive")
    app.run(debug=True, host='0.0.0.0', port=5000)