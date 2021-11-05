<template>
  <b-row no-gutters>
    <b-col cols="4">
      <course-detail :id="$route.params.course_id"/>
    </b-col>
    <b-col cols="8">
      <router-view/>
    </b-col>
  </b-row>
</template>

<script>
import CourseDetail from './CourseDetail.vue';

export default {
  components: {
    CourseDetail,
  },
};
</script>
