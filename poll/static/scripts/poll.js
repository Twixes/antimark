/* eslint-env browser */
/* eslint-disable no-new, space-before-function-paren */
/* globals Vue, Vuex, gettext, gettext_noop, ngettext, npgettext, pgettext */

const dummySchool = {
  nomenclature: 'teachers'
}

const dummyTeachers = [
  {
    id: 2,
    title: 'Pani',
    first_name: 'Maria',
    last_name: 'Skłodowska–Curie',
    subject: 'fizyka'
  },
  {
    id: 1,
    title: 'Pan',
    first_name: 'Jan',
    last_name: 'Miodek',
    subject: 'polski'
  },
  {
    id: 4,
    title: 'Pan',
    first_name: 'Adam',
    last_name: 'Nawałka',
    subject: 'wychowanie fizyczne'
  }
]

const dummyQuestions = [
  {
    id: 2,
    position: 1,
    text: 'Ocenia sprawiedliwie'
  },
  {
    id: 3,
    position: 2,
    text: 'Przestrzega statutu szkoły'
  }
]

const dummyGroups = [
  {
    id: 3,
    name: '3A',
    number_of_students: 27
  }
]

const store = new Vuex.Store({
  state: {
    isLoadingInProgress: true,
    hasSurveyBegan: false,
    haveSelectionsBeenMade: false,
    shouldMissingSelectionsBeHighlighted: false,
    currentQuestionPosition: 1,
    school: dummySchool,
    teachers: dummyTeachers,
    questions: dummyQuestions,
    groups: dummyGroups,
    completion: {
      groupId: null,
      answers: {}
    }
  },
  mutations: {
    beginSurvey(state) {
      state.hasSurveyBegan = true
    },
    loadInitialData(state) {
      state.isLoadingInProgress = false
    },
    setUpAnswers(state) {
      // TODO: make this proper
      for (const question of state.questions) {
        Vue.set(state.completion.answers, question.id, {})
        for (const teacher of state.teachers) {
          Vue.set(state.completion.answers[question.id], teacher.id, null)
        }
      }
    },
    setGroupId(state, groupId) {
      // TODO: make this proper
      state.haveSelectionsBeenMade = true
      Vue.set(state.completion, 'groupId', groupId)
    },
    updateMark(state, { questionId, teacherId, mark }) {
      state.haveSelectionsBeenMade = true
      Vue.set(state.completion.answers[questionId], teacherId, mark)
    }
  }
})

Vue.component('landing', {
  methods: {
    ...Vuex.mapMutations(['beginSurvey']),
    gettext: () => gettext('Professors have been grading your work the whole academic&nbsp;year.')
  },
  template: `
    <div class="v-stack compact">
      <h1>
        <template v-if="$store.state.school.nomenclature == 'professors'">
          ${gettext('Professors have been grading your work the whole academic&nbsp;year.')}
        </template>
        <template v-else>
          ${gettext('Teachers have been grading your work the whole school&nbsp;year.')}
        </template>
        <br>${gettext('Now you grade theirs.')}
      </h1>
      <button class="forward" @click="beginSurvey">${gettext('Begin')}</button>
    </div>
  `
})

Vue.component('spinner', {
  template: `
    <div class='spinner'></div>
  `
})

Vue.component('mark-select', {
  props: {
    questionId: {
      type: Number,
      required: true
    },
    teacher: {
      type: Object,
      required: true
    }
  },
  computed: {
    ...Vuex.mapState({
      highlightMissingSelection: state => state.highlightMissingSelection,
      completionAnswers: state => state.completion.answers
    }),
    specifier() {
      return `teacher-${this.teacher.id}`
    },
    selected: {
      get() {
        return this.completionAnswers[this.questionId][this.teacher.id]
      },
      set(mark) {
        this.updateMark({ questionId: this.questionId, teacherId: this.teacher.id, mark: parseInt(mark) })
      }
    }
  },
  methods: {
    ...Vuex.mapMutations(['updateMark']),
    composeMarkInputId(mark) {
      return `${this.specifier}-mark-${mark}`
    }
  },
  template: `
    <div class="mark-select">
      <div class="info">
        <div class="name">{{ teacher.title }} {{ teacher.first_name }} {{ teacher.last_name }}</div>
        <div class="subject">{{ teacher.subject }}</div>
       </div>
      <div class="marks" :class="{ 'missing-selection': highlightMissingSelection && selected === null }">
        <template v-for="mark in [0, 1, 2]">
          <input :id="composeMarkInputId(mark)" type="radio" :name="specifier" :value="mark" v-model="selected">
          <label :for="composeMarkInputId(mark)">{{ mark }}</label>
        </template>
        <div class="highlight"></div>
      </div>
    </div>
  `
})

Vue.component('question-step', {
  props: {
    teachers: {
      type: Array,
      required: true
    }
  },
  computed: Vuex.mapState({
    currentQuestion(state) {
      for (const question of state.questions) if (question.position === state.currentQuestionPosition) return question
      throw new RangeError(`Cannot get question with position ${state.currentQuestionPosition}`)
    }
  }),
  template: `
    <div class="step v-stack">
      <transition name="fade" mode="out-in" :duration="$store.state.timeShort">
        <h1 :key="currentQuestion.id">{{ currentQuestion.text }}</h1>
      </transition>
      <div class="teachers">
        <mark-select
          v-for="teacher in teachers"
          :questionId="currentQuestion.id"
          :teacher="teacher"
          :key="\`teacher-\${teacher.id}\`"
        ></mark-select>
      </div>
    </div>
  `
})

new Vue({
  store,
  el: 'main',
  data: {
    timeShort: parseInt(getComputedStyle(document.body).getPropertyValue('--time--short').replace('ms', '').trim())
  },
  methods: {
    gettext: gettext
  },
  created() {
    this.$store.commit('setGroupId', 3)
    this.$store.commit('setUpAnswers')
  },
  mounted() {
    addEventListener('beforeunload', event => {
      if (this.$store.state.haveSelectionsBeenMade) {
        event.preventDefault()
        event.returnValue = ''
      }
    })
    setTimeout(this.$store.commit, 1200, 'loadInitialData')
  },
  template: `
    <main class="responsive-content">
      <transition name="fade" mode="out-in" :duration="$root.timeShort">
        <landing
          v-if="!$store.state.hasSurveyBegan"
        ></landing>
        <spinner
          v-if="$store.state.hasSurveyBegan && $store.state.isLoadingInProgress"
        ></spinner>
        <question-step
          v-if="$store.state.hasSurveyBegan && !$store.state.isLoadingInProgress"
          :teachers="$store.state.teachers"
        ></question-step>
      </transition>
    </main>
  `
})
