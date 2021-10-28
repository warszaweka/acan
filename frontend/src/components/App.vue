<template>
  <div id="app">
    <h1>ACAN</h1>
    <div id="nav">
      <ul>
        <li><router-link to="/">Home</router-link></li>
        <li><router-link to="/courses">Courses</router-link></li>
      </ul>
    </div>
    <router-view/>
  </div>
</template>
