<template>
  <Navbar />
  <div id="main-body">
    <router-view></router-view>
  </div>
  <Footer />
</template>
<script>
import Navbar from './components/Navbar.vue'
import Footer from './components/Footer.vue'

export default {
  name: 'App',
  components: {
    Navbar,
    Footer,
  },
}
</script>
<style>
  .alert {
    word-wrap: break-word !important;
  }
</style>