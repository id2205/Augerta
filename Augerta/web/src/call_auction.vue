<template>
  <div>
    <h1>竞价涨停数据 - {{ date }}</h1>
    <table>
      <thead>
        <tr>
          <th>股票代码</th>
          <th>股票名称</th>
          <th>价格</th>
          <th>前收盘价</th>
          <th>成交量</th>
          <th>成交额</th>
          <th>竞价涨幅</th>
          <th>所属概念</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="item in callAuctionData" :key="item.ts_code">
          <td>{{ item.ts_code }}</td>
          <td>{{ item.stock_name }}</td>
          <td>{{ item.price }}</td>
          <td>{{ item.pre_close }}</td>
          <td>{{ item.vol }}</td>
          <td>{{ item.amount }}</td>
          <td>{{ item.auction_gain }}</td>
          <td v-html="item['所属概念']"></td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { get_call_auction_data } from '@/api/call_auction_api'
import { process_call_auction_data } from '@/store/call_auction_store'
import { useRoute } from 'vue-router'

const date = ref('')
const callAuctionData = ref([])

const fetchCallAuctionData = async () => {
  try {
    const data = await get_call_auction_data(date.value)
    const processedData = process_call_auction_data(data)
    callAuctionData.value = processedData
  } catch (error) {
    console.error('获取竞价数据失败:', error)
  }
}

onMounted(() => {
  const route = useRoute()
  // 这里可以根据实际情况设置日期
  // date.value = '2025-01-01'
  date.value = route.query.date || '2025-01-01'
  fetchCallAuctionData()
})
</script>

<style scoped>
/* 可以添加一些样式 */
</style>