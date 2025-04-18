import plotly.graph_objects as go
import pandas as pd
import networkx as nx


def read_excel_file(file_path):
    try:
        return pd.read_excel(file_path)
    except FileNotFoundError:
        print(f"Error: File {file_path} not found.")
        return None
    except Exception as e:
        print(f"Error: {e}")
        return None


def generate_graph(nodes_file, edges_file, layout_k=0.5, node_color='Blue', node_size=10):
    # 读取顶点表
    nodes_df = read_excel_file(nodes_file)
    if nodes_df is None:
        return None

    # 读取边表
    edges_df = read_excel_file(edges_file)
    if edges_df is None:
        return None

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

    pos = nx.spring_layout(G, k=layout_k)

    edge_x, edge_y = [], []
    for edge in G.edges():
        x0, y0 = pos[edge[0]]
        x1, y1 = pos[edge[1]]
        edge_x.extend([x0, x1, None])
        edge_y.extend([y0, y1, None])

    edge_trace = go.Scatter(
        x=edge_x, y=edge_y,
        line=dict(width=0.5, color='#888'),
        hoverinfo='none',
        mode='lines')

    node_x, node_y, node_text = [], [], []
    for node in G.nodes():
        x, y = pos[node]
        node_x.append(x)
        node_y.append(y)
        node_text.append(G.nodes[node]['name'])

    node_trace = go.Scatter(
        x=node_x, y=node_y,
        mode='markers+text',
        hoverinfo='text',
        text=node_text,
        textposition="top center",
        marker=dict(
            showscale=False,
            color=node_color,
            size=node_size,
            line_width=2))

    edge_labels = nx.get_edge_attributes(G, 'weight')
    edge_label_x, edge_label_y, edge_label_text = [], [], []
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
                            font=dict(size=16)
                        ),
                        showlegend=False,
                        hovermode='closest',
                        margin=dict(b=20, l=5, r=5, t=40)))
    fig.show()

    return G


def name_to_id(G, name):
    for node, data in G.nodes(data=True):
        if data['name'] == name:
            return node
    return None


def find_shortest_path(G, source_name, target_name):
    source_id = name_to_id(G, source_name)
    target_id = name_to_id(G, target_name)

    if source_id is None:
        print(f"未找到名为 {source_name} 的顶点。")
        return
    if target_id is None:
        print(f"未找到名为 {target_name} 的顶点。")
        return

    try:
        shortest_path = nx.dijkstra_path(G, source_id, target_id, weight='weight')
        path_length = nx.dijkstra_path_length(G, source_id, target_id, weight='weight')
        node_names = [G.nodes[node]['name'] for node in shortest_path]
        print(f"最短路径: {' -> '.join(map(str, node_names))}")
        print(f"路径长度: {path_length} 公里")
    except nx.NetworkXNoPath:
        print(f"从顶点 {source_name} 到顶点 {target_name} 没有路径。")


if __name__ == "__main__":
    nodes_file = 'nodes.xlsx'
    edges_file = 'edges.xlsx'
    G = generate_graph(nodes_file, edges_file)
    if G is not None:
        source_name = input("请输入起始顶点的名称: ")
        target_name = input("请输入终止顶点的名称: ")
        find_shortest_path(G, source_name, target_name)
