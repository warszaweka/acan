<template>
  <video
    ref="video"
    class="video-js"
    >
  </video>
</template>

<script>
import videojs from 'video.js';
import 'video.js/dist/video-js.css';
import environment from '../environment';

export default {
  data() {
    return {
      player: null,
      media: environment.media,
    };
  },
  props: [
    'path',
  ],
  watch: {
    path() {
      this.player.src([
        this.video,
      ]);
    },
  },
  computed: {
    video() {
      return {
        src: `${this.media}/${this.path}`,
        type: 'application/x-mpegURL',
        withCredentials: true,
      };
    },
  },
  mounted() {
    this.player = videojs(this.$refs.video, {
      controls: true,
      sources: [
        this.video,
      ],
      fluid: true,
    });
  },
  beforeDestroy() {
    if (this.player) {
      this.player.dispose();
    }
  },
};
</script>
