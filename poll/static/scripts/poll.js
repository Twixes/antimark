/* eslint-env browser */
/* eslint-disable no-new, space-before-function-paren */
/* globals Vue */

Vue.component('spinner', {
  template: `
    <div class='spinner'></div>
  `
})

new Vue({
  el: 'main',
  data: {
    loading: true,
    timeShort: parseInt(getComputedStyle(document.body).getPropertyValue('--time--short').replace('ms', '').trim())
  },
  methods: {},
  mounted() {},
  template: `
    <main>
      <transition appear name="fade" mode="out-in" v-bind:duration="timeShort">
        <spinner v-if="loading"></spinner>
        <h1 v-if="!loading">Hello</h1>
      </transition>
    </main>
  `
})
