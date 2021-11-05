<template>
  <lesson-detail :id="$route.params.lesson_id"/>
</template>

<script>
import LessonDetail from './LessonDetail.vue';

export default {
  components: {
    LessonDetail,
  },
};
</script>
