import plotly.graph_objects as go
import pandas as pd
import networkx as nx


def read_excel_file(file_path):
    try:
        return pd.read_excel(file_path, engine='openpyxl')
    except FileNotFoundError:
        print(f"Error: File {file_path} not found.")
        return None
    except Exception as e:
        print(f"Error: {e}")
        return None


def generate_graph(nodes_file, edges_file, layout_k=0.5, node_color='Blue', node_size=10):
    nodes_df = read_excel_file(nodes_file)
    if nodes_df is None:
        return None

    edges_df = read_excel_file(edges_file)
    if edges_df is None:
        return None

    G = nx.Graph()

    for index, row in nodes_df.iterrows():
        node_id = row['序号']
        node_name = row['顶点名称']
        G.add_node(node_id, name=node_name)

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


def find_unvisited_attractions(G, current_attraction):
    current_id = name_to_id(G, current_attraction)
    if current_id is None:
        print(f"未找到名为 {current_attraction} 的顶点。")
        return

    try:
        visited_df = read_excel_file('visited.xlsx')
        visited_ids = visited_df['已走过'].tolist()
    except (FileNotFoundError, AttributeError):
        visited_ids = []

    unvisited = []
    for node in G.nodes():
        if node in visited_ids or node == current_id:
            continue
        node_name = G.nodes[node]['name']
        try:
            path_length = nx.dijkstra_path_length(G, current_id, node, weight='weight')
            unvisited.append((node_name, path_length))
        except nx.NetworkXNoPath:
            continue

    unvisited.sort(key=lambda x: x[1])
    print("未走过的景点（按路程排序）:")
    for attraction, distance in unvisited:
        print(f"{attraction}: {distance} 公里")


def add_visited_manual(G):
    name = input("请输入走过景点的名称: ")
    node_id = name_to_id(G, name)
    if node_id is None:
        print(f"未找到名为 {name} 的顶点。")
        return
    visited_df = pd.DataFrame({'已走过': [node_id]})
    try:
        existing_df = read_excel_file('visited.xlsx')
        new_df = pd.concat([existing_df, visited_df]).drop_duplicates()
        new_df.to_excel('visited.xlsx', index=False)
    except FileNotFoundError:
        visited_df.to_excel('visited.xlsx', index=False)
    print(f"{name} 的序号 {node_id} 已成功记录到已走过列表。")


def print_visited_attractions(G):
    try:
        visited_df = read_excel_file('visited.xlsx')
        visited_ids = visited_df['已走过'].tolist()
        visited_names = []
        for node_id in visited_ids:
            if node_id in G.nodes():
                visited_names.append(G.nodes[node_id]['name'])
        if visited_names:
            print("已走过的景点:")
            for name in visited_names:
                print(name)
        else:
            print("目前还没有记录已走过的景点。")
    except FileNotFoundError:
        print("目前还没有记录已走过的景点。")


def show_menu():
    print("\n菜单:")
    print("1. 查找最短路径")
    print("2. 查找未走过的景点")
    print("3. 手动添加走过的景点")
    print("4. 打印已走过的景点")
    print("5. 退出")


if __name__ == "__main__":
    nodes_file = 'nodes.xlsx'
    edges_file = 'edges.xlsx'
    G = generate_graph(nodes_file, edges_file)
    if G is not None:
        while True:
            show_menu()
            choice = input("请输入你的选择: ")
            if choice == '1':
                source_name = input("请输入起始顶点的名称: ")
                target_name = input("请输入终止顶点的名称: ")
                find_shortest_path(G, source_name, target_name)
            elif choice == '2':
                current_attraction = input("请输入当前景点的名称: ")
                find_unvisited_attractions(G, current_attraction)
            elif choice == '3':
                add_visited_manual(G)
            elif choice == '4':
                print_visited_attractions(G)
            elif choice == '5':
                break
            else:
                print("无效的选择，请重新输入。")

