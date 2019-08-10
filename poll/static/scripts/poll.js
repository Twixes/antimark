/* eslint-disable no-new */
/* globals Vue */

Vue.component('spinner', {
  props: {
    loading: { type: Boolean, required: true }
  },
  data() {
    return {
      transitionDuration: getComputedStyle(document.body).getPropertyValue('--time--short').replace('ms', '').trim()
    }
  },
  template: `
    <transition appear name="spinner" v-bind:duration="transitionDuration">
      <div class='spinner' v-if="loading"></div>
    </transition>
  `
})

new Vue({
  el: '#app',
  data: {
    loading: true
  },
  computed: {},
  methods: {},
  mounted() {},
  template: `
    <spinner v-bind:loading="loading"></spinner>
  `
})
