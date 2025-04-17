import plotly.graph_objects as go
import pandas as pd
import networkx as nx

def generate_graph(nodes_file, edges_file):
    # 读取顶点表
    nodes_df = pd.read_excel(nodes_file)
    # 读取边表
    edges_df = pd.read_excel(edges_file)

    # 创建一个无向图
    G = nx.Graph()

    # 添加顶点到图中
    for index, row in nodes_df.iterrows():
        node_id = row['序号']
        node_name = row['顶点名称']
        G.add_node(node_id, name=node_name)

    # 添加边到图中
    for index, row in edges_df.iterrows():
        source = row['起始节点']
        target = row['终止节点']
        weight = row['权重(公里)']
        G.add_edge(source, target, weight=weight)

    pos = nx.spring_layout(G, k=0.5)

    edge_x = []
    edge_y = []
    for edge in G.edges():
        x0, y0 = pos[edge[0]]
        x1, y1 = pos[edge[1]]
        edge_x.append(x0)
        edge_x.append(x1)
        edge_x.append(None)
        edge_y.append(y0)
        edge_y.append(y1)
        edge_y.append(None)

    edge_trace = go.Scatter(
        x=edge_x, y=edge_y,
        line=dict(width=0.5, color='#888'),
        hoverinfo='none',
        mode='lines')

    node_x = []
    node_y = []
    for node in G.nodes():
        x, y = pos[node]
        node_x.append(x)
        node_y.append(y)

    node_trace = go.Scatter(
        x=node_x, y=node_y,
        mode='markers',
        hoverinfo='text',
        marker=dict(
            showscale=False,
            color='Blue',
            size=10,
            line_width=2))

    node_text = []
    for node in G.nodes():
        node_text.append(G.nodes[node]['name'])
    node_trace.text = node_text

    edge_labels = nx.get_edge_attributes(G, 'weight')
    edge_label_x = []
    edge_label_y = []
    edge_label_text = []
    for edge in G.edges():
        x0, y0 = pos[edge[0]]
        x1, y1 = pos[edge[1]]
        x_mid = (x0 + x1) / 2
        y_mid = (y0 + y1) / 2
        edge_label_x.append(x_mid)
        edge_label_y.append(y_mid)
        edge_label_text.append(edge_labels[edge])

    edge_label_trace = go.Scatter(
        x=edge_label_x, y=edge_label_y,
        mode='text',
        text=edge_label_text,
        textposition="middle center")

    fig = go.Figure(data=[edge_trace, node_trace, edge_label_trace],
                    layout=go.Layout(
                        title=go.layout.Title(
                            text='Graph from Tables',
                            font=dict(size=16)  # 在这里设置标题字体大小等属性
                        ),
                        showlegend=False,
                        hovermode='closest',
                        margin=dict(b=20, l=5, r=5, t=40)))
    fig.show()

    return G

if __name__ == "__main__":
    nodes_file = 'nodes.xlsx'
    edges_file = 'edges.xlsx'
    generate_graph(nodes_file, edges_file)