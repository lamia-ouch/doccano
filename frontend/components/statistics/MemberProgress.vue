<template>
  <v-card>
    <v-card-title>Member's Progress</v-card-title>
    <v-divider />
    <v-card-text>
      <div
        v-for="(item, index) in stats.progress"
        :key="index"
        class="mb-2"
      >
        <span class="font-weight-medium">{{ item.user }}</span>
        <span class="font-weight-medium">{{ item.done }} / {{ stats.total }}</span>
        <v-progress-linear :value="rate(item.done, stats.total)" />
      </div>
    </v-card-text>
  </v-card>
</template>

<script lang="ts">
import Vue from 'vue'
export default Vue.extend({
  data() {
    return {
      stats: {}
    }
  },

  async created() {
    this.stats = await this.$services.statistics.fetchMemberProgress(this.$route.params.id)
  },

  methods: {
    rate(done: number, total: number) {
      return done / total * 100
    }
  }
})
</script>
