<template>
  <div>
    <ul>
      <li>
        <router-link to="/">
          Home
        </router-link>
      </li>
      <li>
        <router-link to="/courses">
          Courses
        </router-link>
      </li>
      <li>
        <router-link to="/user">
          {{$store.state.user.username}}
        </router-link>
      </li>
    </ul>
    <router-view/>
  </div>
</template>
