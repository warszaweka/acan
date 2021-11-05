<template>
  <div>
    <course-card :id="id"/>
    <course-lessons-list :id="id"/>
  </div>
</template>

<script>
import CourseCard from './CourseCard.vue';
import CourseLessonsList from './CourseLessonsList.vue';

export default {
  props: [
    'id',
  ],
  components: {
    CourseCard,
    CourseLessonsList,
  },
};
</script>
