<template>
  <v-navigation-drawer
    expand-on-hover
    rail
    permanent
    color="surface"
    class="nav-drawer"
  >
    <v-list>
      <v-list-item class="py-3">
        <template v-slot:prepend>
          <v-avatar color="primary" size="40">
            <v-icon>mdi-fire</v-icon>
          </v-avatar>
        </template>
        <v-list-item-title class="text-h6 font-weight-bold">
          Burning Register
        </v-list-item-title>
      </v-list-item>
    </v-list>

    <v-divider class="mx-3 my-1" />

    <v-list density="comfortable" nav class="px-2">
      <v-list-item
        prepend-icon="mdi-cash-register"
        title="Register"
        value="register"
        to="/"
        rounded="lg"
        class="my-1"
      />
      <v-list-item
        prepend-icon="mdi-chart-bar"
        title="Statistics"
        value="statistics"
        to="/statistics"
        rounded="lg"
        class="my-1"
      />
      <v-list-item
        prepend-icon="mdi-cog"
        title="Admin"
        value="admin"
        to="/admin"
        rounded="lg"
        class="my-1"
      />
    </v-list>
  </v-navigation-drawer>
</template>

<script>
export default {}
</script>

<style scoped>
.nav-drawer {
  border-right: 1px solid rgba(255, 255, 255, 0.06) !important;
}
</style>
