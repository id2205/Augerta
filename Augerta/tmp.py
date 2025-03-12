# 导入tushare
import tushare as ts
# 初始化pro接口
pro = ts.pro_api('gx03013e909f633ecb66722df66b360f070426613316ebf06ecd3482')

# 拉取数据
df = pro.kpl_list(trade_date='20240927', tag='涨停', fields='ts_code,name,trade_date,tag,theme,status')
print(df)