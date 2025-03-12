import pandas as pd


def process_call_auction_data(df):
    df = df.sort_values(by='price', ascending=False)
    df['limit_up_price'] = df.apply(lambda row: row['pre_close'] * (1.1 if not (1.098 <= row['price'] / row['pre_close'] < 1.1) and not row['ts_code'].startswith(('300', '301', '688', '8')) else 1.2 if not (1.198 <= row['price'] / row['pre_close'] < 1.2) and row['ts_code'].startswith(('300', '301', '688')) else 1.3 if not (1.298 <= row['price'] / row['pre_close'] < 1.3) and row['ts_code'].startswith('8') else row['price'] / row['pre_close']), axis=1)
    df = df[df['price'] >= df['limit_up_price']]
    df['auction_gain'] = ((df['price'] - df['pre_close']) / df['pre_close']) * 100
    df['auction_gain'] = df['auction_gain'].round(2)
    def get_concept_links(ts_code):
        # 这里需要实现从同花顺概念表及成分股表查询所属概念的逻辑
        # 假设返回一个包含概念名称和链接的列表，例如 [('概念1', '/concept/1'), ('概念2', '/concept/2')]
        # 这里暂时保留原逻辑，后续可根据实际情况修改
        return ''
    df['所属概念'] = df['ts_code'].apply(get_concept_links)
    df = df[['ts_code', 'stock_name', 'price', 'pre_close', 'vol', 'amount', 'auction_gain', '所属概念']]
    return df