<template>
  <v-list dense>
    <v-btn
      color="ms-4 my-1 mb-2 primary text-capitalize"
      nuxt
      @click="toLabeling"
    >
      <v-icon left>
        {{ mdiPlayCircleOutline }}
      </v-icon>
      {{ $t('home.startAnnotation') }}
    </v-btn>
    <v-list-item-group
      v-model="selected"
      mandatory
    >
      <v-list-item
        v-for="(item, i) in filteredItems"
        :key="i"
        @click="$router.push(localePath(`/projects/${$route.params.id}/${item.link}`))"
      >
        <v-list-item-action>
          <v-icon>
            {{ item.icon }}
          </v-icon>
        </v-list-item-action>
        <v-list-item-content>
          <v-list-item-title>
            {{ item.text }}
          </v-list-item-title>
        </v-list-item-content>
      </v-list-item>
    </v-list-item-group>
  </v-list>
</template>

<script>
import { mdiHome, mdiDatabase, mdiCog, mdiChartBar, mdiBookOpenOutline, mdiCommentAccountOutline, mdiLabel, mdiAccount, mdiPlayCircleOutline } from '@mdi/js'

export default {
  props: {
    link: {
      type: String,
      default: '',
      required: true
    },
    role: {
      type: Object,
      default: () => {},
      required: true
    },
    project: {
      type: Object,
      default: () => {},
      required: true
    }
  },

  data() {
    return {
      selected: 0,
      mdiPlayCircleOutline
    }
  },

  computed: {
    filteredItems() {
      const items = [
        {
          icon: mdiHome,
          text: this.$t('projectHome.home'),
          link: '',
          isVisible: true
        },
        {
          icon: mdiDatabase,
          text: this.$t('dataset.dataset'),
          link: 'dataset',
          isVisible: true
        },
        {
          icon: mdiLabel,
          text: this.$t('labels.labels'),
          link: 'labels',
          isVisible: this.role.is_project_admin && this.project.canDefineLabel
        },
        {
          icon: mdiLabel,
          text: 'Relations',
          link: 'links',
          isVisible: this.role.is_project_admin && this.project.canDefineRelation
        },
        {
          icon: mdiAccount,
          text: this.$t('members.members'),
          link: 'members',
          isVisible: this.role.is_project_admin
        },
        {
          icon: mdiCommentAccountOutline,
          text: 'Comments',
          link: 'comments',
          isVisible: this.role.is_project_admin
        },
        {
          icon: mdiBookOpenOutline,
          text: this.$t('guideline.guideline'),
          link: 'guideline',
          isVisible: this.role.is_project_admin
        },
        {
          icon: mdiChartBar,
          text: this.$t('statistics.statistics'),
          link: 'statistics',
          isVisible: this.role.is_project_admin
        },
        {
          icon: mdiCog,
          text: this.$t('settings.title'),
          link: 'settings',
          isVisible: this.role.is_project_admin
        }
      ]
      return items.filter(item => item.isVisible)
    }
  },

  methods: {
    toLabeling() {
      const query = this.$services.option.findOption(this.$route.params.id)
      this.$router.push({
        path: this.localePath(this.link),
        query
      })
    }
  }
}
</script>
